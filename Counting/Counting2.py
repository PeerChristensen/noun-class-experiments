#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
COUNTING TASK
Peer Christensen - hr.pchristensen@gmail.com
For Khanyiso Jonas
September, 2018

DESCRIPTION:
4 sets of noun classes
4 items on the screen in each display (for 5 seconds, 2 secs pause between displays)
In congruent displays, items belong to same noun class
In incongruent displays, items belong to different noun classes
5 of each displays type in memorisation phase

Testing phase has the same displays plus 10 previously unseen (5 of each type)
participants presses 'k' if a display has been seen during memorisation phase.
If not, 's' is pressed.
    
PARTICIPANT INFO:
ID, L1, age, gender
    
DATA STRUCTURE:
 ID, language, trial,item 1,item 2,item 3,item 4,in_mem_phase,answer key,display_type,age,gender
''' 

########### LOAD MODULES #############

from psychopy import visual, event, core, gui
import random
import numpy as np
import itertools as it
import os, random, csv

########### PARTICIPANT INFO & LOG ####

info      = {'ID':'','age':'','language':['Xhosa', 'English'],'gender':['male', 'female']}
if not gui.DlgFromDict(info).OK:  
    core.quit()

log_path  = "/Users/peerchristensen/Desktop/Khanyiso/Counting/Logs/" 
log       = open(log_path+str(info['ID'])+".csv",'wb')   
writer    = csv.writer(log, delimiter=";")
variables = "ID","language","trial","disp_type","target","distr","matching","key","n_targ","age","sex"

writer.writerow(variables)

########### DEFINE VARIBLES ##########

# window
screen_size = [1000,800]
size        = [100,100] # stim size
units       = "pix"
win         = visual.Window(size=screen_size, monitor="testMonitor",color=(1,1,1))

# colour
black       = (-1,-1,-1)

# text
intro_text_xh        = "instructions.."
begin_screen_xh      = visual.TextStim(win, text=intro_text_xh,color=black)
end_screen_xh        = visual.TextStim(win, text="the end",color=black)

intro_text_en        = "instructions.."
begin_screen_en      = visual.TextStim(win, text=intro_text_en,color=black)
end_screen_en        = visual.TextStim(win, text="the end",color=black)

# define positions

widths    = list(np.arange((-screen_size[0]/2)+100,(screen_size[0]/2),150))
heights   = list(np.arange((-screen_size[1]/2)+100,(screen_size[1]/2),150))
positions = list(it.product(widths, heights))
positions = [list(elem) for elem in positions]

#add some randomness to positions
for pos in positions:
    pos[0] = pos[0] + random.randint(-25,26)
    pos[1] = pos[1] + random.randint(-25,26)

# n stimuli
n_displays = 60
n_sets = n_displays/2

########### LOAD ITEMS ##################

path  = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC3/"

image_path_A = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC3/"
image_path_B = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC7/"
image_path_C = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC9/"
image_path_D = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC11/"
    
images_A     = [image_path_A + image for image in os.listdir(image_path_A)]
images_B     = [image_path_B + image for image in os.listdir(image_path_B)]
images_C     = [image_path_C + image for image in os.listdir(image_path_C)]
images_D     = [image_path_D + image for image in os.listdir(image_path_D)] # contains only one item

random.shuffle(images_A)
random.shuffle(images_B)
random.shuffle(images_C)

########### CREATE STIMULI ##############

# create target-distractor pairs within noun classes
list_A1 = list(it.permutations(images_A,2))
list_B1 = list(it.permutations(images_B,2))
list_C1 = list(it.permutations(images_C,2))

# create pairs between noun classes
# A is target class
BC_list = images_B+images_C
BC_list = np.random.choice(BC_list,len(list_A1))

list_A2 = []
for i in range(0,len(list_A1)):
    targ  = list_A1[i][0]
    distr = BC_list[i]
    item=[targ,distr]
    list_A2.append(item)
    
# B is target class
AC_list = images_A+images_C
AC_list = np.random.choice(AC_list,len(list_B1))

list_B2 = []
for i in range(0,len(list_B1)):
    targ  = list_B1[i][0]
    distr = AC_list[i]
    item=[targ,distr]
    list_B2.append(item)
    
# C is target class
AB_list = images_A+images_B
AB_list = np.random.choice(AB_list,len(list_C1))

list_C2 = []
for i in range(0,len(list_C1)):
    targ  = list_C1[i][0]
    distr = AB_list[i]
    item=[targ,distr]
    list_C2.append(item)

stims = [list_A1,list_B1,list_C1,list_A2,list_B2,list_C2]
#[random.shuffle(sublist) for sublist in stims]
stims = [x[:int((n_sets/3))] for x in stims] # subset to limit stims

within_sets = [i for sublist in stims[:3] for i in sublist]
# convert tuples to lists
within_sets = [list(elem) for elem in within_sets]
between_sets = [i for sublist in stims[3:] for i in sublist]

displays = within_sets, between_sets
displays = [i for sublist in displays for i in sublist]

# determine whether target n should match
k = 0
for i in displays:
    if  k < 15 or k >= 30 and k < 45:
        i.append(1)
    else:
        i.append(0)
    k += 1

# add n targets and distractors
for i in displays:
    i.append(np.random.choice(range(8,12)))
    i.append(np.random.choice(range(8,12)))

random.shuffle(displays)

########### RUN EXPERIMENT ###########

if info['language'] == "Xhosa":
    begin_screen_xh.draw()
else:
    begin_screen_en.draw()
win.flip()
event.waitKeys(keyList=['return'])
win.flip()
core.wait(1)

trial = 1
for i in displays[0:3]:
    random.shuffle(positions)
    pos1 = positions[:len(positions)/2]
    pos2 = positions[len(positions)/2:]
    stimuli = []
    if i[2] == 1:
        n = i[3]
    elif i[2] == 0 and i[3] == 8:
        n = 9
    elif i[2] == 0 and i[3] == 11:
        n = 10
    else:
        n = i[3] + np.random.choice([-1,1])
    q = visual.TextStim(win, text = str(n),color=(-1,-1,-1),units=units,pos=[450,-350],height=50)
    for j in range(0,i[3]):
        center_targ = visual.ImageStim(win, image=str(i[0]), size=size, units=units, pos=[0,0])
        targ  = visual.ImageStim(win, image=str(i[0]), size=size, units=units, pos=pos1[j])
        stimuli.append(targ)
    for k in range(0,i[4]):
        distr  = visual.ImageStim(win, image=str(i[1]), size=size, units=units, pos=pos2[k])
        stimuli.append(distr)
    center_targ.draw()
    win.flip()
    core.wait(.3)    
    win.flip()
    for s in stimuli:
        s.draw()
    q.draw()
    win.flip()
    RT=core.Clock()
    core.wait(.3)
    key = event.waitKeys(keyList=['s','k'],timeStamped=RT)
    win.flip()
    if i in within_sets:
        disp_type = 'within'
    else:
        disp_type = 'between'
    print(i[0])
    print(i[1])
    print(disp_type)
    row = info['ID'],info['language'],trial,disp_type,i[0],i[1],i[2],key,i[3],info['age'],info['gender']
    writer.writerow(row)
    trial += 1

core.wait(1)
if info['language'] == "Xhosa":
    end_screen_xh.draw()
else:
    end_screen_en.draw()
win.flip()
event.waitKeys(keyList=['return'])

win.close()
core.quit()











