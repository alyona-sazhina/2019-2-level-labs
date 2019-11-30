import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word):
        if word not in self.storage and type(word) == str:
            self.storage[word] = len(self.storage)
            return self.storage[word]
        return {}

    def get_id_of(self, word):
        if word in self.storage:
            return self.storage[word]
        return -1

    def get_original_by(self, id):
        for word, i in self.storage.items():
            if i == id:
                return word
        return 'UNK'

    def from_corpus(self, corpus):
        if type(corpus) == tuple:
            for word in corpus:
                self.put(word)
            return self.storage
        return {}


class NGramTrie:
    def __init__(self, n):
        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple):
        if type(sentence) == tuple:
            for i in range(len(sentence) - self.size + 1):
                a = [sentence[i + b] for b in range(self.size)]
                a = tuple(a)
                if a in self.gram_frequencies.keys():
                    self.gram_frequencies[a] += 1
                else:
                    self.gram_frequencies[a] = 1
            return self.gram_frequencies
        return []

    def calculate_log_probabilities(self):
        dictionary = {}
        for i, j in self.gram_frequencies.items():
            if i[:self.size - 1] not in dictionary:
                dictionary[i[:self.size - 1]] = j
            else:
                dictionary[i[:self.size - 1]] += j
        for i, j in self.gram_frequencies.items():
            if i not in self.gram_log_probabilities:
                p = j / dictionary[i[:self.size - 1]]
                self.gram_log_probabilities[i] = math.log(p)
        return self.gram_log_probabilities

    def calculate_log_probabilities1(self):
        for i, j in self.gram_frequencies.items():
            counter = 0
            if i in self.gram_log_probabilities.keys():
                continue
            for a in self.gram_frequencies:
                if i[:self.size - 1] == a[:self.size - 1]:
                    counter += self.gram_frequencies[a]
            p = j / counter
            self.gram_log_probabilities[i] = math.log(p)
        return self.gram_log_probabilities

    def predict_next_sentence1(self, prefix):
        maximum = -32000
        key = prefix
        if type(prefix) == tuple and len(prefix) == self.size - 1:
            for a, b in self.gram_log_probabilities.items():
                if key[-1] != a[0]:
                    continue
                for i, j in self.gram_log_probabilities.items():
                    if key[-1] != a[0] and j > maximum:
                        maximum = j
                key = list(key)
                if maximum == -32000:
                    return key
                for i, j in self.gram_log_probabilities.items():
                    if j == maximum:
                        key.append(i[-1])
                        break
            return key
        return []

    def predict_next_sentence(self, prefix):
        if type(prefix) == tuple and len(prefix) == self.size - 1:
            print(len(self.gram_log_probabilities))
            for a in range(round(len(self.gram_log_probabilities)/2)):
                maximum = -32000
                prefix = list(prefix)
                for i, j in self.gram_log_probabilities.items():
                    i = list(i)
                    if prefix[a:] == i[:self.size - 1]:
                        if j > maximum:
                            maximum = j
                if maximum == -32000:
                    return prefix
                for i, j in self.gram_log_probabilities.items():
                    if j == maximum:
                        prefix.append(i[-1])
            return prefix
        return []


def encode(storage_instance, corpus):
    encoded_corpus1 = []
    encoded_corpus = []
    for sent in corpus:
        sentence = []
        encoded_corpus1.append(sentence)
        for word in sent:
            sentence.append(storage_instance.get_id_of(word))
    for sent in encoded_corpus1:
        for word in sent:
            encoded_corpus.append(word)
    return tuple(encoded_corpus)


def split_by_sentence(text: str) -> list:
    if not text or ' ' not in text:
        return []
    new_text = ''
    for symbol in text:
        if symbol.isalpha() or symbol in ' .!?':
            if symbol in '!?':
                new_text += '.'
            else:
                new_text += symbol
    sent_list = []
    new_text += ' A'
    a = 0
    for i in range(len(new_text[:-2])):
        if new_text[i] == '.' and new_text[i+1] == ' ' and (new_text[i+2].isupper() or new_text[i+2] == ' '):
            sent_list.append(new_text[a:i])
            if new_text[i+2] == ' ':
                a = i + 3
            else:
                a = i + 2
    corpus = []
    for sent in sent_list:
        words1 = sent.split(' ')
        words = [symbol.lower() for symbol in words1 if symbol != '']
        words = ['<s>'] + words + ['</s>']
        corpus.append(words)
    return corpus


def big_text():
    storage_instance = WordStorage()
    a = NGramTrie(3)
    #corpus = split_by_sentence('Mary wanted to swim. However, she was afraid of sharks! Mary wanted. Mary wanted. However, she was.')
    corpus = split_by_sentence(REFERENCE_TEXT)
    for j in corpus:
        storage_instance.from_corpus(tuple(j))
    encoded_corpus = encode(storage_instance, corpus)
    a.fill_from_sentence(encoded_corpus)
    a.calculate_log_probabilities()
    prediction = ''
    predict = a.predict_next_sentence((1, 301))
    print(predict)
    for i in range(len(predict)):
        prediction = prediction + storage_instance.get_original_by(predict[i]) + ' '
    print(prediction)