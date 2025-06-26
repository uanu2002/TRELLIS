import os
import sys 
import pandas as pd
sys.path.append("..")
# os.environ['ATTN_BACKEND'] = 'xformers'   # Can be 'flash-attn' or 'xformers', default is 'flash-attn'
os.environ['SPCONV_ALGO'] = 'native'        # Can be 'native' or 'auto', default is 'auto'.
                                            # 'auto' is faster but will do benchmarking at the beginning.
                                            # Recommended to set to 'native' if run only once.

import imageio
from trellis.pipelines import TrellisTextTo3DPipeline
from trellis.utils import render_utils, postprocessing_utils
from trellis.datasets.json2prompt import json2prompt
# Load a pipeline from a model folder or a Hugging Face model hub.
pipeline = TrellisTextTo3DPipeline.from_pretrained("./finetune_float")
pipeline.cuda()

df_T8 = pd.read_csv('/fs-computility/ai-shen/wujianyu/TRELLIS/datasets/T8/metadata.csv', encoding='utf-8')
caption_paths = []
caption_paths.extend(df_T8['captions'].tolist())
gt_paths = []
gt_paths.extend(df_T8['local_path'].tolist())
# prompt = json2prompt(caption_paths[1])
# print(caption_paths[0])

name = 'origin3-2'
# Run the pipeline
# with open(f"./generated_results_626/{name}.txt", 'w') as f:
#     f.write(prompt)

with open(f"./generated_results_626/origin3-2.txt", "r") as f: 
    prompt = f.read()

# with open(f"./generated_results_626/{name}.txt", 'w') as f:
#     f.write(prompt)

outputs = pipeline.run(
    prompt,
    seed=1,
)

# GLB files can be extracted from the outputs
glb = postprocessing_utils.to_glb(
    outputs['gaussian'][0],
    outputs['mesh'][0],
    # Optional parameters
    simplify=0.95,          # Ratio of triangles to remove in the simplification process
    texture_size=1024,      # Size of the texture used for the GLB
)
glb.export(f"./generated_results_626/{name}.glb")

