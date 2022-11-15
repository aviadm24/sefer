import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
plt.style.use('seaborn')
image = cv2.imread('testImages/c.jpg')
# blue_histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
# red_histogram = cv2.calcHist([image], [1], None, [256], [0, 256])
# green_histogram = cv2.calcHist([image], [2], None, [256], [0, 256])
#
# plt.subplot(3, 1, 1)
# plt.title("histogram of Blue")
# plt.hist(blue_histogram, color="darkblue")
#
# plt.subplot(3, 1, 2)
# plt.title("histogram of Green")
# plt.hist(green_histogram, color="green")
#
# plt.subplot(3, 1, 3)
# plt.title("histogram of Red")
# plt.hist(red_histogram, color="red")
#
# plt.tight_layout()
# plt.show()


def image_to_color_percentage(image_file):
    img = Image.open(image_file)
    size = w, h = img.size
    pixel_num = {
        'redAVG': 0,
        'dark<40': 0,
        '240<red<255,green<40,blue<40': 0,
        '240<red<255,green<100,blue<40': 0,
        '240<red<255,green<150,blue<40': 0,
        '220<red<240,green<40,blue<40': 0,
        '220<red<240,green<100,blue<40': 0,
        '220<red<240,green<150,blue<40': 0,
        '200<red<220,green<40,blue<40': 0,
        '200<red<220,green<100,blue<40': 0,
        '200<red<220,green<150,blue<40': 0,
    }
    # https: // stackoverflow.com / questions / 47520048 / how - to - count - bright - pixels - in -an - image
    # https://stackoverflow.com/questions/50545192/count-different-colour-pixels-python
    for pixel in img.getdata():
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        color = ''
        brightness = ''
        avg = (r + g + b) / 3
        if r != 0:
            if avg / r < 0.9:
                pixel_num['redAVG'] += 1
        if b < 40:
            if g < 40:
                if r < 40:
                    pixel_num['dark<40'] += 1
                elif 240 < r < 255:
                    pixel_num['240<red<255,green<40,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<40,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<40,blue<40'] += 1
            elif g < 100:
                if 240 < r < 255:
                    pixel_num['240<red<255,green<100,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<100,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<100,blue<40'] += 1
            elif g < 150:
                if 240 < r < 255:
                    pixel_num['240<red<255,green<150,blue<40'] += 1
                elif 220 < r < 240:
                    pixel_num['220<red<240,green<150,blue<40'] += 1
                elif 200 < r < 220:
                    pixel_num['200<red<220,green<150,blue<40'] += 1
        # else if avg < 80 then brightness = 'dark'
        # else if avg > 220 then brightness = 'white'
        # else if avg > 150 then brightness = 'light'
        # if avg / r > 0.9 then hue = 'red'
    pixel_avg = {}
    pixel_total = w*h
    for k, v in pixel_num.items():
        if v > 0:
            pixel_avg[k] = v/pixel_total
        # print('k: ', k, ' v: ', v)

    return dict(size=size, pixel_num=pixel_num, pixel_avg=pixel_avg)  # , pix_val=pix_val


image_dict = image_to_color_percentage('testImages/c.jpg')


plt.figure(figsize=(40, 10))

plt.subplot(1, 3, 1)
# plt.axis("off")
plt.title("Original Image")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.hist(image_dict['pixel_num'], color="red")

blue_histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
red_histogram = cv2.calcHist([image], [1], None, [256], [0, 256])
green_histogram = cv2.calcHist([image], [2], None, [256], [0, 256])

plt.subplot(1, 3, 2)
plt.title("Histogram of All Colors")
plt.hist(blue_histogram, color="darkblue")
plt.hist(green_histogram, color="green")
plt.hist(red_histogram, color="red")

plt.subplot(1, 3, 3)
plt.title("Line Plots of All Colors")
plt.plot(blue_histogram, color="darkblue")
plt.plot(green_histogram, color="green")
plt.plot(red_histogram, color="red")

plt.tight_layout()
plt.show()