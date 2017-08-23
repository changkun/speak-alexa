from utils import Utils

# testing code
# create utils object
print('start db init...')

utils = Utils()
utils.destroy_db()

# insert to mongodb
utils.store_status('amzn1.ask.account.XXX')
utils.store_status('amzn1.ask.account.YYY')
utils.store_status('amzn1.ask.account.ZZZ')
# initial one user
utils.initial_cache_for('amzn1.ask.account.WWW')
# clear one user
utils.clear_cache_for('amzn1.ask.account.XXX')
utils.store_status('amzn1.ask.account.WWW')
# user judgement
assert True == utils.is_new_user('amzn1.ask.account.AAA')
assert False == utils.is_new_user('amzn1.ask.account.WWW')
# compute rank
assert (2, 0.25) == utils.compute_rank('amzn1.ask.account.YYY')

# initial pronunciation sentences to database
pron_exs = [{
    'level': '1',
    'sentence': 'the dog was flying to the moon'
}, {
    'level': '1',
    'sentence': 'john went to the supermarket'
}, {
    'level': '1',
    'sentence': 'the cat sat on the mat'
}, {
    'level': '3',
    'sentence': 'i scream you scream we all scream for icecream'
}, {
    'level': '5',
    'sentence': 'i saw susie sitting in a shoe shine shop'
}, {
    'level': '5',
    'sentence': 'how can a clam cram in a clean cream can'
}, {
    'level': '5',
    'sentence': 'roberta ran rings around the roman ruins'
}]
for ex in pron_exs:
    utils.insert_pronunciation_ex_with(ex)


insertv_exs = [{
    'level': 1,
    'verb': 'to go',
    'tense': 'simple past',
    'sentence_front': 'I',
    'sentence_back':  'to the park',
    'answer': 'went'
},
    {
    'level': 1,
    'verb': 'to win',
    'tense': 'will future',
    'sentence_front': 'He',
    'sentence_back':  'the match',
    'answer': 'will win'
},
    {
    'level': 1,
    'verb': 'to play',
    'tense': 'simple present',
    'sentence_front': 'Mary',
    'sentence_back':  'tennis',
    'answer': 'plays'
},
    {
    'level': 1,
    'verb': 'to see',
    'tense': 'present perfect',
    'sentence_front': 'You',
    'sentence_back':  'that movie many times',
    'answer': 'have seen'
},
    {
    'level': 1,
    'verb': 'to stay',
    'tense': 'will future',
    'sentence_front': 'He',
    'sentence_back':  'at home',
    'answer': 'will stay'
},
    {
    'level': 1,
    'verb': 'to tell',
    'tense': 'simple past',
    'sentence_front': 'She',
    'sentence_back':  'her friend to come with her',
    'answer': 'told'
},
    {
    'level': 1,
    'verb': 'to meet',
    'tense': 'present perfect',
    'sentence_front': 'I don\'t believe we',
    'sentence_back':  'before',
    'answer': 'have met'
}]
for ex in insertv_exs:
    utils.insert_insert_verb_ex_with(ex)

print('database was just initiated.')
