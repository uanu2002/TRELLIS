#!/usr/bin/env bash
# usage: ./process.sh /path/to/your/data


# DATA_DIR="$1" 
DATA_DIR="./datasets/dataset_v1" 

scripts=(
  # "dataset_toolkits/test2csv.py"
  dataset_toolkits/render.py
)

for script in "${scripts[@]}"; do
  echo "==> run $script --output_dir $DATA_DIR"
  python "$script" --output_dir "$DATA_DIR"
  echo "==> $script done!"
done

echo "All done!"