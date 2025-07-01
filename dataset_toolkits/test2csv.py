import pathlib
import hashlib
import json
import pandas as pd
import trimesh
import numpy as np
from datetime import datetime
from typing import Any
from tqdm import tqdm
import argparse
import os

def compute_aesthetic_score(mesh: trimesh.Trimesh) -> float:
    return 100 # np.random.rand()


def sha256_of_file(path: pathlib.Path, chunk: int = 8192) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for piece in iter(lambda: f.read(chunk), b""):
            h.update(piece)
    return h.hexdigest()

def process_folder(obj_dir: str,
                   captions_dir: str,
                   csv_out: str,
                   glb_dir: str):

    obj_dir     = pathlib.Path(obj_dir)
    captions_dir= pathlib.Path(captions_dir)
    glb_dir     = pathlib.Path(glb_dir)

    glb_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for obj_path in tqdm(obj_dir.rglob("*.obj")):
        file_id = obj_path.stem
        # if 'sample' not in file_id:
        #     continue
        try:
            mesh = trimesh.load(obj_path, force="mesh")
        except Exception as e:
            print(f"Load {obj_path} error: {e}!")
            continue

        glb_path = glb_dir / f"{file_id}.glb"
        glb_path_rel = f"glb/{file_id}.glb"
        mesh.export(glb_path, file_type="glb")

        if not os.path.exists(glb_path):
            print(f"glb does not exist!")
            continue
        cap_file = captions_dir / f"{file_id}_info.json"
        if not os.path.exists(cap_file):
            print(f"json does not exist!")
            continue
        captions = cap_file

        sha = sha256_of_file(glb_path)

        records.append({
            "sha256": sha,
            "file_identifier": glb_path_rel,
            "local_path": f"{glb_path_rel}",
            "aesthetic_score": 100,
            "captions": captions,
            "rendered": False,
            "voxelized": False,
            "num_voxels": 0,
            "cond_rendered": False,
        })

    cols = ["sha256", "file_identifier", "local_path",
            "aesthetic_score", "captions",
            "rendered", "voxelized", "num_voxels", "cond_rendered"]

    pd.DataFrame(records, columns=cols).to_csv(csv_out, index=False, encoding="utf-8")
    print(f"Finished: {csv_out}  ({len(records)} rows)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the metadata')
    opt = parser.parse_args()
    process_folder(
        obj_dir=f"{opt.output_dir}/mesh",
        captions_dir=f"{opt.output_dir}/json",
        csv_out=f"{opt.output_dir}/metadata.csv",
        glb_dir=f"{opt.output_dir}/glb",
    )
