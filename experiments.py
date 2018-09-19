from psychopy import gui, visual, event, core
import sys, logging, os
from controller import *
from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

"""
A selection of experiment classes
"""

class bareBoneExperiment(Controller):
    """
    Bare minimum of attributes and methods needed to be compatible with
    the Experiment-class
    """
    def __init__(self, **args):
        super().__init__(**args)
        self.trials = []

    def runTrials():
        pass

    def clearTrials(self):
        self.trials = []


class AB(Controller):
    """
    Todo:
        Write this doc string
    """
    def __init_(self, **args):
        Controller.__init__(self, **args)

    def drawAndWait(self, obj_list, responses=[]):
        """
        parameters
            obj: list of psychopy object with draw method
            responses: list
                list of keywords that will exit the loop
        todo:
            add possibility of time limit
        """

        while True:
            for obj in obj_list:
                obj.draw()
            self.win.flip()
            key = event.getKeys()
            if len(key)>0:
                if key[0] in responses:
                    return key[0]
            event.clearEvents()

    def initTrialLog(self):
        """
        A more specific log for only saving necessary
        trial by trial information
        """
        print('init trial log')
        self.trial_log_name = f'results/{self.subject_id}_task-'\
                              f'{self.experiment_name}_ses-{self.session:02d}_'\
                              f'run-{self.run:02d}_events.tsv'

        # create folder
        if not os.path.exists('results'):
            os.mkdir('results')

        # create log file
        header = ['Subject', 'TrialType', 'Session', 'Block', 'Trial', 'T1',
                  'T2', 'T1menu', 'T2menu', 'T1rest', 'T2resp',
                  'T1RT', 'T2RT', 'T1hit', 'T2hit']
        with open(self.trial_log_name, 'w') as f:
            f.write('\t'.join(header) + '\n')

    def updateTrialLog(self, tp):
        """
        Updates the trial log used
        """
        trial_info = [self.subject_id, tp['trial type'], self.session,
                      self.block, self.trial, tp['T1'], tp['T2'],
                      tp['T1 options'], tp['T2 options'], self.t1_response,
                      self.t2_response, self.t1_rt, self.t2_rt,
                      tp['t1_hit'], tp['t2_hit']]
        trial_info = [str(x) for x in trial_info]
        with open(self.trial_log_name, 'a') as f:
            f.write('\t'.join(trial_info) + '\n')

    def progressBar(self):
        """
        Todo:
            Make progress bar
        """
        pass

    def runTrial(self, tp):
        """
        Parameters
            tp: dict
                contains fields for the following:
                    trial_sequence (list of drawable objects)
                    fixation time (in secs)
                    imgdur (in secs)
                    SOA (in secs)
                    T1 (int/str)
                    T2 (int/str)
                    T1 options (list of options for the menu)
                    T2 options (list of options for the menu)
                    T1 menu (list of drawable object)
                    T2 menu (list of drawable object)
                    T1 responses (list of keys)
                    T2 responses (list of keys)
                    T1 correct respons (str)
                    T2 correct respons (str)
        Todo:
            Make sure timing is correct depending on refresh rate
        """
        #start = self.block_start.getTime()
        trial_start = core.Clock()

        # log trial start
        self.log(f'Start of trial - {self.trial} - block - {self.block}  - '\
                 f'run start - {self.run_start.getTime()} - '\
                 f'block start - {self.block_start.getTime()}')

        # show fixation
        fixation = visual.GratingStim(win=self.win, size=0.4, pos=[0,0], sf=0, rgb=-1)
        fixation.draw()
        self.win.flip()
        core.wait(tp['fixation time'])

        # begin RSVP
        for i, im in enumerate(tp['trial sequence']):
            im.draw()
            self.win.flip()
            self.log(f'RSVP - {im.name} - trial - {self.trial} - block - '\
                     f'{self.block}  - trial start - {trial_start.getTime()}'\
                     f' - block start - {self.block_start.getTime()} - '\
                     f'run start - {self.run_start.getTime()}')
            core.wait(tp['imgdur'])
            self.win.flip()
            core.wait(tp['SOA'])

        # fixation before menu
        fixation.draw()
        self.win.flip()
        core.wait(0.5)

        # draw menu
        timer = core.Clock()
        self.log(f'T1 menu - {self.subject_id} - {self.trial} -  '\
                 f'{self.block} - {self.block_start.getTime()} - '\
                 f'{trial_start.getTime()}')
        self.t1_response = self.drawAndWait(tp['T1 menu'], responses=tp['T1 responses'])
        self.t1_rt = timer.getTime()

        timer = core.Clock()
        self.log(f'T2 menu - {self.subject_id} - {self.trial} -  '\
                 f'{self.block} - {self.block_start.getTime()} - '\
                 f'{trial_start.getTime()}')
        self.t2_response = self.drawAndWait(tp['T2 menu'], responses=tp['T2 responses'])
        self.t2_rt = timer.getTime()

        tp['t1_hit'] = tp['T1 correct response'] == self.t1_response
        tp['t2_hit'] = tp['T2 correct response'] == self.t2_response

        # save trial data
        self.updateTrialLog(tp)

        self.log(f'End of trial - {self.trial} - block - {self.block}  - '\
                 f'run start - {self.run_start.getTime()} - '\
                 f'block start - {self.block_start.getTime()}')


    def addTrial(self, tp):
        self.trials.append(tp)

    def clearTrials(self):
        self.trials = []