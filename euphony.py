import nltk
from nltk.corpus import cmudict, wordnet
import cPickle as pickle
import random
from nltk.collocations import *
from collections import defaultdict
from nltk.corpus import PlaintextCorpusReader
transcr = nltk.corpus.cmudict.dict()
corpus_root = '/Users/kevinzeidler/Documents/corpora/'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
ij = wordlists.words('InfiniteJest.txt')
import time
ts = time.time()
import datetime
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')

print str(st), type(st)


def words_containing( list_of_phonemes, from_corpus ):
	results = []
	excluded = ['u']
	if from_corpus is None:
	 	for key, value in transcr.iteritems():
	 		if all(map(lambda x: x in value[0], list_of_phonemes)):
	 			results.append(key)
	else:
	 	for word in from_corpus:
	 		word = word.lower()
	 		if word in transcr and word not in excluded:
		 		if all(map(lambda x: x in transcr[word][0], list_of_phonemes)):
		 			results.append(word)
 	return list(set(results))


def primary_pronunciation(word):
	return transcr[word][0]

def vowels(word):
	return filter(lambda x: len(x) == 3, transcr[word][0])

def cardinal_vowel(word):
	v = vowels(word)
	v = filter(lambda x: x[2] == '1', v)
	return v

def consonants(word):
	return filter(lambda x: len(x) < 3, transcr[word][0])



def consonance_score(word1, word2):
	affricates = ['B', 'D', 'DZ', 'G']
	stops = ['P', 'T', 'K']
	voiceless_obstruents = ['P', 'T', 'K', 'TH', 'F', 'CH', 'S', 'SH']
	voiced_obstruents = ['B', 'D', 'JH', 'G', 'V', 'DH', 'Z', 'ZH']
	approximates = ['W', 'R', 'JH', 'L']
	def has(phoneme_type, consonants):
		return any(map(lambda x: x in phoneme_type, consonants))
	def analyze_ending(w):
		mod = 0
		print ""
		print "   Analyzing '", w, "' ending" 
		c = consonants(w)
		if len(c) > 1:
			if c[-1:][0] in stops:
				print w, "explodes with ending:", c[-1:][0]
			if c[-1:][0] in affricates:
				mod = -3
				print w, "implodes with ending:", c[-1:][0]
			if c[-1:][0] is 'M' and c[-2:-1][0] in voiced_obstruents:
				print w, "ends on a syllabic nasal with ending:", c[-2:][0]
		return mod
	c1 = consonants(word1)
	c2 = consonants(word2)
	n = len(c2)
	score = 0
	score += analyze_ending(word1)
	score += analyze_ending(word2)
	print "Now scoring '", word1, word2, "' for consonance..."
	print word1, transcr[word1]
	print word2, transcr[word2]
	for consonant in c2:
		print "    ", "Score =", score
		if consonant in c1:
			print "  ", consonant, "is an exact match." 
			score += 1.5
		elif consonant in affricates and has(affricates,c1):
			print "  ", consonant, "is an affricate and", word1, "has affricates", filter(lambda x: x in affricates, c1)
			score += .5
		elif consonant in stops and has(stops,c1):
			print "  ", consonant, "is an stop and", word1, "has stops", filter(lambda x: x in stops, c1)
			score += .5
		elif consonant in approximates and has(approximates,c1):
			print "  ", consonant, "is an approximate and", word1, "has approximates", filter(lambda x: x in approximates, c1)
			score += .5
		elif consonant in voiceless_obstruents and has(voiceless_obstruents,c1):
			print "  ", consonant, "is a voiceless obstruent and", word1, "has voiceless_obstruents", filter(lambda x: x in voiceless_obstruents, c1)
			score += .25
		elif consonant in voiced_obstruents and has(voiced_obstruents, c1):
			print "  ", consonant, "is a voiced obstruent and", word1, "has voiced obstruents", filter(lambda x: x in voiceless_obstruents, c1)
			score += .25
		else:
			print "  ", consonant, "is not a match. Decrementing score..."
			score -= .5
	print ""
	
	print "   FINAL SCORE FOR '", word1.upper(), word2.upper(),"': ", score
	return tuple([score, str(word1 +" "+ word2)])








