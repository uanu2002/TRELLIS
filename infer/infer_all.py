import os
import sys 
import pandas as pd
from tqdm import tqdm
sys.path.append("..")
# os.environ['ATTN_BACKEND'] = 'xformers'   # Can be 'flash-attn' or 'xformers', default is 'flash-attn'
os.environ['SPCONV_ALGO'] = 'native'        # Can be 'native' or 'auto', default is 'auto'.
                                            # 'auto' is faster but will do benchmarking at the beginning.
                                            # Recommended to set to 'native' if run only once.

import imageio
from trellis.pipelines import TrellisTextTo3DPipeline
from trellis.utils import render_utils, postprocessing_utils
from trellis.datasets.json2prompt import json2prompt

save_dir = './ft_generated_results_float'
# Load a pipeline from a model folder or a Hugging Face model hub.
pipeline = TrellisTextTo3DPipeline.from_pretrained("./finetune_float")
pipeline.cuda()

df_T8 = pd.read_csv('/fs-computility/ai-shen/wujianyu/TRELLIS/datasets/T8/metadata.csv', encoding='utf-8')
# df_f02 = pd.read_csv('/fs-computility/ai-shen/wujianyu/TRELLIS/datasets/f02/metadata.csv', encoding='utf-8')
caption_paths = []
caption_paths.extend(df_T8['captions'].tolist())
# caption_paths.extend(df_f02['captions'].tolist())
gt_paths = []
gt_paths.extend(df_T8['local_path'].tolist())
# gt_paths.extend(df_f02['local_path'].tolist())
assert len(caption_paths)==len(gt_paths)
print(f"Num of samples: {len(caption_paths)}")

for caption_path, gt_path in tqdm(zip(caption_paths, gt_paths)):
    os.makedirs(f"{save_dir}/generated", exist_ok=True)
    output_name = f"{save_dir}/generated/generated_{gt_path.split('/')[-1].split('.')[0]}"
    print(output_name)
    if os.path.exists(f"{output_name}_simple.glb"):
        continue
    caption = json2prompt(caption_path)
    # Run the pipeline
    outputs = pipeline.run(
        caption,
        seed=1,
        # Optional parameters
        # sparse_structure_sampler_params={
        #     "steps": 12,
        #     "cfg_strength": 7.5,
        # },
        # slat_sampler_params={
        #     "steps": 12,
        #     "cfg_strength": 7.5,
        # },
    )

    # GLB files can be extracted from the outputs
    glb = postprocessing_utils.to_glb(
        outputs['gaussian'][0],
        outputs['mesh'][0],
        # Optional parameters
        simplify=0.0,          # Ratio of triangles to remove in the simplification process
        texture_size=1024,      # Size of the texture used for the GLB
    )
    glb.export(f"{output_name}.glb")

    glb_simple = postprocessing_utils.to_glb(
        outputs['gaussian'][0],
        outputs['mesh'][0],
        # Optional parameters
        simplify=0.95,          # Ratio of triangles to remove in the simplification process
        texture_size=1024,      # Size of the texture used for the GLB
    )
    glb_simple.export(f"{output_name}_simple.glb")
