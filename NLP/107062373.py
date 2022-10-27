import streamlit as st
import re
from collections import Counter
from pprint import pprint
import time


time.clock = time.time


# from functools import filter

def words(text): return re.findall(r'\w+', text.lower())


txt = words(open('big.txt').read())
#txt = txt + words(open('word.list.txt').read())
# word_count = Counter(txt)
word_count = Counter(words(open('big.txt').read()))
# word_count = Counter(txt)

N = sum(word_count.values())


def P(word): return word_count[word] / N  # float


# Run the function:

#print(list(map(lambda x: (x, P(x)), words('speling spelling speeling'))))

letters = 'abcdefghijklmnopqrstuvwxyz'


def edits0(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [L + c + R for L, R in splits for c in letters]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    return set(inserts + transposes)


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)


# Run the function:

# print( list(edits1('speling')))
# print( list(map(lambda x: (x, P(x)), edits1('guic'))) )
#print(list(filter(lambda x: P(x) != 0.0, edits1('guic'))))


# print( max(edits1('guic'), key=P) )


def correction(word):
    return max(candidates(word), key=P)


def candidates(word):
    return (known([word]) or known(edits0(word)) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words):
    return set(w for w in words if w in word_count)


def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



st.title("Spellchecker Demo")
select_word = st.selectbox('Choose a word or ..',[' ','apple','lamon','speling','hapy'])
if select_word != " ":
    word = select_word
else:
    word = st.text_input('type your own')
org_word = st.sidebar.checkbox('show original word')
#word = st.text_input('type your own')

if org_word:
    st.write('Original word: '+word)
if correction(word) == word:
    #st.write('correct')
    #new_title = '<p style="font-family:sans-self; color:Green;background:MediumSeaGreen;"> <var> word </var>  is the correct spelling</p>'
    st.success(word+" is the correct spelling")
else:
    #new_title = '<p style="font-family:sans-self; color:#FF0000;background:#FF8888;">Correction: </p>'
    st.error('Correction: ' + correction(word))

