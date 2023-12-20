#!/bin/bash

#CUDA_VISIBLE_DEVICES_LIST=(0 1 2 3 4 5 6 7)
CUDA_VISIBLE_DEVICES_LIST=(0)
now=1
interval=11188

for id in "${CUDA_VISIBLE_DEVICES_LIST[@]}"
do
    echo "Start: ${now}"
    echo "End $((now + interval))"
    echo "GPU $id" 
    export CUDA_VISIBLE_DEVICES=${id} 
    python null_text_inversion.py \
    --save_root=output/sa_000000@4-Inversion_test \
    --data_root=/data/tanglv/data/sam-1b/sa_000000 \
    --control_mask_dir=/data/tanglv/data/sam-1b/sa_000000/four_mask \
    --caption_path=/data/tanglv/data/sam-1b/sa_000000-blip2-caption.json \
    --controlnet_path=ckpt/control_v11p_sd15_mask_sa000000@4.pth \
    --guidence_scale=1.0 \
    --steps=10 \
    --ddim_steps=20 \
    --start=${now} \
    --end=$((now + interval))\ 
    now=$(expr $now + $interval)
done

wait
