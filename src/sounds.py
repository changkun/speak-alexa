import random


class Sounds:
    def __init__(self):
        return

    @staticmethod
    def celebration():
        return random.choice([
            ' <audio src="https://s3-eu-west-1.amazonaws.com/magiclingua-alexa/FinalMinutesPresidentObamaYesWeCan.mp3"/> ',
            ' <audio src="https://s3-eu-west-1.amazonaws.com/magiclingua-alexa/Yoda_PowerfulYouHaveBecome.mp3"/> ',
            ' <audio src="https://s3-eu-west-1.amazonaws.com/magiclingua-alexa/YouDidIt_Congratulations.mp3"/> '
        ])

    @staticmethod
    def beep():
        return ' <audio src="https://s3-eu-west-1.amazonaws.com/magiclingua-alexa/beep.mp3"/> '
