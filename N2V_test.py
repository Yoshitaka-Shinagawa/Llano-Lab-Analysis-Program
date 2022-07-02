# -*- coding: utf-8 -*-
"""
Created on Thu May 20 16:02:00 2021

@author: Yoshi
"""
from n2v.models import N2VConfig, N2V
import numpy as np
from csbdeep.utils import plot_history
from n2v.utils.n2v_utils import manipulate_val_data
from n2v.internals.N2V_DataGenerator import N2V_DataGenerator
from matplotlib import pyplot as plt
import urllib
import os
import zipfile
from tifffile import imread



data = imread("n2v_test_data/flower.tif")

datagen = N2V_DataGenerator()

imgs = datagen.load_imgs_from_directory(directory = "n2v_test_data/", dims="TYX")
print(imgs[0].shape)

plt.imshow(imgs[0][0,...,0], cmap='gray')
plt.show()

imgs_train = [imgs[0][:,:832]]
X = datagen.generate_patches_from_list(imgs_train,shape=(96,96))
imgs_vali = [imgs[0][:,832:]]
X_val = datagen.generate_patches_from_list(imgs_vali,shape=(96,96))

plt.figure(figsize=(14,7))
plt.subplot(1,2,1)
plt.imshow(X[0,...,0], cmap='gray')
plt.title('Training Patch');
plt.subplot(1,2,2)
plt.imshow(X_val[0,...,0], cmap='gray')
plt.title('Validation Patch');

config = N2VConfig(X, unet_kern_size=3, 
                   train_steps_per_epoch=int(X.shape[0]/128), train_epochs=10, train_loss='mse', batch_norm=True, 
                   train_batch_size=128, n2v_perc_pix=0.198, n2v_patch_shape=(64, 64), 
                   n2v_manipulator='uniform_withCP', n2v_neighborhood_radius=5, structN2Vmask = [[0,1,1,1,1,1,1,1,1,1,0]])

model_name = 'n2v_2D'
basedir = 'models'
model = N2V(config, model_name, basedir=basedir)

history = model.train(X, X_val)

print(sorted(list(history.history.keys())))
plt.figure(figsize=(16,5))
plot_history(history,['loss','val_loss']);

