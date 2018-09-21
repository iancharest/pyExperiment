from psychopy.visual import RadialStim, GratingStim #import some libraries from PsychoPy
from psychopy import visual, event, core
import matplotlib.pyplot as plt
import os
import numpy as np
from experiments import *
from numpy.random import choice as rchoice

"""
TODO:
    fix monitor
    fix dialogue box for getting responses
"""
def loadInfoTxt():
    b = ''
    with open('instructions.txt', 'r') as f:
        for line in f.readlines():
            b += line + '\n'
    return b

def getCorrectResponse(opt, t, keys):
    return keys[list(opt).index(t)]

def createMasks(win, n_masks):
    """
    Takes a list of images and makes masks
    """
    masks = []
    for i in range(n_masks):
        mask = RadialStim(win, mask='gauss', size=6, radialCycles=5,
                         angularCycles=5, ori=np.random.randint(360), name='mask')
        masks.append(mask)
    return masks

def createTrialSequence(win, T1, T2, t1_pos, t2_pos, masks, n_masks, RSVP_len):
    # Create trial_sequence
    trial_sequence = [rchoice(range(n_masks)) for x in range(RSVP_len)]
    trial_sequence = [masks[x]for x in trial_sequence]

    # Add T1 and T2 to their respective positions in the stream
    trial_sequence[t1_pos] = GratingStim(win,  mask='gauss', pos=(0, 0),
                             name=f'T1 {T1}', size=6, ori=T1, sf=3)
    trial_sequence[t2_pos] = GratingStim(win,  mask='gauss', pos=(0, 0),
                             name=f'T2 {T2}', size=6, ori=T2, sf=3)
    return trial_sequence

# load images
info_txt = loadInfoTxt()
fix_time = 0.5
img_dur = 0.02
SOA = 0.1
n_trials = 10
t1_pos = 3
t2_pos = 7
RSVP_len = 12
n_masks = 20
im_size = 5 # in degrees
n_blocks = 2
max_response_time = 2.5
keys  = ['z', 'm']
# initiate
ab = AB(name='AB_ping', distance_to_screen=100)

# generate trials
trial_dict = {
            'trial sequence':None, # list of named psychopy objects to draw
            'fixation time': fix_time,
            'imgdur': img_dur,
            'SOA': SOA,
            'max response time': max_response_time,
            'T1': None, # T1 identifier
            'T2': None, # T2 identifier
            'T1 options': None, # list of keys
            'T2 options': None, # list of keys
            'T1 menu': None, # list of drawable objects shown as alternatives
            'T2 menu': None, # list of drawable objects shown as alternatives
            'Response keys': keys, # possible key responses
            'T2 keys': None, # possible key responses
            'T1 correct response': None, # correct key response for T1
            'T2 correct response': None  # correct key response for T2
            }

empty = visual.GratingStim(ab.win, size=0, name='empty')
ping = RadialStim(ab.win, mask='circle', size=6, radialCycles=0,
                 angularCycles=0, color=(-1, -1, -1), name='ping')
for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(ab.win, text=info_txt, pos=(0, 0), height=0.5)
        params = {'obj_list': [info_message], 'responses': ['space']}
        ab.drawAndWait(**params)
    masks = createMasks(ab.win, n_masks)
    for i in range(n_trials):
        T1 = rchoice((45, -45), 1)[0]
        T2 = rchoice((45, -45), 1)[0]
        trial_sequence = createTrialSequence(ab.win, T1, T2, t1_pos, t2_pos, masks, n_masks, RSVP_len)
        addage = [empty, empty, empty, ping]
        trial_sequence.extend(addage)
        # Make menu options
        T1_opt = np.array([45, -45])
        np.random.shuffle(T1_opt)
        T2_opt = np.array([45, -45])
        np.random.shuffle(T2_opt)

        # create image instances for menu
        menu_txt = visual.TextStim(ab.win, text='Which one was the first target', pos=(0, 4), height=0.5)
        menu_txt2 = visual.TextStim(ab.win, text='Which one was the second target', pos=(0, 4), height=0.5)
        pos = ([-4, 0], [4, 0])
        T1_menu = [GratingStim(ab.win,  mask='gauss', pos=pos[i],
                                 name=f'Menu {x}', size=6, ori=x, sf=3) for i, x in enumerate(T1_opt)]
        T1_menu.append(menu_txt)
        T2_menu = [GratingStim(ab.win,  mask='gauss', pos=pos[i],
                                 name=f'Menu {x}', size=6, ori=x, sf=3) for i, x in enumerate(T2_opt)]
        T2_menu.append(menu_txt2)


        # Add specifics to trial_dict
        trial_dict['trial sequence'] = trial_sequence
        trial_dict['trial type'] = 'ping'
        trial_dict['T1'] = T1
        trial_dict['T2'] = T2
        trial_dict['T1 options'] = T1_opt
        trial_dict['T2 options'] = T2_opt
        trial_dict['T1 menu'] = T1_menu
        trial_dict['T2 menu'] = T2_menu
        trial_dict['T1 correct response'] = getCorrectResponse(T1_opt, T1, keys)
        trial_dict['T2 correct response'] = getCorrectResponse(T2_opt, T2, keys)

        ab.addTrial(trial_dict.copy())

    if block == n_blocks-1: # if last block
        block_txt = f'End of run {ab.run}\npress space to continue'
        info_message = visual.TextStim(ab.win, text=block_txt, pos=(0, 0), height=0.5)
    else:
        block_txt = f'End of block {block+1}/{n_blocks}\nPress space to continue'
        info_message = visual.TextStim(ab.win, text=block_txt, pos=(0, 0), height=0.5)
    params = {'obj_list': [info_message], 'responses': ['space']}
    ab.start(run_after=[(ab.drawAndWait, params)])
