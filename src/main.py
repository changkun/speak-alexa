from __future__ import print_function

import sys
import random
from flask import Flask
from flask_ask import Ask, statement, question, session

from helper import Helper
from sounds import Sounds
from utils import Utils

import random
from datetime import datetime

random.seed(datetime.now())

app = Flask(__name__)
ask = Ask(app, "/alexa")

utils = Utils()

# read only
ex_iv = utils.fetch_all_insert_verb_exercise()
ex_ram = utils.fetch_all_repeat_sentence()
ram_max = insert_max = 4

"""
All session state:

+ session.attributes['state']:
    - 'general'
    - 'recover'
    - 'insertVerbsExercise'
    - 'repeatAfterMeExercise'
+ session.attributes['tutorial']:
    - 'true'
    - 'false'
+ session.attributes['YesLeadsTo']:
    - 'exerciseRound'
+ session.attributes['NoLeadsTo']
    - 'help'
+ session.attributes['HelpLeadsTo']:
    - 'general'
    - 'insertVerbsExercise'
    - 'repeatAfterMeExercise'
    - 'simple present'
    - 'simple past'
    - 'will future'
    - 'present perfect'
+ session.attributes['sentence']
+ session.attributes['task']
+ session.attributes['solution_verbform']
+ session.attributes['solution_sentence']
"""

#====================================
# Start and Stop
#====================================


@ask.launch
def start_skill():
    print('#### start_skill', file=sys.stderr)

    session.attributes['NoLeadsTo'] = 'help'
    userid = session.user.userId
    utils.initial_cache_for(userid)

    if utils.is_new_user(userid):
        # new user first time use
        session.attributes['state'] = 'insertVerbsExercise'
        session.attributes['tutorial'] = 'true'
        session.attributes['HelpLeadsTo'] = 'insertVerbsExercise'
        insert_verbs_exercise = exercise_round(returnStringOnly=True)

        return question(Helper.wrap(Helper.welcome_msg(first=True) + insert_verbs_exercise)) \
            .reprompt(Helper.reprompt())
    else:
        # old user second time use
        session.attributes['tutorial'] = 'false'
        progress = utils.fetch_status(userid)
        current_ex = progress['status']['current_exercise']

        if current_ex == None:
            # no former session to recover
            session.attributes['state'] = 'general'
            session.attributes['HelpLeadsTo'] = 'general'
            return question(Helper.welcome_msg() +
                            Helper.ex_ask_msg()).reprompt(Helper.reprompt())
        else:
            # found former session to recover
            session.attributes['state'] = 'recover'
            session.attributes['HelpLeadsTo'] = 'general'
            return question(Helper.welcome_msg() + Helper.recover_msg(current_ex)).reprompt(Helper.reprompt())


@ask.intent("AMAZON.StopIntent")
def close_skill():
    print('#### close_skill', file=sys.stderr)
    userid = session.user.userId
    if session.attributes['tutorial'] == 'false':
        # tutorial finished
        utils.store_status(userid)
        count, rank = utils.compute_rank(userid)
        utils.clear_cache_for(userid)
        return statement(Helper.stop_msg(tutorial=True, count=count, rank=rank))
    else:
        # tutorial not finished, user status will not be stored into database
        utils.clear_cache_for(userid)
        return statement(Helper.stop_msg())


@ask.session_ended
def session_ended():
    print('#### session_ended', file=sys.stderr)
    userid = session.user.userId
    # tutorial not finished, user status will not be stored into database
    if session.attributes['tutorial'] == 'false':
        utils.store_status(userid)
    utils.clear_cache_for(userid)
    return '{}', 200

#====================================
# Picking an exercise
#====================================


