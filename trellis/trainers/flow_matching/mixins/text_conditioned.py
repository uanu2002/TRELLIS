from typing import *
import os
os.environ['TOKENIZERS_PARALLELISM'] = 'true'
import torch
import re
import torch.nn as nn
from transformers import AutoTokenizer, CLIPTextModel

from ....utils import dist_utils


class TextConditionedMixin_old:
    """
    Mixin for text-conditioned models.
    
    Args:
        text_cond_model: The text conditioning model.
    """
    def __init__(self, *args, text_cond_model: str = './zer0int/LongCLIP-L-Diffusers', **kwargs): # zer0int/LongCLIP-L-Diffusers ./openai/clip-vit-large-patch14
        super().__init__(*args, **kwargs)
        self.text_cond_model_name = text_cond_model
        self.text_cond_model = None     # the model is init lazily
        self.max_length = 248 if 'Long' in text_cond_model else 77
        
    def _init_text_cond_model(self):
        """
        Initialize the text conditioning model.
        """
        # load model
        with dist_utils.local_master_first():
            model = CLIPTextModel.from_pretrained(self.text_cond_model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.text_cond_model_name)
        model.eval()
        model = model.cuda()
        self.text_cond_model = {
            'model': model,
            'tokenizer': tokenizer,
        }
        self.text_cond_model['null_cond'] = self.encode_text([''])
        
    # @torch.no_grad()
    def encode_text(self, text: List[str]) -> torch.Tensor:
        """
        Encode the text.
        """
        assert isinstance(text, list) and isinstance(text[0], str), "TextConditionedMixin only supports list of strings as cond"
        if self.text_cond_model is None:
            self._init_text_cond_model()
        encoding = self.text_cond_model['tokenizer'](text, max_length=self.max_length, padding='max_length', truncation=True, return_tensors='pt')
        tokens = encoding['input_ids'].cuda()
        embeddings = self.text_cond_model['model'](input_ids=tokens).last_hidden_state
        
        return embeddings
        
    def get_cond(self, cond, **kwargs):
        """
        Get the conditioning data.
        """
        cond = self.encode_text(cond)
        kwargs['neg_cond'] = self.text_cond_model['null_cond'].repeat(cond.shape[0], 1, 1)
        cond = super().get_cond(cond, **kwargs)
        return cond
    
    def get_inference_cond(self, cond, **kwargs):
        """
        Get the conditioning data for inference.
        """
        cond = self.encode_text(cond)
        kwargs['neg_cond'] = self.text_cond_model['null_cond'].repeat(cond.shape[0], 1, 1)
        cond = super().get_inference_cond(cond, **kwargs)
        return cond

class FloatCrossAttentionFusion(nn.Module):
    def __init__(self, embed_dim: int, num_heads: int = 4):
        super().__init__()
        self.cross_attn = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.layernorm = nn.LayerNorm(embed_dim)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.ReLU(),
            nn.Linear(embed_dim, embed_dim),
        )

    def forward(self, text_emb: torch.Tensor, float_emb_list: List[torch.Tensor]) -> torch.Tensor:
        """
        text_emb: (B, L, D)
        float_emb_list: list of float_emb (Nᵢ, D)
        Returns: (B, L, D)
        """
        B, L, D = text_emb.shape
        output = []

        for i in range(B):
            text_i = text_emb[i:i+1]  # (1, L, D)
            float_i = float_emb_list[i]  # (N, D)

            if float_i.shape[0] == 0:
                output.append(text_i)  # no fusion needed
                continue

            float_i = float_i.unsqueeze(0)  # (1, N, D)
            # Cross-attend: query=text, key/value=float
            attn_output, _ = self.cross_attn(query=text_i, key=float_i, value=float_i)  # (1, L, D)

            # Add & Norm + FFN
            fused = self.layernorm(text_i + attn_output)
            fused = fused + self.ffn(fused)
            output.append(fused)

        return torch.cat(output, dim=0)  # (B, L, D)


class TextConditionedMixin:
    """
    Mixin for text-conditioned models.
    
    Args:
        text_cond_model: The text conditioning model.
    """
    def __init__(self, *args, text_cond_model: str = './zer0int/LongCLIP-L-Diffusers', **kwargs): # zer0int/LongCLIP-L-Diffusers ./openai/clip-vit-large-patch14
        super().__init__(*args, **kwargs)
        self.text_cond_model_name = text_cond_model
        self.text_cond_model = None     # the model is init lazily
        self.max_length = 248 if 'Long' in text_cond_model else 77
        self.float_encoder = nn.Sequential(
            nn.Linear(1, 128),
            nn.ReLU(),
            nn.Linear(128, 768),
        ).cuda()
        self.float_text_fuser = FloatCrossAttentionFusion(768).cuda()
        
    def _init_text_cond_model(self):
        """
        Initialize the text conditioning model.
        """
        # load model
        with dist_utils.local_master_first():
            model = CLIPTextModel.from_pretrained(self.text_cond_model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.text_cond_model_name)
        model.eval()
        model = model.cuda()
        self.text_cond_model = {
            'model': model,
            'tokenizer': tokenizer,
        }
        self.text_cond_model['null_cond'] = self.encode_text([''])

    @torch.no_grad()
    def encode_text(self, text: List[str]) -> torch.Tensor:
        """
        Encode the text.
        """
        assert isinstance(text, list) and isinstance(text[0], str), "TextConditionedMixin only supports list of strings as cond"
        if self.text_cond_model is None:
            self._init_text_cond_model()
        encoding = self.text_cond_model['tokenizer'](text, max_length=self.max_length, padding='max_length', truncation=True, return_tensors='pt')
        tokens = encoding['input_ids'].cuda()
        text_embeddings = self.text_cond_model['model'](input_ids=tokens).last_hidden_state
        
        # Float embedding
        float_embeddings = []
        for sentence in text:
            float_vals = [float(m.group(1)) for m in re.finditer(r'=\s*(-?\d+\.\d{2})', sentence)]
            if float_vals:
                float_tensor = torch.tensor(float_vals, dtype=torch.float32).unsqueeze(-1).cuda()
                float_emb = self.float_encoder(float_tensor)  # (N, D)
            else:
                float_emb = torch.empty((0, text_embeddings.size(-1)), dtype=torch.float32).cuda()
            float_embeddings.append(float_emb)

        fused_embeddings = self.float_text_fuser(text_embeddings, float_embeddings)  # (B, L, D)
        return fused_embeddings
        
    def get_cond(self, cond, **kwargs):
        """
        Get the conditioning data.
        """
        cond = self.encode_text(cond)
        kwargs['neg_cond'] = self.text_cond_model['null_cond'].repeat(cond.shape[0], 1, 1)
        cond = super().get_cond(cond, **kwargs)
        return cond
    
    def get_inference_cond(self, cond, **kwargs):
        """
        Get the conditioning data for inference.
        """
        cond = self.encode_text(cond)
        kwargs['neg_cond'] = self.text_cond_model['null_cond'].repeat(cond.shape[0], 1, 1)
        cond = super().get_inference_cond(cond, **kwargs)
        return cond