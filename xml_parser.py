'''
http://excess.org/article/2013/02/itergen2/
'''

from coroutine import coroutine


@coroutine
def tag_filter():
    """
    coroutine accepting characters and yielding True when the character
    passed is an ordinary char or False when it is part of an xml tag.
    """
    ordinary = None
    while True:
        char = yield ordinary
        if char != '<':
            ordinary = True
            continue
        ordinary = False

        # char == < ... grab next char
        while ordinary == False:
            char = yield False
            if char != '>':
                ordinary = False
                continue
            break


def test_tag_filter1(data):
    tf = tag_filter()

    def goo(char):
        return {True:char, False:'_'}[tf.send(char)] 

    globals().update(locals())
    result = ''.join(goo(char) for char in data)
#    assert result == alt1
    return result



def xml_tokenizer(data):
    """
    >>> xml_tokenizer('boo<foo>barf</foo bah><doo/ >boo')
    ['', 'boo', '<foo>', 'barf', '</foo bah>', '<doo/ >', 'boo']
    """

    tf = tag_filter()

    def classify(char):
        return tf.send(char)
    
    (prev, result, tmp) = None, [], []
    for char in data:
        res = classify(char) 
        if res != prev or (prev==False and char=='<') :
            result.append(''.join(tmp)) 
            tmp = [char]
            prev = res
        else:
            tmp.append(char)
    result.append(''.join(tmp)) 
    return result[1:]







data = '<>foo <bat bot >bah da<dt>qyp</dt>  </bat> <br/><br/ ><br />tab</>'
data = '  </bat> <br/><br/ ><br />tab</>'
data = '<br/><br/ ><br />tab</>'
data = '<br/><br/ ><br />tab'
data = '<br/><br/ >'
alt1 = 'foo __________bah da____qyp_____  ______ _________tab'


# Now we can easily know whether we are in a tag.
# Next we want to know if we are in an opening/closing/self-closing tag.
# To do that we should first elaborate the original tag_filter to yield one of
# four states, [out, in, open, close]
# or maybe
# five states, [out, in, open, close, slash]
# six states, [out, in, open, close, slash, white]
# with the extras only being relevant <inside tags>
# four states, [out, in, lt, gt]

@coroutine
def tag_filter2():
    """
    coroutine accepting characters and yielding 
    one of several states/characters currently:  '<>io/ '
    """
    state = None
    while True:
        char = yield state
        if char != '<':
            state = 'o'
            continue
        state = char  # <

        # char == < ... grab chars until >
        while state != '>':
            char = yield state
            if char in '/ >':
                state = char
            else:
                state = 'i'


def test_tag_filter2(data):
    tf2 = tag_filter2()
    result = ''.join(tf2.send(char) for char in data)
    return result

import re


def analyze_token(s):
    if not s.startswith('<'):
        return s
    s = re.sub('\s*>', '>', s)  # remove whitespace before >
    close = lambda s: s.startswith('</')
    self_close = lambda s: s.endswith('/>')
    if close(s):
        name = s[2:-1]
        return ('close', close_check(name))
    if self_close(s):
        name = s[1:-2]
        return ('self_close', close_check(name))
    content = s[1:-1].split()
    name = content[0]
    return ('open', name)


def close_check(s):
    lst = s.split()
    if not lst:
        raise Exception('No text in closing tag')
    try:
        lst[1]
        raise Exception('Too many words in closing tag')
    except: # happy
        return lst[0]


def analyze_open(s):
    # extract attributes
    print 'later'


def token_classifier(data):
    prev_state = ''
    tag_state = ''

    token_list = xml_tokenizer(data)
    return [analyze_token(t) for t in token_list]
    globals().update(locals())




def test_blah(data):
    b = blah(data)
    return ''.join(char for char in blah(data))




