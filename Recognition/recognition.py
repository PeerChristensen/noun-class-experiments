'''
RECOGNITION TASK
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
 
noun class type and match/non-match answers will be added to the data later
'''
########### LOAD MODULES #############

from psychopy.visual import Rect
from psychopy import visual, event, core, gui
import random, os, csv
import numpy as np
import itertools as it

########### PARTICIPANT INFO & LOG ####

info      = {'ID':'','age':'','language':['Xhosa', 'English'],'gender':['male', 'female']}
if not gui.DlgFromDict(info).OK:  
    core.quit()

log_path  = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/Logs/" 
log       = open(log_path+str(info['ID'])+".csv",'wb')   
writer    = csv.writer(log, delimiter=";")
variables = "ID","language","trial","item1","item2","item3","item4","in_mem","key","disp_type","age","sex"

writer.writerow(variables)

########### LOAD ITEMS ##################

image_path_A = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC3/"
image_path_B = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC7/"
image_path_C = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC9/"
image_path_D = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC11/"
    
images_A     = [image_path_A + image for image in os.listdir(image_path_A)]
images_B     = [image_path_B + image for image in os.listdir(image_path_B)]
images_C     = [image_path_C + image for image in os.listdir(image_path_C)]
images_D     = [image_path_D + image for image in os.listdir(image_path_D)] # contains only one item

########### RANDOMISE ITEMS ###############
n_items = 4 # n items (displayed on the scrren)

combinations_A = list(it.permutations(images_A,n_items))
combinations_B = list(it.permutations(images_B,n_items))
combinations_C = list(it.permutations(images_C,n_items))
#combinations_D = list(it.permutations(images_D,n_items))

random.shuffle(combinations_A)
random.shuffle(combinations_B)
random.shuffle(combinations_C)
#random.shuffle(combinations_D)

# make 10 congruent displays

sets_selected = np.random.randint(1,4,10) # sets A,B,C - 10 sets

congruent_displays = []

for set in sets_selected:
    if set == 1:
        congruent_displays.append(combinations_A[0])
        combinations_A.pop(0)
    elif set == 2:
        congruent_displays.append(combinations_B[0])
        combinations_B.pop(0)
    else:
        congruent_displays.append(combinations_C[0])
        combinations_C.pop(0)

# make 10 incongruent sets

incongruent_displays = []

for i in range(1,11):
    set = []
    random.shuffle(images_A)
    random.shuffle(images_B)
    random.shuffle(images_C)
    random.shuffle(images_D)
    set.append(images_A[0])
    set.append(images_B[0])
    set.append(images_C[0])
    set.append(images_D[0])
    random.shuffle(set)
    incongruent_displays.append(set)

# combine displays
displays_mem = [congruent_displays[0:5],incongruent_displays[0:5]]

#flatten list of lists
displays_mem = [item for sublist in displays_mem for item in sublist] 
random.shuffle(displays_mem)

test_displays = [congruent_displays,incongruent_displays]
test_displays = [item for sublist in test_displays for item in sublist] 
random.shuffle(test_displays)

########### DEFINE VARIBLES ##########

win   = visual.Window(size=(1000,800), monitor="testMonitor",color=(1,1,1))

black = (-1,-1,-1)

intro_text_xh        = "some text"
begin_screen_xh      = visual.TextStim(win, text=intro_text_xh,color=black)
mem_phase_screen_xh  = visual.TextStim(win, text="?",color=black)
test_phase_screen_xh = visual.TextStim(win, text="?",color=black)
end_screen_xh        = visual.TextStim(win, text="?",color=black)

intro_text_en        = "some text"
begin_screen_en      = visual.TextStim(win, text=intro_text_en,color=black)
mem_phase_screen_en  = visual.TextStim(win, text="?",color=black)
test_phase_screen_en = visual.TextStim(win, text="?",color=black)
end_screen_en        = visual.TextStim(win, text="?",color=black)

# item positions
item1_pos = [-300,0]
item2_pos = [-100,0]
item3_pos = [ 100,0]
item4_pos = [ 300,0]

# buttons
no_pos  = [-300,-200]
yes_pos = [ 300,-200]

