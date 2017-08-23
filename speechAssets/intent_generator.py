import os
from pymongo import MongoClient


class Generator():
    def __init__(self):
        self.db_gram = MongoClient('localhost', 27017)[
            'MagicLingua']['AlexaInsertVerbs']
        self.db_pron = MongoClient('localhost', 27017)[
            'MagicLingua']['AlexaPronunciation']

    @staticmethod
    def _AnswerIntentInsert_template(first, last):
        return 'AnswerIntentInsert ' + first + ' {verbform} ' + last

    @staticmethod
    def _AnswerIntentRepeat_template(sentence):
        return 'AnswerIntentRepeat {' + sentence + '|answerSentence}'

    def AnswerIntentInsert(self):
        AnswerIntentInsert_list = []
        for item in self.db_gram.find({}):
            AnswerIntentInsert_list.append(
                Generator._AnswerIntentInsert_template(
                    item['sentence_front'], item['sentence_back']
                )
            )
        return AnswerIntentInsert_list

    def AnswerIntentRepeat(self):
        AnswerIntentRepeat_list = []
        for item in self.db_pron.find({}):
            AnswerIntentRepeat_list.append(
                Generator._AnswerIntentRepeat_template(item['sentence'])
            )
        return AnswerIntentRepeat_list


def main():
    generator = Generator()
    utterances = []
    utterances += generator.AnswerIntentInsert()
    utterances += generator.AnswerIntentRepeat()
    file_path = os.path.dirname(os.path.abspath(
        __file__)) + '/utterances_answers.txt'
    with open(file_path, 'w') as f:
        for utterance in utterances:
            f.write(utterance + '\n')


if __name__ == '__main__':
    main()
