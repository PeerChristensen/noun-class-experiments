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

# the lines below create a dialog box in which to put info about participants
# The info is stored in a 'dictionary' called 'info'.
# A 'dict' contains any unordered number of key-value pairs.
# e.g. to access 'age', type indo['age']
info      = {'ID':'','age':'','language':['Xhosa', 'English'],'gender':['male', 'female']}
if not gui.DlgFromDict(info).OK: 
    core.quit()

# These lines create a .csv log file
# the top row will be the variable names stored in 'variables'
log_path  = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/Logs/" 
log       = open(log_path+str(info['ID'])+".csv",'wb')   
writer    = csv.writer(log, delimiter=";")
variables = "ID","language","trial","item1","item2","item3","item4","in_mem","key","disp_type","age","sex"

# write the first row in our csv file
writer.writerow(variables)

########### LOAD ITEMS ##################

# paths to where the image files are stored
# make sure to get these right when switching between laptops
image_path_A = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC3/"
image_path_B = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC7/"
image_path_C = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC9/"
image_path_D = "/Users/peerchristensen/Desktop/Khanyiso/Recognition/NC11/"

# these lines will glue path and file names together
images_A     = [image_path_A + image for image in os.listdir(image_path_A)]
images_B     = [image_path_B + image for image in os.listdir(image_path_B)]
images_C     = [image_path_C + image for image in os.listdir(image_path_C)]
images_D     = [image_path_D + image for image in os.listdir(image_path_D)] # contains only one item

########### RANDOMISE ITEMS ###############
# n items (displayed on the scrren)
n_items = 4 

# create lists with all possible combinations within noun classes
combinations_A = list(it.permutations(images_A,n_items))
combinations_B = list(it.permutations(images_B,n_items))
combinations_C = list(it.permutations(images_C,n_items))
#combinations_D = list(it.permutations(images_D,n_items))

# randomise the lists of possible combinations 
random.shuffle(combinations_A)
random.shuffle(combinations_B)
random.shuffle(combinations_C)
#random.shuffle(combinations_D)

# make 10 congruent displays

# first, we generate 10 random numbers between 1-3
sets_selected = np.random.randint(1,4,10) # '1,4' here means 1,2,3, so not incl 4

# we then make an empty list an empty list..
congruent_displays = []

# ..and take the first combination of 4 images in either set A,B or C
# based on each of the random numbers
# i.e. 1 = A, 2 = B. 3 = C
# the first combination is then stored in our empty list
# this process is repeated 10 times (the length of the generated numbers)
# the pop(0) part removes the combination from the list of possible combinations.
# here, '0' means the first element (first combination)
# we do this so that the next time we take the first combination, it will be a different one

for set in sets_selected: # for each set/element in the sets_selected list..
    if set == 1: #.. if the set is equal to 1..
        congruent_displays.append(combinations_A[0]) # store first combination of 'combinations_A in our empty list
        combinations_A.pop(0) # .. then remove the combination from combinations_A
    elif set == 2: # "or if" ..
        congruent_displays.append(combinations_B[0])
        combinations_B.pop(0)
    else: # if set is not equal to 1 or 2.. (i.e. 3) ..
        congruent_displays.append(combinations_C[0])
        combinations_C.pop(0)

# make 10 incongruent sets

# again, an empty list for storing lists of 4 images to display
incongruent_displays = []

for i in range(1,11): # range(1,11) means [1,2,3,4,5,56,7,8,9,10]
    set = [] # for storing a single combination. It is reset at each iteration
    # randomise the order of images 
    random.shuffle(images_A)
    random.shuffle(images_B)
    random.shuffle(images_C)
    random.shuffle(images_D)
    # take the first image from each and add to our list (set)
    set.append(images_A[0])
    set.append(images_B[0])
    set.append(images_C[0])
    set.append(images_D[0])
    # randomise the order
    random.shuffle(set)
    # add set to our f
    incongruent_displays.append(set)

# combine congruent and incongruent displays
# for the memory phase, we only take half, meaning 5 congruent displays
# and 5 incongruent displays
displays_mem = [congruent_displays[0:5],incongruent_displays[0:5]]

#"flatten" list of lists (i.e. unnesting lists wihtin list
displays_mem = [item for sublist in displays_mem for item in sublist] 
random.shuffle(displays_mem)

