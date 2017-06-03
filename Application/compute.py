#!/usr/bin/env python2

NUM_IMAGE = 2
IMAGE_HEIGHT = 100
IMAGE_WIDTH = 100

from sklearn.decomposition import PCA
import datetime
import errno
import gzip
import matplotlib.image as matimage
import numpy as np
import os
import shutil
import subprocess
import sys
from scipy import linalg, mat, dot
from scipy.spatial import distance
from scipy.linalg import norm

try:
    import cPickle as pickle
except ImportError:
    import pickle

def _reshape(image, height, width):
    desired_shape = (height, width)
    if image.shape != desired_shape:
        actual_height, actual_width = image.shape[:2]
        if len(image.shape) == 3:
            image = image[:, :, 0]
        elif actual_height < height:
            padding = np.zeros((height - actual_height, width))
            image = np.vstack([image, padding])
        elif actual_width < width:
            padding = np.zeros((height, width - actual_width))
            image = np.hstack([image, padding])
        else:
            raise ValueError('unhandled resizing case: ' + str(image.shape))
    return image.reshape(1, height * width)

def inputpath():
    return ['pngimage/1.png']

def compute(image_paths, image_path, n_eigenfaces=NUM_IMAGE,
            width=IMAGE_WIDTH, height=IMAGE_HEIGHT):
    input_path = image_path
    image_matrix = np.vstack([_reshape(image, height, width)
                              for image in _imread(image_paths)])
                              
    print image_matrix.size

    img1 = np.vstack([_reshape(image, height, width)
                      for image in _imread(input_path)])

    pca = PCA(n_components=n_eigenfaces).fit(image_matrix)
    eigenvectors = pca.components_.reshape((n_eigenfaces, height, width))
    eigenvalues = pca.explained_variance_ratio_
    data_mean = pca.mean_.reshape((height, width))
    po = pca.transform(image_matrix)
    eigenvectors = image_matrix.reshape(2, 100, 100)
    recons1 = po[0][0] * eigenvectors[0] + po[0][1] * eigenvectors[1]
    rimage = np.reshape(img1[0], (100, 100))
    diff1 = rimage - recons1
    det1 = np.linalg.det(diff1)
    a = rimage
    b = recons1
    c = dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)
    n_m, n_0 = compare_images(a, b)
    n_m = np.mean(n_m)
    n_0 = np.mean(n_0)
    return n_0 * 1.0 / a.size


def compare_images(img1, img2):
    img1 = normalize(img1)
    img2 = normalize(img2)
    diff = img1 - img2
    m_norm = sum(abs(diff))
    z_norm = norm(diff.ravel(), 0)
    return (m_norm, z_norm)

def normalize(arr):
    rng = arr.max() - arr.min()
    arrmin = arr.min()
    return (arr - arrmin) * 255 / rng

def _imread(paths):
    for path in paths:
        try:
            yield matimage.imread(path)
        except RuntimeError:
            print 'could not read image'

def _main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__.split('Usage:')[0])
    parser.add_argument('files', nargs='+', help='the image files to reduce')
    args = parser.parse_args()

    out = compute(args.files)
    print out

if __name__ == '__main__':
    _main()