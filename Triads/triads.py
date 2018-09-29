
'''
TRIADS TASK
Peer Christensen - hr.pchristensen@gmail.com
For Khanyiso Jonas
September, 2018

DESCRIPTION:
24 stimulus items (triads), in two sets
For each item/trial, participants select the object most similar to 'object X'
Pressing 's' selects 'object A', 'k' selects 'object B'
Order of the two sets is balanced
Order of items within sets is randomised
    
PARTICIPANT INFO:
ID, age, gender, L1, AoA ENglish, condition
    
DATA STRUCTURE:
ID, L1, condition, trial, item, match, selected, correct, info...
'''
########### LOAD MODULES #############

from psychopy import visual, event, core, gui
import random, os, csv

########### PARTICIPANT INFO & LOG ####

info      = {'ID':'','age':['3','5','7'],'language':['Xhosa', 'English'],'gender':['male', 'female'],'condition': ['1','2','3']}
if not gui.DlgFromDict(info).OK:    #, order = ['ID', 'age', 'language', 'gender','condition']   
    core.quit()

log_path  = "/Users/peerchristensen/Desktop/Khanyiso/Triads/Logs/" 
log       = open(log_path+str(info['ID'])+".csv",'wb')   
writer    = csv.writer(log, delimiter=";")
variables = "ID", "language", "condition", "trial", "item", "key", "age", "sex"

writer.writerow(variables)

########### LOAD & RANDOMISE ITEMS ###############

if int(info['condition']) == 1:
    if info['language']   == 'Xhosa':
        image_path_A = "/Users/peerchristensen/Desktop/Khanyiso/Triads/Xhosa_A/"
        image_path_B = "/Users/peerchristensen/Desktop/Khanyiso/Triads/Xhosa_B/"
    
    elif info['language'] == 'English':
        image_path_A = "/Users/peerchristensen/Desktop/Khanyiso/Triads/English_A/"
        image_path_B = "/Users/peerchristensen/Desktop/Khanyiso/Triads/English_B/"
    
    images_A     = os.listdir(image_path_A)
    images_B     = os.listdir(image_path_B)
    images_A = [image_path_A + i for i in images_A]
    images_B = [image_path_B + i for i in images_B]

elif int(info['condition']) > 1: 
    image_path_A = "..."
    image_path_B = "..."
    
    images_A     = os.listdir(image_path_A)
    images_B     = os.listdir(image_path_B)
    images_A = [image_path_A + i for i in images_A]
    images_B = [image_path_B + i for i in images_B]

random.shuffle(images_A)
random.shuffle(images_B)

if int(info['ID']) % 2   == 1: #int(info['ID'])
    images = images_A,images_B

elif int(info['ID']) % 2 == 0: #int(info['ID'])
    images = images_B,images_A

images = [item for sublist in images for item in sublist]
images = [ item for item in images if "DS" not in item ]

########### DEFINE VARIBLES ##########

black           = (-1,-1,-1)
win             = visual.Window(size=(1000,800), monitor="testMonitor",color=(1,1,1))
begin_screen_xh = visual.TextStim(win, text="?",color=black)
intro_text_xh = "some text"
end_screen_xh   = visual.TextStim(win, text="?",color=black)
begin_screen_en = visual.TextStim(win, text="?",color=black)
end_screen_en   = visual.TextStim(win, text="?",color=black)

########### RUN WARM-UP TRIALS ########



########### RUN EXPERIMENT ###########

if info['language'] == 'Xhosa':
    begin_screen_xh.draw()
elif info['language'] == 'English':
    begin_screen_en.draw()
win.flip()
event.waitKeys(keyList=['return'])
win.flip()
core.wait(1)

trial = 1
for i in images:
    print(i)
    img = visual.ImageStim(win, image=i)
    img.draw()
    win.flip()
    key = event.waitKeys(keyList=['s','k'])
    win.flip()
    row = info['ID'],info['language'],info['condition'],trial,i,key,info['age'],info['gender']
    writer.writerow(row)
    trial += 1
    core.wait(.8)
    
if info['language'] == "Xhosa":
    end_screen_xh.draw()
elif info['language'] == "English":
    end_screen_en.draw()
win.flip()
event.waitKeys(keyList=['return'])

log.close()
win.close()
core.quit()
