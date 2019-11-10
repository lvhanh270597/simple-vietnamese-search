import os.path, json
from nltk.tokenize import sent_tokenize
from system.data_structures.sentence import Sentence
from system.helpers import string

def set_filenames(self, filenames):
    self.filenames = filenames

def preprocessing(self, actions):
    for key in actions.keys():
        new_data = self._data[key]
        for action in actions[key]:
            for i, item in enumerate(new_data):
                new_data[i] = self.functions[action](item)
        self._data[key] = new_data

def save(self, save_as):
    for key in save_as:
        with open(save_as[key], "w") as f:
            f.write("\n".join(self._data[key]))

def item_indices(key, indices, default=None):
    if key not in indices:
        return default
    return indices[key]

def get_bow_vectors(list_sentences, ngrams, vocab):
    vectors = []
    sentence_ins = Sentence()
    for sentence in list_sentences:
        vector = [0] * (vocab.length() + 1)
        sentence_ins.set_sentence(sentence)
        for n in ngrams:
            ngrams_features = sentence_ins.extract_n_gram(n)
            indices = vocab.get_vector_indices_by_list(ngrams_features)
            for index in indices:
                vector[index] = 1
        vectors.append(vector)
    return vectors

def get_window_item(sentence, window_size):
    noa_sentence = Sentence(sentence).remove_accents()
    noa_words = noa_sentence.split()
    words = sentence.split()

    vectors = []
    half_size = window_size // 2
    words = ['__begin__'] * half_size + words + ['__end__'] * half_size
    noa_words = ['__begin__'] * half_size + noa_words + ['__end__'] * half_size
    word_size = len(noa_words)

    for i in range(half_size, word_size - half_size):
        current_words = ' '.join(noa_words[i - half_size : i + half_size + 1])
        vectors.append(tuple([current_words, noa_words[i], words[i]]))

    return vectors

def create_window_items(data, window_size, only_lower=True):
    res = dict()
    cur, cnt = 1, len(data)
    for sentence in data:
        print("Processing at %d/%d %.2f%%" % (cur, cnt, (cur / cnt) * 100))
        vectors = get_window_item(sentence, window_size)
        for X, label, rlabel in vectors:
            if only_lower:
                if label.isalpha() and label.islower():
                    if label not in res:
                        res[label] = []
                    res[label].append(tuple([X, rlabel]))
            else:
                if label not in res:
                    res[label] = []
                res[label].append(tuple([X, rlabel]))
        cur += 1
    return res

def get_indices(self, name, default=True, startIndex=1, line_or_word='line', delimiter=' ', action=None):
    list_of_words = []
    if default:
        list_of_words.extend(config.DEFAULT)
    if (type(name) == str) and (name in self.filenames):
        list_of_words.extend(self._data[name])
    else:
        list_of_words.extend(list(name))
    res = dict()
    index = startIndex
    for line in list_of_words:
        items = [line]
        if line_or_word == 'word':
            items = line.split(delimiter)
        for item in items:
            if action is not None:
                if action in self.functions:
                    item = self.functions[action](item)
            if item not in res:
                res[item] = index
                index += 1
    return res
def get_noa_words(self, list_of_words):
    res = dict()
    for word in list_of_words:
        noa_word = string.accentdel(word)
        if noa_word not in res:
            res[noa_word] = {word}
        else:
            res[noa_word].add(word)
    return res
def save_indices_as_json(self, indices, fname):
    if type(list(indices.values())[0]) == set:
        for key in indices:
            indices[key] = list(indices[key])
    with open(fname, "w") as f:
        json.dump(indices, f)
def load_json_files(self, list_fnames):
    self.last_data = dict()
    for name in list_fnames:
        self.last_data[name] = self.json_read(list_fnames[name])
    return self.last_data

def separate_sentence(document):
    sentences = sent_tokenize(document)
    return sentences

def get_vocabulary(sentences, ngrams, startIndex=1, init=[]):
    vocabulary = Vocabulary(startIndex)
    vocabulary.add_list(init)

    sentence_ins = Sentence()
    for sentence in sentences:
        sentence_ins.set_sentence(sentence)
        for n in ngrams:
            vocabulary.add_list(sentence_ins.extract_n_gram(n))

    return vocabulary

def get_dict_feature(sentence, refer, max_words):
    words = sentence.split()
    half = len(words) // 2
    vector = []
    for nsize in range(max_words, 0, -1):
        for i in range(0, len(words) - nsize + 1):
            last_index = i + nsize - 1
            if (i <= half) and (last_index >= half):
                cur_word = ' '.join(words[i: last_index + 1])
                item = 1 if cur_word in refer else 0
                vector.append(item)
    return vector

def separate_part(data, n_part):
    data_parts = []
    for i in range(n_part):
        data_parts.append([])
    for item in data:
        for i in range(n_part):
            data_parts[i].append(item[i])
    return data_parts
