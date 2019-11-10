import string, time
from data_structures.sentence import Sentence
from data_structures.phanso import PhanSo
from functions.functions import *
from logs.log import *
from config import config
from nltk.tokenize import word_tokenize

class HiddenMarkovModel:
	def __init__(self,  list_ngrams=[2, 3, 4], eta=0.0001):
		print('Created Hidden Markov Model with ngrams =', list_ngrams)
		self.list_ngrams = set(list_ngrams)
		self.list_ngrams.add(1)
		self.maxtime = 0
		self.eta = eta
	def set_data(self, data):
		self.data = data
	def get_prop(self, ngram, list_words):
		hash_code = 0
		for word in list_words:
			if word not in config.INDICES:
				word = Sentence().R_S
			index = config.INDICES[word]
			hash_code = hash_code * config.HASH_BASE + index
		if hash_code not in self.prop[ngram]:
			return PhanSo(0, 1)
		return PhanSo(self.prop[ngram][hash_code], self.cnt[ngram])
	def get_next_word(self, results, window_prop, windows):
		for i in range(windows):
			for word in window_prop[i].keys():
				window_prop[i][word] = self.get_prop(1, [word])

		for i in range(windows - 2, -1, -1):
			for word1 in window_prop[i].keys():
				total = PhanSo(0, 1)
				word1_prop = window_prop[i][word1]
				for word2 in window_prop[i + 1].keys():
					x = window_prop[i + 1][word2].instance()
					x.multiple(self.get_prop(2, [word1, word2]))
					x.multiple(word1_prop)
					total.add(x)
				window_prop[i][word1] = total
		for i in range(windows - 3, -1, -1):
			for word1 in window_prop[i].keys():
				total = window_prop[i][word1].instance()
				for word2 in window_prop[i + 1].keys():
					for word3 in window_prop[i + 2].keys():
						total.add(self.get_prop(3, [word1, word2, word3]))
				window_prop[i][word1] = total
		next_word = None
		pre_prop = self.get_prop(1, results[-1:])
		max_num = PhanSo(0, 1)

		for word in window_prop[0].keys():
			x = window_prop[0][word].instance()
			x.multiple(pre_prop.instance())
			x.add(window_prop[0][word].instance())
			if max_num.compare(x) == -1:
				max_num = x
				next_word = word
		return next_word
	def calculate(self, list_words, windows=3):
		list_words = [Sentence().B_C] + list_words + [Sentence().E_C]
		for i, word in enumerate(list_words):
			if word not in config.WORDS:
				list_words[i] = Sentence().R_S
		nsize = len(list_words)
		related_words = [set()]
		for i in range(1, nsize - 1):
			if (Sentence().check_has_accent(list_words[i])) and (list_words[i] in config.INDICES):
				related_words.append({list_words[i]})
			else:
				related_words.append(config.WORDS[list_words[i]])
		window_prop = []
		for i in range(windows - 1): window_prop.append(dict())
		# Initialize
		for i in range(1, windows):
			for word in related_words[i]:
				window_prop[i - 1][word] = 0
		results = [Sentence().B_C]
		for start in range(1, nsize - 1):
			cur_win = min(windows, nsize - start - 1)
			end = start + windows - 1
			window_prop.append(dict())
			if end < len(related_words):
				for word in related_words[end]:
					window_prop[-1][word] = 0
			results.append(self.get_next_word(results, window_prop, cur_win))
			#self.get_next_word(results, window_prop, windows)
			del window_prop[0]
		return results

	def fast_predict(self, sentence):
		starttime = time.time()
		sentence = sentence.lower()
		table = str.maketrans({key: None for key in string.punctuation})
		sentence = sentence.translate(table)
		old_words = Sentence(sentence).revert()
		sentence = Sentence(sentence).remove_continue()
		new_words = word_tokenize(sentence)
		new_words = self.calculate(new_words)[1:]
		for i, word in enumerate(old_words):
			if Sentence().check_object(word):
				new_words[i] = word
			if new_words[i] is None:
				new_words[i] = old_words[i]
		sentence = ' '.join(new_words)
		endtime = time.time()
		self.current_time = endtime - starttime
		self.maxtime = max(self.maxtime, self.current_time)
		return sentence
	def predict(self, list_of_sentences):
		res = []
		for sentence in list_of_sentences:
			res.append(self.fast_predict(sentence))
		return res
	def match(self, str1, str2):
		listwords1 = set(str1.split())
		listwords2 = set(str2.split())
		giao = listwords1.intersection(listwords2)
		hop = listwords1.union(listwords2)
		return len(giao) / len(hop)
	def score(self):
		acc, cnt = 0, 0
		for sentence in config.TEST:
			cnt += 1
			sentence = sentence.lower()
			no_accents = Sentence().remove_accents(sentence)
			pred = self.fast_predict(no_accents)
			x = self.match(sentence, pred)
			print("Accuracy at %d/%d testcase %.2f%%" % (cnt, len(config.TEST), x * 100))
			print("On time: %f" % self.current_time)
			acc += x
		print('Accuracy = %.2f%%' % ((acc / cnt) * 100))

	def adjust_sentence(self, sentence):
		return [Sentence().B_C] + word_tokenize(sentence.lower()) + [Sentence().E_C]
	def get_indices(self, sentence):
		indices = []
		for word in self.adjust_sentence(sentence):
			if word not in config.INDICES:
				word = Sentence().R_S
			indices.append(config.INDICES[word])
		return indices
	def fit(self):
		print('Fitting model...')
		write_alog('Fitting model...')
		self.prop, self.cnt = {}, {}
		for i in self.list_ngrams:
			self.prop[i] = {}
			self.cnt[i] = 0
		print('Extracting n-gram ', self.list_ngrams)
		cnt, full_size = 1, len(config.TRAIN)
		for sentence in config.TRAIN[:int(full_size * 0.5)]:
			sentence = sentence.lower()
			for word in word_tokenize(sentence):
				no_accent = Sentence().remove_accents(word)
				if word not in config.INDICES:
					config.INDICES[word] = config.INDEX
					config.INDEX += 1
					if no_accent not in config.WORDS:
						config.WORDS[no_accent] = {word}
					else:
						config.WORDS[no_accent].add(word)

			print('Processing at %d/%d (%.2f%%)' %(cnt, full_size, (cnt / full_size) * 100))
			list_indices = self.get_indices(sentence)
			for ngram in self.list_ngrams:
				hash_ngram = get_hash_ngram(list_indices, ngram, config.HASH_BASE)
				for item in hash_ngram:
					if item not in self.prop[ngram]:
						self.prop[ngram][item] = 1
					else:
						self.prop[ngram][item] += 1
				self.cnt[ngram] += len(hash_ngram)
			cnt += 1
		print('Done!')
		write_alog('Done!')