@ask.intent("InsertVerbsIntent")
def insertVerbsIntent():
    print('#### InsertVerbsIntent', file=sys.stderr)
    utils.reset_ram_and_insert_ctr(session.user.userId)
    if(session.attributes['tutorial'] == 'true'):
        # only for tutorial session, appear once
        sentence = ram_exercise_round(returnStringOnly=True)
        if(session.attributes['state'] == 'general'):
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            return question(Helper.round_msg(sentence, prefix=True))
        elif(session.attributes['state'] == 'insertVerbsExercise'):
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            return question(Helper.wrap(
                Helper.correction_msg(
                    session.attributes['solution_sentence']) + Helper.round_msg(sentence)
            )).reprompt(Helper.reprompt())
        # pronunciation intent selection
        elif(session.attributes['state'] == 'repeatAfterMeExercise'):
            session.attributes['state'] = 'general'
            session.attributes['tutorial'] = 'false'
            session.attributes['HelpLeadsTo'] = 'general'
            return question(Helper.wrap(
                Helper.correction_msg(session.attributes['task']) +
                Helper.tutorial_msg(step=0)
            )).reprompt(Helper.reprompt())
    else:
        # general situation, old user always go to this branch
        if(session.attributes['state'] == 'general'):
            session.attributes['HelpLeadsTo'] = 'insertVerbsExercise'
            session.attributes['state'] = 'insertVerbsExercise'
            return exercise_round()
        elif(session.attributes['state'] == 'insertVerbsExercise'):
            next_exercise = exercise_round(returnStringOnly=True)
            return question(Helper.wrap(
                Helper.correction_msg(session.attributes['solution_sentence']) +
                'Now let\'s do the pronunciation exercise. <break time="1s"/>' +
                next_exercise
            )).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'repeatAfterMeExercise'):
            ram_next_exercise = ram_exercise_round(returnStringOnly=True)
            return question(Helper.wrap(
                Helper.correction_msg(session.attributes['task']) +
                'Here comes the next exercise <break time="1s"/>' +
                ram_next_exercise
            )).reprompt(Helper.reprompt())


@ask.intent("PronunciationIntent")
def pronunciationIntent():
    print('#### PronunciationIntent', file=sys.stderr)
    utils.reset_ram_and_insert_ctr(session.user.userId)
    if(session.attributes['tutorial'] == 'true'):
        sentence = ram_exercise_round(returnStringOnly=True)
        if(session.attributes['state'] == 'general'):
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            return question(Helper.round_msg(sentence, prefix=True)).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'insertVerbsExercise'):
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            return question(Helper.wrap(Helper.correction_msg(
                session.attributes['solution_sentence']) + Helper.round_msg(sentence)
            )).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'repeatAfterMeExercise'):
            print('#### Pronunciation Intent Selection', file=sys.stderr)
            session.attributes['state'] = 'general'
            session.attributes['tutorial'] = 'false'
            session.attributes['HelpLeadsTo'] = 'general'
            return question(Helper.wrap(Helper.correction_msg(
                session.attributes['task']) +
                Helper.tutorial_msg(step=0)
            )).reprompt(Helper.reprompt())
    else:
        if(session.attributes['state'] == 'general'):
            sentence = ram_exercise_round(returnStringOnly=True)
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            return question(Helper.round_msg(sentence, prefix=True)).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'insertVerbsExercise'):
            next_exercise = exercise_round(returnStringOnly=True)
            return question(Helper.wrap(Helper.correction_msg(
                session.attributes['solution_sentence']) +
                next_exercise
            )).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'repeatAfterMeExercise'):
            ram_next_exercise = ram_exercise_round(returnStringOnly=True)
            return question(Helper.wrap(Helper.correction_msg(
                session.attributes['task']) +
                "Here comes the next exercise <break time=\"1s\"/>" +
                ram_next_exercise
            )).reprompt(Helper.reprompt())


#====================================
# Yes and no
#====================================

