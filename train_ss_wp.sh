source /fs-computility/ai-shen/wujianyu/.bashrc
source activate trellis
python train.py \
--config configs/generation/ss_flow_txt_dit_B_16l8_fp16_wp.json \
--output_dir outputs/ss_flow_txt_dit_B_16l8_fp16_1node_v1 \
--data_dir datasets/dataset_v1 > train_ss_wp.log 2>&1