yes = Rect(win=win,pos=yes_pos, width = 100, height = 100, units="pix", fillColor="green")
no  = Rect(win=win,pos=no_pos,  width = 100, height = 100, units="pix", fillColor="red")

size  = (150,150)
units = "pix"

########### RUN EXPERIMENT ###########

if info['language']   == 'Xhosa':
    begin_screen_xh.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    win.flip()
    core.wait(0.3)
    mem_phase_screen_xh.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    core.wait(1)
    for i in displays_mem:
        item1 = visual.ImageStim(win, image=i[0], size=size, units=units, pos=item1_pos)
        item2 = visual.ImageStim(win, image=i[1], size=size, units=units, pos=item2_pos)
        item3 = visual.ImageStim(win, image=i[2], size=size, units=units, pos=item3_pos)
        item4 = visual.ImageStim(win, image=i[3], size=size, units=units, pos=item4_pos)
        item1.draw()
        item2.draw()
        item3.draw()
        item4.draw()
        win.flip()
        core.wait(0.3)
        win.flip()
        core.wait(0.3) # pause
    
    test_phase_screen_xh.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    win.flip()
    core.wait(1)
    trial = 1
    for i in test_displays:
        item1 = visual.ImageStim(win, image=i[0], size=size, units=units, pos=item1_pos)
        item2 = visual.ImageStim(win, image=i[1], size=size, units=units, pos=item2_pos)
        item3 = visual.ImageStim(win, image=i[2], size=size, units=units, pos=item3_pos)
        item4 = visual.ImageStim(win, image=i[3], size=size, units=units, pos=item4_pos)
        item1.draw()
        item2.draw()
        item3.draw()
        item4.draw()
        win.flip()
        core.wait(1)
        win.flip()
        core.wait(1)
        yes.draw()
        no.draw()
        win.flip()
        key = event.waitKeys(keyList=['s','k'])
        win.flip()
        if i in displays_mem:
            in_mem = 1
        else:
            in_mem = 0
        if i in congruent_displays:
            disp_type = "CS"
        else:
            disp_type = "IS"
        row = info['ID'],info['language'],trial,i[0],i[1],i[2],i[3],in_mem,key,disp_type,info['age'],info['gender']
        print(row)
        writer.writerow(row)
        core.wait(1) # pause
        trial += 1
    end_screen_xh.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

else:
    begin_screen_en.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    win.flip()
    core.wait(0.3)
    mem_phase_screen_en.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    core.wait(1)
    for i in displays_mem:
        item1 = visual.ImageStim(win, image=i[0], size=size, units=units, pos=item1_pos)
        item2 = visual.ImageStim(win, image=i[1], size=size, units=units, pos=item2_pos)
        item3 = visual.ImageStim(win, image=i[2], size=size, units=units, pos=item3_pos)
        item4 = visual.ImageStim(win, image=i[3], size=size, units=units, pos=item4_pos)
        item1.draw()
        item2.draw()
        item3.draw()
        item4.draw()
        win.flip()
        core.wait(0.3)
        win.flip()
        core.wait(0.3) # pause
    
    test_phase_screen_en.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    win.flip()
    core.wait(1)
    trial = 1
    for i in test_displays:
        item1 = visual.ImageStim(win, image=i[0], size=size, units=units, pos=item1_pos)
        item2 = visual.ImageStim(win, image=i[1], size=size, units=units, pos=item2_pos)
        item3 = visual.ImageStim(win, image=i[2], size=size, units=units, pos=item3_pos)
        item4 = visual.ImageStim(win, image=i[3], size=size, units=units, pos=item4_pos)
        item1.draw()
        item2.draw()
        item3.draw()
        item4.draw()
        win.flip()
        core.wait(1)
        win.flip()
        core.wait(1)
        yes.draw()
        no.draw()
        win.flip()
        key = event.waitKeys(keyList=['s','k'])
        win.flip()
        if i in displays_mem:
            in_mem = 1
        else:
            in_mem = 0
        if i in congruent_displays:
            disp_type = "CS"
        else:
            disp_type = "IS"
        row = info['ID'],info['language'],trial,i[0],i[1],i[2],i[3],in_mem,key,disp_type,info['age'],info['gender']
        writer.writerow(row)
        core.wait(1) # pause
        trial += 1
    end_screen_en.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

log.close()
win.close()
core.quit()