@ask.intent("YesIntent")
def yes_intent():
    print('#### YesIntent', file=sys.stderr)
    # yes intent for state recovering (recover state)
    if session.attributes['state'] == 'recover':
        progress = utils.fetch_status(session.user.userId)
        if progress['status']['current_exercise'] == 'grammar':
            session.attributes['HelpLeadsTo'] = 'insertVerbsExercise'
            session.attributes['state'] = 'insertVerbsExercise'
            return exercise_round()
        else:
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            session.attributes['state'] = 'repeatAfterMeExercise'
            return ram_exercise_round()
    # yes intent for going back to general intent
    elif session.attributes['state'] == 'general':
        return question(Helper.welcome_msg() + Helper.ex_ask_msg()).reprompt(Helper.reprompt())
    # yes intent for going back to invertverbs intent
    elif session.attributes['state'] == 'insertVerbsExercise':
        # help doesn't lead to insertverbs
        if(session.attributes['HelpLeadsTo'] != 'insertVerbsExercise'):
            return question(Helper.wrap(session.attributes['task'])).reprompt(Helper.reprompt())
        # not in session attributes or yes leads to exerciseround
        if (('YesLeadsTo' not in session.attributes) or (session.attributes['YesLeadsTo'] == 'exerciseRound')):
            return exercise_round()
    # yes intent for going back to repeat after me intent
    elif session.attributes['state'] == 'repeatAfterMeExercise':
        if (session.attributes['YesLeadsTo'] == 'exerciseRound'):
            return question(Helper.wrap(session.attributes['task'])).reprompt(Helper.reprompt())
        else:
            return ram_exercise_round()  # going to ram


@ask.intent("NoIntent")
def no_intent():
    print('#### NoIntent', file=sys.stderr)

    # no intent for state recovering (do not recover)
    if (session.attributes['state'] == 'recover'):
        session.attributes['state'] = 'general'
        session.attributes['HelpLeadsTo'] = 'general'
        return question(Helper.ex_ask_msg(prefix=True)).reprompt(Helper.reprompt())
    # no intent for explaining help again
    if (session.attributes['NoLeadsTo'] == 'help'):
        response = help_intent()
        return response


#====================================
# Exercise Insert Verbs
#====================================


def load_new_exercise_data():
    ex_obj = random.choice(ex_iv)
    session.attributes['solution_verbform'] = ex_obj['answer']
    session.attributes['solution_sentence'] = "%s %s %s" % (
        ex_obj['sentence_front'], ex_obj['answer'], ex_obj['sentence_back']
    )
    session.attributes['task'] = "%s, %s, %s" % (
        ex_obj['verb'], ex_obj['tense'],
        ex_obj['sentence_front'] + Sounds.beep() + ex_obj['sentence_back']
    )
    session.attributes['HelpLeadsTo'] = ex_obj['tense']


def exercise_round(returnStringOnly=False):
    print('#### exercise_round', file=sys.stderr)
    userid = session.user.userId
    if session.attributes['tutorial'] == 'true':
        utils.set_current_ex_for(userid)
    else:
        utils.set_current_ex_for(userid, 'grammar')

    load_new_exercise_data()

    if returnStringOnly:
        if(session.attributes['tutorial'] == 'true'):
            return Helper.tutorial_msg(step=1) + session.attributes['task']
        else:
            return session.attributes['task']
    else:
        return question(Helper.wrap(
            Helper.start_msg('INSERT_VERBS', session.attributes['task'])
        )).reprompt(Helper.reprompt(more=True))


@ask.intent("AnswerIntentInsert", convert={'verbform': str})
def check_answer(verbform):
    print('#### AnswerIntentInsert', file=sys.stderr)
    solution_verbform = session.attributes['solution_verbform']
    solution_sentence = session.attributes['solution_sentence']
    print('reco verbform: ' + verbform, file=sys.stderr)
    print('true verbform: ' + solution_verbform, file=sys.stderr)
    print('correct sentence: ' + solution_sentence, file=sys.stderr)

    next_exercise = exercise_round(returnStringOnly=True)
    if(session.attributes['tutorial'] == 'true'):
        session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
        session.attributes['state'] = 'repeatAfterMeExercise'
        sentence = ram_exercise_round(returnStringOnly=True)
        ram_tutorial_sentence = Helper.round_msg(sentence)
        session.attributes['sentence'] = sentence
        if(verbform == solution_verbform):
            return question(Helper.wrap(
                'Very good! ' + solution_sentence +
                Helper.tutorial_msg(step=2) + ram_tutorial_sentence
            )).reprompt(Helper.reprompt())
        else:
            return question(Helper.wrap(
                'Sorry, your answer: ' + verbform + ', was wrong. Correct answer is ' +
                solution_sentence + Helper.tutorial_msg(step=2) +
                ram_tutorial_sentence
            )).reprompt(Helper.reprompt())
    else:
        if (verbform == solution_verbform):
            utils.increase_progress_count(session.user.userId)
            utils.increase_insert_ctr(session.user.userId)
            if utils.get_insert_ctr(session.user.userId) < insert_max:
                return question(Helper.wrap(
                    Helper.check_msg(True, solution_sentence, next_exercise)
                )).reprompt(Helper.reprompt())
            else:
                session.attributes['state'] = 'general'
                session.attributes['HelpLeadsTo'] = 'general'
                utils.set_current_ex_for(session.user.userId)
                return question(Helper.wrap(
                    Helper.check_msg(True, solution_sentence,
                                     None, celebrate=True)
                )).reprompt(Helper.reprompt())
        else:
            return question(Helper.wrap(
                Helper.check_msg(False, solution_sentence, next_exercise)
            )).reprompt(Helper.reprompt())


