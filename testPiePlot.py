import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import cv2
from skimage.color import rgb2lab, deltaE_cie76
from collections import Counter
import os


def RGB_HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_colors(image, number_of_colors, show_chart):
    reshaped_image = cv2.resize(image, (600, 400))
    reshaped_image = reshaped_image.reshape(reshaped_image.shape[0] * reshaped_image.shape[1], 3)
    new_reshaped_image = []
    for rgb_list in reshaped_image:
        if rgb_list[0] > 0 and rgb_list[1] > 0 and rgb_list[2] < 80:
            new_reshaped_image.append(rgb_list)
    print(new_reshaped_image)
    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(new_reshaped_image)
    counts = Counter(labels)
    counts = dict(sorted(counts.items()))
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB_HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    if (show_chart):
        plt.figure(figsize=(8, 6))
        plt.pie(counts.values(), labels=rgb_colors, colors=hex_colors)
        plt.show()
    return rgb_colors


image = cv2.imread('testImages/a.jpg')
get_colors(image, 8, True)