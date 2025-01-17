# Copyright by HQ-SAM team
# All rights reserved.

## data loader
from __future__ import print_function, division

import numpy as np
import random
from copy import deepcopy
from skimage import io
import os
from glob import glob

import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from torchvision import transforms, utils
from torchvision.transforms.functional import normalize
import torch.nn.functional as F
from torch.utils.data.distributed import DistributedSampler
import json
from pycocotools import mask


class ImagenetPartDataset(Dataset):
    def __init__(self, name_im_gt_list, transform=None, eval_ori_resolution=False,batch_size_prompt=-1):

        self.transform = transform
        self.dataset = {}
        ## combine different datasets into one
        dataset_names = []
        dt_name_list = [] # dataset name per image
        im_name_list = [] # image name
        im_path_list = [] # im path
        gt_path_list = [] # gt path
        im_ext_list = [] # im ext
        gt_ext_list = [] # gt ext
        for i in range(0,len(name_im_gt_list)):
            dataset_names.append(name_im_gt_list[i]["dataset_name"])
            # dataset name repeated based on the number of images in this dataset
            dt_name_list.extend([name_im_gt_list[i]["dataset_name"] for x in name_im_gt_list[i]["im_path"]])
            im_name_list.extend([x.split(os.sep)[-1].split(name_im_gt_list[i]["im_ext"])[0] for x in name_im_gt_list[i]["im_path"]])
                
            im_path_list.extend(name_im_gt_list[i]["im_path"])
            gt_path_list.extend(name_im_gt_list[i]["gt_path"])
                
            im_ext_list.extend([name_im_gt_list[i]["im_ext"] for x in name_im_gt_list[i]["im_path"]])
            gt_ext_list.extend([name_im_gt_list[i]["gt_ext"] for x in name_im_gt_list[i]["gt_path"]])

        self.dataset["data_name"] = dt_name_list
        self.dataset["im_name"] = im_name_list
        self.dataset["im_path"] = im_path_list
        self.dataset["ori_im_path"] = deepcopy(im_path_list)
        self.dataset["gt_path"] = gt_path_list
        self.dataset["ori_gt_path"] = deepcopy(gt_path_list)
        self.dataset["im_ext"] = im_ext_list
        self.dataset["gt_ext"] = gt_ext_list

        self.eval_ori_resolution = eval_ori_resolution
        self.batch_size_prompt = batch_size_prompt
        
        #To DO: open all instance
        self.all_instance = batch_size_prompt
    def __len__(self):
        return len(self.dataset["im_path"])
    def __getitem__(self, idx):
        im_path = self.dataset["im_path"][idx]
        gt_path = self.dataset["gt_path"][idx]
        
        im = io.imread(im_path)
        naive_gt = io.imread(gt_path)        
        
        unique_list = sorted(np.unique(naive_gt))        
        gt = np.empty((0,naive_gt.shape[0],naive_gt.shape[1]))
        
        
        print(unique_list)
        
        for i in unique_list:
            if i==40: continue
            tmp_gt = np.zeros((naive_gt.shape[0],naive_gt.shape[1]))     
            tmp_gt[naive_gt==i]=255
            gt = np.concatenate((gt,tmp_gt[np.newaxis,:,:]))
            
            # import cv2
            # cv2.imwrite(f"{str(i)}.png",tmp_gt)
        # print(gt.shape)
        # raise NameError       
        if len(im.shape) < 3:
            im = im[:, :, np.newaxis]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
            
        im = torch.tensor(im.copy(), dtype=torch.float32)
        im = torch.transpose(torch.transpose(im,1,2),0,1)
        gt = torch.tensor(gt, dtype=torch.float32)
        
        sample = {
            "imidx": torch.from_numpy(np.array(idx)),
            "image": im,
            "label": gt,
            "shape": torch.tensor(im.shape[-2:]),
        }

        if self.transform and gt.shape[0]: 
            sample = self.transform(sample)

        sample["ori_label"] = gt.type(torch.uint8)  # NOTE for evaluation only. And no flip here
        sample['ori_im_path'] = self.dataset["im_path"][idx]
        sample['ori_gt_path'] = self.dataset["gt_path"][idx]

        return sample