def words_containing_only( list_of_vowels, from_corpus ):
	vowels = ['AA1', 'AA2', 'AA0', 'AE0', 'AE1', 'AE2', 'AW0', 'AW1', 'AW2', 'IH0', 'IH1', 'IH2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'AH0', 'AH1', 'AH2', 'AO1', 'AO2', 'AO0', 'AY1', 'AY2', 'AY0', 'IY0', 'IY1', 'IY2', 'UW0', 'UW1', 'UW2', 'EY0','EY1','EY2', 'OW0','OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']
	results = []
	verified = []
	forbidden = vowels
	for i in list(set(list_of_vowels)):
		try:
			forbidden.remove(i)
		except ValueError:
			print i, "isn't in the vowels. Maybe you should add it."
	if from_corpus is None:
	 	for key, value in transcr.iteritems():
	 		if all(map(lambda x: x in value[0], list_of_vowels)):
	 			results.append(key)
	else:
		for word in from_corpus:
			word = word.lower()
			if word in transcr:
				if all(map(lambda x: x in transcr[word][0], list_of_vowels)):
					results.append(word)
 	for result in results:
 		pronunciation = transcr[result]
 		if any(map(lambda x: x in pronunciation[0], forbidden)):
 			#print "Removing", result, any(map(lambda x: x in pronunciation[0], forbidden))
 			results.remove(result)	
 		else:
 			verified.append(result)
 	return list(set(verified))


def words_with_vowel_pattern( phoneme_sequence, from_corpus ):
	candidates = words_containing_only(phoneme_sequence, from_corpus)
	results = []
	for word in candidates:
		pronunciation = transcr[word][0]
		vowels = filter(lambda x: len(x) == 3, pronunciation)
		if vowels == phoneme_sequence:
			results.append(word)
	return list(set(results))

def only(part_of_speech, list_of_words):
	results = []
	if part_of_speech is "adjectives":
		for word in list_of_words:
			adjective = wordnet.morphy(word,wordnet.ADJ)
			print word, adjective
			if adjective:
				results.append(adjective)
		return results
	if part_of_speech is "nouns":
		for word in list_of_words:
			noun = wordnet.morphy(word,wordnet.NOUN)
			print word, noun
			if noun:
				results.append(noun)
		return results
	if part_of_speech is "adverb":
		for word in list_of_words:
			adverb = wordnet.morphy(word,wordnet.ADV)
			print word, adverb
			if adverb:
				results.append(adverb)
		return results
	if part_of_speech is "verb":
		for word in list_of_words:
			verb = wordnet.morphy(word,wordnet.VERB)
			print word, verb
			if adverb:
				results.append(verb)
		return results


def words_with_vowel_pattern_and_pos( phoneme_sequence ):
	candidates = words_containing_only(phoneme_sequence)
	results = []
	for word in candidates:
		pronunciation = transcr[word][0]
		vowels = filter(lambda x: len(x) == 3, pronunciation)
		if vowels == phoneme_sequence:
			results.append(word)
	return preview(results,5)
def preview(lst,maxsize):
	samplelst = []
	if len(lst) >= maxsize:
		samplelst.extend(random.sample(lst,maxsize))
		return samplelst
	return lst

def print_combinations( list_of_lists ):
	for word1 in list_of_lists[0]:
		for word2 in list_of_lists[1]:
			for word3 in list_of_lists[2]:
				print word1, word2, word3

#print words_containing(['IH0','AE1','IH0'],ij)
word1 = 'baby'

def tokenize( fp ):
	with open(fp) as f:
 		raw = f.read()
 		tokens = nltk.word_tokenize(raw)
		text = nltk.Text(tokens)

def bigrams(filterword,freq,from_corpus,maxsize):
	## Bigrams
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
	# only bigrams that appear 3+ times
	sieved = lambda *w: filterword not in w
	finder.apply_freq_filter(freq)
	# only bigrams that contain 'creature'
	finder.apply_ngram_filter(sieved)
	# return the 10 n-grams with the highest PMI
	return finder.nbest(bigram_measures.likelihood_ratio, maxsize)

def trigrams(filterword, freq, from_corpus, maxsize):
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	sieved = lambda *w: filterword not in w
	finder = TrigramCollocationFinder.from_words(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
	# only trigrams that appear 3+ times
	finder.apply_freq_filter(freq)
	# only trigrams that contain 'creature'
	finder.apply_ngram_filter(sieved)
	# return the 10 n-grams with the highest PMI
	return finder.nbest(trigram_measures.likelihood_ratio, maxsize)

strictmatch = words_with_vowel_pattern(vowels(word1), ij)
#loosematch = words_containing(cardinal_vowel(word1), ij)
#print strictmatch
#print loosematch
tails = bigrams('baby', 'undefined')
tails = filter(lambda x: x[0] is 'baby', tails)
babybigrams = [(u'Congo', u'baby'), (u'baby', u'preserved'), (u'faced', u'baby'), (u'real', u'baby'), (u'however', u'baby'), (u'baby', u"'"), (u'every', u'baby'), (u'a', u'baby'), (u'baby', u'man'), (u'baby', u'an'), (u'baby', u'.')]
commonjoiners = [(u'it', u'is'), (u'It', u'is'), (u'is', u'not'), (u'there', u'is'), (u'is', u'a'), (u'what', u'is'), (u'There', u'is'), (u'that', u'is'), (u'is', u'no'), (u'this', u'is'), (u'This', u'is'), (u'which', u'is'), (u'is', u'called'), (u'He', u'is'), (u'Nor', u'is'), (u'whale', u'is'), (u'is', u'this'), (u'is', u'it'), (u'is', u'.'), (u'is', u'an'), (u'is', u'only'), (u'harpooneer', u'is'), (u'What', u'is'), (u'is', u'still'), (u'he', u'is'), (u'is', u'but'), (u'ambergris', u'is'), (u'Whale', u'is'), (u'is', u'technically'), (u'is', u'much'), (u'is', u'always'), (u'thing', u'is'), (u'Delight', u'is'), (u'whaling', u'is'), (u'is', u'chiefly'), (u'oil', u'is'), (u'is', u'very'), (u'is', u'quite'), (u'is', u'of'), (u'is', u'often'), (u'is', u'the'), (u'and', u'is'), (u';', u'is'), (u'is', u'impossible'), (u'spout', u'is'), (u'is', u'thine'), (u'line', u'is'), (u'is', u'nothing'), (u'brow', u'is'), (u'is', u'about'), (u'is', u'used'), (u'is', u'sometimes'), (u'is', u'perhaps'), (u'That', u'is'), (u'is', u'supplied'), (u'is', u'precisely'), (u'is', u'made'), (u'is', u'ginger'), (u'is', u'worship'), (u'Where', u'is'), (u'meat', u'is'), (u'leviathan', u'is'), (u'is', u'more'), (u'is', u'deemed'), (u'is', u'worth'), (u'business', u'is'), (u'gold', u'is'), (u'is', u'furnished'), (u'is', u'true'), (u'THAT', u'is'), (u'is', u';'), (u'is', u'worse'), (u'is', u'also'), (u'is', u'striking'), (u'is', u'sweet'), (u'is', u'seldom'), (u'whiteness', u'is'), (u'here', u'is'), (u'sun', u'is'), (u'Leviathan', u'is'), (u'is', u'generally'), (u'truth', u'is'), (u'How', u'is'), (u'is', u'found'), (u'name', u'is'), (u'point', u'is'), (u'is', u'all'), (u'blubber', u'is'), (u'wood', u'is'), (u'is', u'full'), (u'is', u'there'), (u'is', u'done'), (u'is', u'almost'), (u'is', u'so'), (u'where', u'is'), (u'is', u'ready'), (u'Ahab', u'is'), (u'whatever', u'is'), (u'is', u'mine'), (u'Yet', u'is')]

for i in strictmatch:
	stem = trigrams(i, 'undefined')
	print stem
	if stem:
		for i in stem:
			print i[0], i[1], i[2], 'baby'
			for tail in tails:
				nextln1 = random.choice(babybigrams)
				nextln2 = random.choice(commonjoiners)
				print str(i[0], i[1], i[2], 'baby'
				print str(nextln[0], nextln[1], 


n = only("nouns", words_with_vowel_pattern(vowels('swagger'), ij))
#v = only("verbs", loosematch)
adj = only("adjectives", loosematch)
def generate_grams(list_of_adjectives,word,minfreq,from_corpus,maxsize):
	for i in adj:
	 	if bigrams(i,1,'moby',100):
	 		for i in bigrams(i,1,'moby',100):
	 			 i[0], i[1], word



	
		


#pickle.dump(sorted(res),open(str('/Users/kevinzeidler/Documents/corpora/scored/'+ str(ts) + "-" + word1 + "-" + word2 + ".txt"),'w'))




 