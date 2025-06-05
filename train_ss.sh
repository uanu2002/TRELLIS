source /fs-computility/ai-shen/wujianyu/.bashrc
source activate trellis
python train.py \
--config configs/generation/ss_flow_txt_dit_B_16l8_fp16.json \
--output_dir outputs/ss_flow_txt_dit_B_16l8_fp16_1node_from_scratch \
--data_dir datasets/T8 > train_ss 2>&1