from psychopy import visual, event, core, gui
import random
import numpy as np
import itertools as it
import os, random


# make a grid
screen_size = [1000,800]

win   = visual.Window(size=screen_size, monitor="testMonitor",color=(1,1,1))

widths = list(np.arange((-screen_size[0]/2)+150,(screen_size[0]/2)-50,150))

#random.shuffle(widths)

heights = list(np.arange((-screen_size[1]/2)+150,(screen_size[1]/2)-50,150))
#for i in range(0,len(heights)):
#    heights[i] = heights[i] + random.randint(-40,41)

#random.shuffle(heights)

positions = list(it.product(widths, heights))
positions = [list(elem) for elem in positions]

for pos in positions:
    pos[0] = pos[0] + random.randint(-25,26)
    pos[1] = pos[1] + random.randint(-25,26)

random.shuffle(positions)

#load image
path  = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC3/"
image = str(path+os.listdir(path)[0])

images = []
for i in positions:
    img = visual.ImageStim(win, image=image, size=[100,100], units="pix", pos=i)
    images.append(img)

for i in images:
    i.draw()
core.wait(2)
win.flip()
event.waitKeys(keyList=['return'])

win,close()
core.quit()