#====================================
# Exercise Repeat after me
#====================================


def ram_exercise_round(returnStringOnly=False):
    print('#### ram_exercise_round', file=sys.stderr)
    if session.attributes['tutorial'] == 'true':
        utils.set_current_ex_for(session.user.userId)
    else:
        utils.set_current_ex_for(session.user.userId, 'pronunciation')

    session.attributes['task'] = random.choice(ex_ram)
    if returnStringOnly:
        return session.attributes['task']
    else:
        return question(Helper.wrap(
            Helper.start_msg('REPEAT_AFTER_ME', session.attributes['task'])
        )).reprompt(Helper.reprompt(more=True))


@ask.intent("AnswerIntentRepeat", convert={'answerSentence': str})
def ram_check_answer(answerSentence):
    if(session.attributes['tutorial'] == 'true'):
        if (session.attributes['state'] == 'repeatAfterMeExercise'):
            print('#### check_answer_repeat in tutorial branch', file=sys.stderr)
            solution = session.attributes['task']
            next_exercise = ram_exercise_round(returnStringOnly=True)
            print('recognized answer: ' + str(answerSentence), file=sys.stderr)
            print('correct answer:    ' + solution, file=sys.stderr)
            session.attributes['tutorial'] = 'false'
            session.attributes['state'] = 'general'
            session.attributes['HelpLeadsTo'] = 'general'

            if (solution == str(answerSentence)):
                return question(Helper.wrap(
                    'Very good! ' + solution +
                    '<break time="1s"/>' + Helper.tutorial_msg(step=0)
                )).reprompt(Helper.reprompt())
            else:
                return question(Helper.wrap(
                    'I think this was wrong. Correct is ' + solution +
                    '<break time="1s"/>' + Helper.tutorial_msg(step=0)
                )).reprompt(Helper.reprompt())

        elif (session.attributes['state'] == 'insertVerbsExercise'):
            print('#### check_answer_repeat in tutorial branch', file=sys.stderr)
            print('#### User landed in wrong intent', file=sys.stderr)
            sentence = ram_exercise_round(returnStringOnly=True)
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            return question(Helper.wrap(
                'I think this was wrong. Correct answer is ' +
                session.attributes['solution_sentence'] +
                '<break time="1s"/>' + Helper.round_msg(sentence)
            )).reprompt(Helper.reprompt())
    else:
        if (session.attributes['state'] == 'repeatAfterMeExercise'):
            print('#### check_answer_repeat', file=sys.stderr)
            solution = session.attributes['task']
            next_exercise = ram_exercise_round(returnStringOnly=True)
            print('recognized answer: ' + str(answerSentence), file=sys.stderr)
            print('correct answer:    ' + solution, file=sys.stderr)

            if (solution == str(answerSentence)):
                utils.increase_progress_count(session.user.userId)
                utils.increase_ram_ctr(session.user.userId)
                if utils.get_ram_ctr(session.user.userId) < ram_max:
                    return question(Helper.wrap(
                        Helper.check_msg(True, solution, next_exercise)
                    )).reprompt(Helper.reprompt())
                else:
                    session.attributes['state'] = 'general'
                    session.attributes['HelpLeadsTo'] = 'general'
                    utils.set_current_ex_for(session.user.userId)
                    return question(Helper.wrap(
                        Helper.check_msg(True, solution, None, celebrate=True)
                    )).reprompt(Helper.reprompt())
            else:
                return question(Helper.wrap(
                    Helper.check_msg(False, solution, next_exercise)
                )).reprompt(Helper.reprompt())

        elif (session.attributes['state'] == 'insertVerbsExercise'):
            print('#### check_answer_repeat', file=sys.stderr)
            print('#### User landed in wrong intent', file=sys.stderr)
            correct_answer = session.attributes['solution_sentence']
            next_exercise = exercise_round(returnStringOnly=True)
            return question(Helper.wrap(
                Helper.check_msg(False, correct_answer, next_exercise)
            )).reprompt(Helper.reprompt())


