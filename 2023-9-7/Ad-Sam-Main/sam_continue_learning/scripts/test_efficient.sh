export CUDA_VISIBLE_DEVICES=4,5,6,7
python -m torch.distributed.run --nproc_per_node=4 --master_port=30013  efficient_sam_tuning.py \
--model-type vit_t \
--output_prefix efficient_sam_token-tuning_adv@4t \
--batch_size_train=4 \
--batch_size_prompt=4 \
--batch_size_prompt_start=0 \
--find_unused_params \
--numworkers=0 \
--learning_rate=2e-3 \
--train-datasets dataset_sa000000efficient \
--valid-datasets dataset_LVIS dataset_voc2012_val dataset_cityscapes_val dataset_coco2017_val dataset_ade20k_val \
--slow_start \
--prompt_type box \
--restore-model work_dirs/efficient_sam_token-tuning-sa000138_dci-sa000000adv_dice-11186-vit_t/epoch_9.pth \
--eval

#--valid-datasets dataset_hrsod_val dataset_ade20k_val dataset_voc2012_val dataset_cityscapes_val dataset_coco2017_val dataset_camo dataset_big_val dataset_BBC038v1 dataset_DOORS1 dataset_DOORS2 dataset_ZeroWaste dataset_ndis_train dataset_Plittersdorf_test dataset_egohos dataset_LVIS \