# for the test displays, we'll need all congruent and incongruent displays
test_displays = [congruent_displays,incongruent_displays]
test_displays = [item for sublist in test_displays for item in sublist] 
random.shuffle(test_displays)

########### DEFINE VARIBLES ##########

# this creates the screen, colour is in rgb format and 1,1,1 means white
win   = visual.Window(size=(1000,800), monitor="testMonitor",color=(1,1,1))

# We'll use black colour for all text displays, so we define this colour for convenience
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

# item positions in pixels
# the first number is lateral position, the second is vertical position
# 0,0 is the default setting (center screen)
item1_pos = [-300,0] # left
item2_pos = [-100,0] # left, but closer to center
item3_pos = [ 100,0] # right, but closer to center
item4_pos = [ 300,0] # right

# button positions
no_pos  = [-300,-200] # low, right
yes_pos = [ 300,-200] # low, left

# create buttons as rectanfular objects
yes = Rect(win=win,pos=yes_pos, width = 100, height = 100, units="pix", fillColor="green")
no  = Rect(win=win,pos=no_pos,  width = 100, height = 100, units="pix", fillColor="red")

# settings for the stimuli
size  = (150,150)
units = "pix"

########### RUN EXPERIMENT ###########

if info['language']   == 'Xhosa':      # if Xhosa is the language of the participant
    begin_screen_xh.draw()             # prepare the "begin screen" with instructions "behind the scenes"
    win.flip()                         # shows the screen
    event.waitKeys(keyList=['return']) # wait for return/enter to be pressed
    win.flip()                         # then "flip" screen to blank
    core.wait(0.3)                     # and wait a few seconds
    mem_phase_screen_xh.draw()         # prepare a screen saying e.g. "memorisation phase"
    win.flip()                         # show it 
    event.waitKeys(keyList=['return']) # wait for return key to be pressed
    core.wait(1)                       # wait
    for i in displays_mem:             # for each item (e.g. set of four image paths in the list)..
        item1 = visual.ImageStim(win, image=i[0], size=size, units=units, pos=item1_pos) # create stim 1..
        item2 = visual.ImageStim(win, image=i[1], size=size, units=units, pos=item2_pos) # 2
        item3 = visual.ImageStim(win, image=i[2], size=size, units=units, pos=item3_pos) # 3
        item4 = visual.ImageStim(win, image=i[3], size=size, units=units, pos=item4_pos) # 4.. at their respective positions
        item1.draw()                   # draw in the background
        item2.draw()
        item3.draw()
        item4.draw()
        win.flip()                     # show them simultaneously
        core.wait(0.3)                 # and wait for n secs
        win.flip()                     # then blank screen
        core.wait(0.3) # pause
        
    # after 10 iterations, we're ready for the test phase
    test_phase_screen_xh.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    win.flip()
    core.wait(1)
    trial = 1                          # this creates a "counter" keeping track of trial number
    # much the same as the above loop
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
        #Instead of proceeding to the next display we want to collect yes/no answers
        yes.draw() # the green "yes" button (that we created as a rectangular object
        no.draw()  # the red "no" button
        win.flip() 
        key = event.waitKeys(keyList=['s','k']) # participant must press 's' (no) or 'k' (yes)
        win.flip()
        if i in displays_mem:       # if the i'th (current) displays is in the memorisation set..
            in_mem = 1              # we set a variable called in_mem to 1
        else:                       # otherwise..
            in_mem = 0              # 0
        if i in congruent_displays: # if the i'th (current) displays is found in the list of "congruent" displays
            disp_type = "CS"        # we set a variable "disp_type" to "CS" (congruent set)
        else:                       # otherwise
            disp_type = "IS"        # IS
        # we then define what data to include + the order in each row in our csv file
        row = info['ID'],info['language'],trial,i[0],i[1],i[2],i[3],in_mem,key,disp_type,info['age'],info['gender']
        writer.writerow(row)        # we pass the "row" to the csv file
        core.wait(1) # pause
        trial += 1                  # we then add 1 to the trial counter for each iteration 
    end_screen_xh.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

# If the language is set to 'English', we do the exact same procedure, but with English text
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
        print(row)
        writer.writerow(row)
        core.wait(1) # pause
        trial += 1
    end_screen_en.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

log.close() # close file
win.close() # close window
core.quit() # exit program