#====================================
# Repeat, Help etc.
#====================================
@ask.intent("AMAZON.HelpIntent")
def help_intent():
    session.attributes['NoLeadsTo'] = 'help'
    session.attributes['YesLeadsTo'] = 'exerciseRound'
    return question(Helper.help_msg(session.attributes['HelpLeadsTo'])).reprompt(Helper.reprompt())


@ask.intent("RepeatIntent")
def repeat_intent():
    return question(Helper.wrap('<emphasis level="strong">' + session.attributes['task'] + '</emphasis>')).reprompt(Helper.reprompt())


@ask.intent("NextIntent")
def another_sample():
    print('#### another sample intent', file=sys.stderr)
    if(session.attributes['tutorial'] == 'true'):
        print('#### Next Intent Tutorial', file=sys.stderr)
        if(session.attributes['state'] == 'general'):
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            session.attributes['state'] = 'repeatAfterMeExercise'
            print('#### exercise_round_repeat', file=sys.stderr)
            sentence = ram_exercise_round(returnStringOnly=True)
            session.attributes['sentence'] = sentence
            return question(Helper.round_msg(sentence, prefix=True))
        elif(session.attributes['state'] == 'insertVerbsExercise'):
            return question(Helper.wrap(
                Helper.restriction_msg() + session.attributes['task']
            )).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'repeatAfterMeExercise'):
            return question(Helper.wrap(
                Helper.restriction_msg() + session.attributes['task']
            )).reprompt(Helper.reprompt())
    else:
        next_exercise = None
        if session.attributes['state'] == 'insertVerbsExercise':
            next_exercise = exercise_round(returnStringOnly=True)
        else:
            next_exercise = ram_exercise_round(returnStringOnly=True)
        return question(Helper.wrap(
            "Ok, let\'s just go on with the next exercise.<break time=\"1s\"/>" + next_exercise
        )).reprompt(Helper.reprompt())


@ask.intent("SwitchIntent")
def switch_intent():
    print('### switch intent')
    if(session.attributes['tutorial'] == 'true'):
        if(session.attributes['state'] == 'general'):
            sentence = ram_exercise_round(returnStringOnly=True)
            session.attributes['state'] = 'repeatAfterMeExercise'
            session.attributes['sentence'] = sentence
            session.attributes['HelpLeadsTo'] = 'repeatAfterMeExercise'
            return question(Helper.round_msg(sentence, prefix=True)).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'insertVerbsExercise'):
            return question(Helper.wrap(
                Helper.restriction_msg() + session.attributes['task']
            )).reprompt(Helper.reprompt())
        elif(session.attributes['state'] == 'repeatAfterMeExercise'):
            return question(Helper.wrap(
                Helper.restriction_msg() + session.attributes['task']
            )).reprompt(Helper.reprompt())
    else:
        session.attributes['state'] = 'general'
        session.attributes['HelpLeadsTo'] = 'general'
        session.attributes['YesLeadsTo'] = 'exerciseRound'
        return question(Helper.ex_ask_msg(prefix=True)).reprompt(Helper.reprompt())


if __name__ == '__main__':
    app.run(debug=True, port=5005)
