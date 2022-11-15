import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from PIL import Image

im = Image.open("testImages/b.jpg")
px = im.load()

ax = plt.axes(projection='3d')
x = []
y = []
z = []
c = []

for row in range(0, im.height):
    for col in range(0, im.width):
        pix = px[col, row]
        newCol = (pix[0] / 255, pix[1] / 255, pix[2] / 255)
        print('new col: ', newCol)
        if(not newCol in c):
            x.append(pix[0])
            y.append(pix[1])
            z.append(pix[2])
            c.append(newCol)

ax.scatter(x, y, z, c=c)
plt.show()