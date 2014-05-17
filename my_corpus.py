#Dependencies
from gensim import corpora, models, similarities

#This allows us to iterate through a huge corpus one document at a time
class my_corpus():
	
	def __init__(self, corpus_file):
		self.corpus_file = corpus_file
		create_dictionary(self)
	
	def create_dictionary(self):
		stoplist = set('for a of the and to in'.split())
		dictionary = corpora.Dictionary(line.lower().split() for line in open(self.corpus_file))
 		# remove stop words and words that appear only once
		stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
		once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
		dictionary.filter_tokens(stop_ids + once_ids)
		dictionary.compactify()
		self.dictionary = dictionary
	
	def __iter__(self):
		for line in open(self.corpus_file):
			yield self.dictionary.doc2bow(line.lower().split())
