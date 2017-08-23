from sounds import Sounds


class Helper:
    @staticmethod
    def start_msg(ex_type, exercise):
        if ex_type == 'INSERT_VERBS':
            return 'Okay! Let\'s do the "insert verbs" exercise. Say help, to get an explanation of the exercise. Here comes the first exercise: ' + exercise
        elif ex_type == 'REPEAT_AFTER_ME':
            return 'Okay! Let\'s do the "repeat after me" exercise. Say help, to get an explanation of the exercise. Here comes the first exercise: ' + exercise
        else:
            return ''

    @staticmethod
    def tutorial_check_msg(correct, solution, next_ex):
        if correct:
            return
        else:
            return

    @staticmethod
    def check_msg(correct, solution, next_ex, celebrate=False):
        if correct:
            if celebrate:
                return 'Very good! ' + solution + '<break time="1s"/>' + Sounds.celebration() + '<break time="1s"/>' + Helper.congrats() + Helper.ex_ask_msg()
            else:
                return 'Very good! ' + solution + '. Here comes the next exercise: <break time="1s"/> ' + next_ex
        else:
            return 'I think this was wrong. Correct answer is ' + solution + '. Here comes the next exercise:  <break time="1s"/>' + next_ex

    @staticmethod
    def restriction_msg():
        return 'Switching is only available after you have completed the tutorial. Let\'s try again: <break time="1s"/>'

    @staticmethod
    def tutorial_msg(step=0):
        if step == 0:
            return "You've finished our small tutorial. What would you like to do now? Do the grammar or the pronunciation exercise?"
        elif step == 1:
            return 'Welcome to the grammar exercise. I will give you an infinitive and the tense in which it should be used. \
            The ' + Sounds.beep() + ' beep sound shows you where the correct verbform should go. \
            I will do the first one: <break time="1s" /> To go <break time="1s"/> \
            simple past <break time="1s"/> I ' + Sounds.beep() + ' to the park. \
            <break time="1s"/> The correct answer would be <break time="1s"/> I walked in the park. <break time="1s"/>  Now it is your turn! '
        elif step == 2:
            return '<break time="1s"/> Now let\'s move on to the pronunciation exercise<break time="1s"/>'
        else:
            return ''

    @staticmethod
    def wrap(string):
        return '<speak>' + string + '</speak>'

    @staticmethod
    def reprompt(more=False):
        if more:
            return " I didn't get that. Say it again! "
        else:
            return " I didn't get that. "

    @staticmethod
    def stop_msg(tutorial=False, count=0, rank=0.0):
        if tutorial:
            return ' You finished %d exercise this time, and beat %.2f percent \
                of total user cross the universe. That\'s all. See you next time. ' % (count, rank * 100)
        else:
            return " It\'s so sad to hear you want to stop, you haven't even finished the tutorial yet, hope I could help you next time. Good bye. "

    @staticmethod
    def recover_msg(ex_type):
        return ' I found out you left the %s exercise last time, shall we keep continue on the %s exercise? yes or no? ' \
            % (ex_type, ex_type)

    @staticmethod
    def round_msg(sentence, prefix=False):
        if prefix:
            return "Okay! Please repeat the sentences you hear. If you need help just say help. Let's start: " + sentence
        else:
            return "Please repeat the sentences you hear. If you need help just say help. Let's start:  " + sentence

    @staticmethod
    def correction_msg(solution):
        return 'I think this was wrong. Correct answer is <break time="1s"/>' + solution + '.<break time="1s"/>'

    @staticmethod
    def ex_ask_msg(prefix=False):
        if prefix:
            return ' OK, then what do you want to do? grammar or pronunciation? '
        else:
            return ' What do you want to do? grammar or pronunciation? '

    @staticmethod
    def help_msg(session_attr):
        if(session_attr == 'general'):
            return Helper.wrap(Helper.general_msg())

        elif(session_attr == 'insertVerbsExercise'):
            return Helper.wrap(Helper.exercise('INSERT_VERBS'))
        elif(session_attr == 'repeatAfterMeExercise'):
            return Helper.wrap(Helper.exercise('REPEAT_AFTER_ME'))

        elif(session_attr == 'simple present'):
            return Helper.wrap(Helper.grammar('SIMPLE_PRESENT'))
        elif(session_attr == 'simple past'):
            return Helper.wrap(Helper.grammar('SIMPLE_PAST'))
        elif(session_attr == 'will future'):
            return Helper.wrap(Helper.grammar('WILL_FUTURE'))
        elif(session_attr == 'present perfect'):
            return Helper.wrap(Helper.grammar('PRESENT_PERFECT'))

    @staticmethod
    def general_msg():
        return '''
                In this skill you can navigate using several commands. 
                If you want to get help regarding the current context just say Help. 
                If you want to hear an exercise again say repeat. 
                For switching exercises you can say switch exercises and if you want to skip an exercise say next one. 
                You got that?
        '''

    @staticmethod
    def welcome_msg(first=False):
        if first:
            return '''
                Hello there, I am your magic teacher! This is your first time using this skill. 
                We will start by doing two small exercises together. 
            '''
        else:
            return 'Welcome back! This is MagicLingua, I am your magic teacher!'

    @staticmethod
    def congrats():
        return 'Congratulations! You gave enough correct answers for now. \
                Let\'s do something else.'

    @staticmethod
    def exercise(ex_type):
        if ex_type == 'INSERT_VERBS':
            return '\
                    You are doing an exercise where you have to say the correct time form.\
                    Here is an example: To shine. will future.\
                    The sun' + Sounds.beep() + 'tomorrow.\
                    The correct answer would be: The sun will shine tomorrow. You got that?\
            '
        elif ex_type == 'REPEAT_AFTER_ME':
            return 'In this exercise you just have to repeat the whole sentence. You got that?'
        else:
            return 'Sorry, I can not handle this help'

    @staticmethod
    def grammar(grammar_type):
        if grammar_type == 'SIMPLE_PAST':
            return '''
                    Using the simple past is easy. Unless the Verb is irregular, 
                    simply add 
                        <break time="200ms"/>
                    e
                        <break time="200ms"/>
                    d
                        <break time="200ms"/> 
                    to the end of a verb. 
                    You got that?
            '''
        elif grammar_type == 'SIMPLE_PRESENT':
            return '''
                    When you use simple present you just have to follow one rule: 
                    Add an 
                        <break time="200ms"/>s<break time="200ms"/> 
                    to the end of a verb if the pronoun is 
                        <break time="200ms"/> he <break time="200ms"/> she <break time="200ms"/> 
                    or 
                        <break time="200ms"/> it. 
                    You got that?
            '''
        elif grammar_type == 'WILL_FUTURE':
            return '''
                    You form the will future by adding 
                        <break time="200ms"/> 
                    will 
                        <break time="200ms"/>
                    infront of your normal verb. 
                    You got that?
            '''
        elif grammar_type == 'PRESENT_PERFECT':
            return '''
                The present perfect of any verb is composed of two elements:
                the appropriate form of the auxiliary verb to have (present tense),
                plus the past participle of the main verb. You got that?
            '''
        else:
            return 'Sorry, I can not handle this help'
