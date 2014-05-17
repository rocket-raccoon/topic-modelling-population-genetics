#Necessary imports
from gensim import corpora, models, similarities
from parameters import *
import population_simulator
import numpy as np
import file_joiner
import ratio_inferrer

#We generate the cohort genomes for each population
simulator = population_simulator.population_simulator()
simulator.set_cohort_size(cohort_size)
simulator.set_population_ratios(ratios)
simulator.generate_ancestral_allele_freqs()
simulator.generate_genomes()
print "Cohorts generated"

#Join individual genomes into one big file
fj = file_joiner.file_joiner()
fj.set_input_folder("individuals")
fj.join_files(partition_size)
print "Files joined"

#Import documents from big file, tokenize them, and create vectorized corpus
documents = [f.strip() for f in open("corpus/my_corpus.txt")]
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

#Now we create our ensemble of LDA models
overall_inferred_ratios = np.zeros([simulator.no_admixed_pops, simulator.no_ancestral_pops])
for i in range(ensemble_size):
	
	test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary)
	ri = ratio_inferrer.ratio_inferrer()
	inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
	real_ratios = ratios.T.tolist()
	inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
	overall_inferred_ratios += np.array(inferred_ratios)
	
overall_inferred_ratios = overall_inferred_ratios / ensemble_size
blah, score = ri.align_inferred_ratios(real_ratios, overall_inferred_ratios.tolist())

#Finally, display the results
print "The Root Mean Squared Error is: %f" %score
ri.plot_side_by_side(real_ratios, overall_inferred_ratios.tolist())








