#!/bin/python
import codecs
import nltk

def preprocess_corpus(train_sents):
    global college
    college = set(line.strip() for line in codecs.open('./data/lexicon/education.university', 'r', 'utf-8'))

    global first_name
    global last_name
    first_name = set(line.strip() for line in codecs.open('./data/lexicon/firstname.5k', 'r', 'utf-8'))
    last_name = set(line.strip() for line in codecs.open('./data/lexicon/lastname.5000', 'r', 'utf-8'))

    global stop
    stop = set(line.strip() for line in codecs.open('./data/lexicon/english.stop', 'r', 'utf-8'))

    global loc
    location = set(line.strip() for line in codecs.open('./data/lexicon/location', 'r', 'utf-8'))
    country = set(line.strip() for line in codecs.open('./data/lexicon/location.country', 'r', 'utf-8'))
    venues = set(line.strip() for line in codecs.open('./data/lexicon/venues', 'r', 'utf-8'))
    loc=location|country|venues

    global tv
    network =  set(line.strip() for line in codecs.open('./data/lexicon/tv.tv_network', 'r', 'utf-8'))
    program =  set(line.strip() for line in codecs.open('./data/lexicon/tv.tv_program', 'r', 'utf-8'))
    tv =  network|program

    global sports
    league = set(line.strip() for line in codecs.open('./data/lexicon/sports.sports_league', 'r', 'utf-8'))
    team =  set(line.strip() for line in codecs.open('./data/lexicon/sports.sports_team', 'r', 'utf-8'))
    sports = league|team
    '''
    global company
    venture =set(line.strip() for line in codecs.open('./data/lexicon/venture_capital.venture_funded_company', 'r', 'utf-8'))
    brand = set(line.strip() for line in codecs.open('./data/lexicon/business.brand', 'r', 'utf-8'))
    company = venture|brand
    '''


def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")

    if word in college:
        ftrs.append("IS_COLLEGE")

    if word.upper() in first_name:
        ftrs.append("FIRST_NAME")
    elif word.lower() in last_name:
        ftrs.append("LAST_NAME")

    if word.lower() in stop:
        ftrs.append("IS_STOP")
    if word in loc:
        ftrs.append("IS_LOCATION")
    '''
    if word in company:
        ftrs.append("IS_COMPANY")
    '''
    if word in tv:
        ftrs.append("IS_TV")
    if word in sports:
        ftrs.append("IS_SPORTS")
    # previous/next word feats


    w = nltk.word_tokenize(word)
    l = nltk.pos_tag(w)
    #print l
    if (len(l)>0):
     ftrs.append("IS_"+str(l[0][1]))

    if 'http' in word or '.com' in word:
        ftrs.append("URL")

    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i - 1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        '''
        if i > 1:
            for pf in token2features(sent,i - 2,add_neighs = False):
                ftrs.append("BEFOREPREV_"+pf)
        '''
        if i < len(sent)-1:
            for pf in token2features(sent, i + 1, add_neighs = False):
                ftrs.append("NEXT_" + pf)
        '''
        if i < len(sent) - 2:
            for pf in token2features(sent, i + 2, add_neighs=False):
                ftrs.append("AFTERNEXT_" + pf)
        '''
    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love","happy","food","run" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
