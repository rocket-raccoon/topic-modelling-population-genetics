#Necessary imports
from gensim import corpora, models, similarities
import population_simulator
import numpy as np
import file_joiner
import ratio_inferrer

#First we set the paramaters of the simulator
ratios1 = [0.34, 0.33, 0.33]
ratios2 = [0.90, 0.05, 0.05]
ratios3 = [0.10, 0.10, 0.80]
ratios4 = [0.20, 0.40, 0.40]
ratios = np.matrix([ratios1, ratios2, ratios3, ratios4]).T
cohort_size = 500
partition_size = cohort_size

#Simulate genomres
simulator = population_simulator.population_simulator()
simulator.set_population_ratios(ratios)
simulator.set_cohort_size(cohort_size)
simulator.generate_ancestral_allele_freqs()
simulator.clear_genomes()
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

#Train and evaluate model
test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary)
ri = ratio_inferrer.ratio_inferrer()
inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
real_ratios = ratios.T.tolist()
inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
print "LDA Model trained"

#plot
ri.plot_side_by_side(real_ratios, inferred_ratios)








