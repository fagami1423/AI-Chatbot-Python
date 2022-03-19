# things we need for NLP
import enum
import nltk
import numpy as np
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

#tokenize the sentences into each individual tokens
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

#base of the word
def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_tokens):
    """
    sentence=["hello","how", "are", "you"]
    words = ["hi","hello","I","like","bye","thank","cool"]
    bag = [0,     1,        0,  1,     0,    0,     0]

    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_tokens), dtype=np.float32)
    for idx, w in enumerate(all_tokens):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag

