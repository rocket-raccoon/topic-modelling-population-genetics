#Necessary imports
from gensim import corpora, models, similarities
import population_simulator
import numpy as np
import file_joiner
import ratio_inferrer
from sklearn.preprocessing import normalize

#First we set the paramaters of the simulator
ratios1 = [0.34, 0.33, 0.33]
ratios2 = [0.90, 0.05, 0.05]
ratios3 = [0.10, 0.10, 0.80]
ratios4 = [0.20, 0.40, 0.40]
ratios = np.matrix([ratios1, ratios2, ratios3, ratios4]).T
simulator = population_simulator.population_simulator()
simulator.set_population_ratios(ratios)
simulator.generate_ancestral_allele_freqs()

#Generate the cohorts of the specified size
partition_size = 1
simulator.set_cohort_size(200)
simulator.clear_genomes()
simulator.generate_genomes()
	
#Join individual genomes into one big file
fj = file_joiner.file_joiner()
fj.set_input_folder("individuals")
fj.join_files(partition_size)

#Import documents from big file, tokenize them, create vectorized corpus, and train LDA model
documents = [f.strip() for f in open("corpus/my_corpus.txt")]
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

#Test really high alpha
alpha = 20
test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary, alpha=alpha)
ri = ratio_inferrer.ratio_inferrer()
inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
real_ratios = ratios.T.tolist()
inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
ri.plot_side_by_side(real_ratios, inferred_ratios)

#Default alpha
test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary)
ri = ratio_inferrer.ratio_inferrer()
inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
real_ratios = ratios.T.tolist()
inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
ri.plot_side_by_side(real_ratios, inferred_ratios)

#Test really low alpha
test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary, alpha=alpha, eta=0.90)
ri = ratio_inferrer.ratio_inferrer()
inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
real_ratios = ratios.T.tolist()
inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
ri.plot_side_by_side(real_ratios, inferred_ratios)
















