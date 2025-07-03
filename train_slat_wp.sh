source /fs-computility/ai-shen/wujianyu/.bashrc
source activate trellis
python train.py \
--config configs/generation/slat_flow_txt_dit_B_64l8p2_fp16_wp.json \
--output_dir outputs/slat_flow_txt_dit_B_64l8p2_fp16_1node_v1 \
--data_dir datasets/dataset_v1 > train_slat_wp.log 2>&1