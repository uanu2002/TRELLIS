source /fs-computility/ai-shen/wujianyu/.bashrc
source activate trellis
python train.py \
--config configs/generation/slat_flow_txt_dit_B_64l8p2_fp16.json \
--output_dir outputs/slat_flow_txt_dit_B_64l8p2_fp16_1node_from_scratch \
--data_dir datasets/T8 > train_slat 2>&1