from __future__ import division
from pymongo import MongoClient


class Utils:
    def __init__(self):
        self._db_user = MongoClient('localhost', 27017)[
            'MagicLingua']['AlexaUser']
        self._db_grammar = MongoClient('localhost', 27017)[
            'MagicLingua']['AlexaInsertVerbs']
        self._db_pronunciation = MongoClient('localhost', 27017)[
            'MagicLingua']['AlexaPronunciation']

        self._cache = {
            'amzn1.ask.account.XXX': {
                '_id': 'amzn1.ask.account.XXX',
                'status': {
                    'current_exercise': 'grmmar',
                    'progress': 2,
                    'ram_ctr': 0,
                    'insert_ctr': 0,
                }
            },
            'amzn1.ask.account.YYY': {
                '_id': 'amzn1.ask.account.YYY',
                'status': {
                    'current_exercise': 'grmmar',
                    'progress': 2,
                    'ram_ctr': 0,
                    'insert_ctr': 0,
                }
            },
            'amzn1.ask.account.ZZZ': {
                '_id': 'amzn1.ask.account.ZZZ',
                'status': {
                    'current_exercise': 'grmmar',
                    'progress': 2,
                    'ram_ctr': 0,
                    'insert_ctr': 0,
                }
            }
        }

    def destroy_db(self):
        """
        WATCH OUT: this method is dangerous
        """
        self._db_user.remove({})
        self._db_grammar.remove({})
        self._db_pronunciation.remove({})

    # user database connection
    def is_new_user(self, userid):
        """
        check a user id is a new user or not
        return status if not and return False if true
        """
        results = self.fetch_status(userid)
        if results:
            return False  # old user
        return True

    def initial_cache_for(self, userid):
        """
        initial cache for a given userid
        """
        self._cache[userid] = {
            '_id': userid,
            'status': {
                'current_exercise': None,
                'progress': 0,
                'ram_ctr': 0,
                'insert_ctr': 0,
            }
        }

    def clear_cache_for(self, userid):
        """
        clear cache for a given userid
        """
        self._cache.pop(userid, 0)

    def fetch_status(self, userid):
        return self._db_user.find_one({'_id': userid})

    def store_status(self, userid):
        """
        store everything from cache to mongodb database
        """
        if userid in self._cache:
            self._db_user.update(
                {'_id': userid}, self._cache[userid], upsert=True)

    def store_all_status(self):
        """
        stores everything from cache
        """
        for userid, item in self._cache:
            self._db_user.update({'_id': item['_id']}, item, upsert=True)

    def set_current_ex_for(self, userid, ex_type=None):
        """
        set current exercise type for userid:
        ex_type: default None, or 'grammar', 'pronunciation' string
        """
        self._cache[userid]['status']['current_exercise'] = ex_type

    def increase_progress_count(self, userid):
        self._cache[userid]['status']['progress'] += 1

    def increase_ram_ctr(self, userid):
        self._cache[userid]['status']['ram_ctr'] += 1

    def increase_insert_ctr(self, userid):
        self._cache[userid]['status']['insert_ctr'] += 1

    def reset_ram_and_insert_ctr(self, userid):
        self._cache[userid]['status']['ram_ctr'] = 0
        self._cache[userid]['status']['insert_ctr'] = 0

    def get_insert_ctr(self, userid):
        return self._cache[userid]['status']['insert_ctr']

    def get_ram_ctr(self, userid):
        return self._cache[userid]['status']['ram_ctr']

    def compute_rank(self, userid):
        """
        given a userid then compute the current progress with all history user
        """
        count = self._db_user.find(
            {'status.progress': {'$lt': self._cache[userid]['status']['progress']}}).count()
        total = self._db_user.find({}).count()

        rank = count / total
        return self._cache[userid]['status']['progress'], rank

    # grammar exercise db connection
    def insert_insert_verb_ex_with(self, ex_obj):
        self._db_grammar.update(ex_obj, ex_obj, upsert=True)

    def fetch_all_insert_verb_exercise(self):
        return list(self._db_grammar.find({}, {'_id': 0}))

    # pronunciation exercise db connection
    def insert_pronunciation_ex_with(self, ex_obj):
        self._db_pronunciation.update(ex_obj, ex_obj, upsert=True)

    def fetch_all_repeat_sentence(self):
        return [item['sentence'] for item in self._db_pronunciation.find({}, {'_id': 0, 'sentence': 1})]
