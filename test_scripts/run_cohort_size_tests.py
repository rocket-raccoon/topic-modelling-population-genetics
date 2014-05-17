#Necessary imports
from gensim import corpora, models, similarities
import population_simulator
import numpy as np
import file_joiner
import ratio_inferrer

#Track the RMSE score as we adjust the no individuals per cohort
cohort_sizes = [50, 100, 200, 400, 600, 800, 1000]
num_runs = 10
results = []

#First we set the paramaters of the simulator
ratios1 = [0.34, 0.33, 0.33]
ratios2 = [0.90, 0.05, 0.05]
ratios3 = [0.10, 0.10, 0.80]
ratios4 = [0.20, 0.40, 0.40]
ratios = np.matrix([ratios1, ratios2, ratios3, ratios4]).T
simulator = population_simulator.population_simulator()
simulator.set_population_ratios(ratios)
simulator.generate_ancestral_allele_freqs()

#Test the RMSE as a function of cohort size
for cohort_size in cohort_sizes:
	
	partition_size = cohort_size
	result = 0
	for i in range(num_runs):
		
		#Generate the cohorts of the specified size
		simulator.set_cohort_size(cohort_size)
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
		test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary)
		
		#Get the inferred ratios from the LDA, get the true ratios, then align them
		ri = ratio_inferrer.ratio_inferrer()
		inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
		real_ratios = ratios.T.tolist()
		inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
		result += score
	
	result = float(result)/num_runs
	results.append(result)
	print "Testing done for cohort of size %d" % cohort_size

plt.plot(cohort_sizes, results)
plt.xlabel("Cohort Size")
plt.ylabel("RMSE")











