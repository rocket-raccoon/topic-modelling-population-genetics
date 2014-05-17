#Necessary imports
from gensim import corpora, models, similarities
import population_simulator
import numpy as np
import file_joiner
import ratio_inferrer

#Track the RMSE score as we adjust the no individuals per cohort
cohort_size = 50
num_runs = 5
results = []
partition_size = cohort_size
ensemble_size = 25

#First we set the paramaters of the simulator
ratios1 = [0.34, 0.33, 0.33]
ratios2 = [0.90, 0.05, 0.05]
ratios3 = [0.10, 0.10, 0.80]
ratios4 = [0.20, 0.40, 0.40]
ratios = np.matrix([ratios1, ratios2, ratios3, ratios4]).T
simulator = population_simulator.population_simulator()
simulator.set_population_ratios(ratios)
simulator.set_cohort_size(cohort_)
simulator.generate_ancestral_allele_freqs()
simulator.clear_genomes()
simulator.generate_genomes()

results = []

ensemble_size = 25
overall_inferred_ratios = np.zeros([simulator.no_admixed_pops, simulator.no_ancestral_pops])
for j in range(ensemble_size):
	
	test_lda = models.LdaModel(corpus, num_topics=simulator.no_ancestral_pops, id2word=dictionary)
	ri = ratio_inferrer.ratio_inferrer()
	inferred_ratios = ri.get_inferred_ratios(partition_size, simulator.no_individuals, simulator.no_admixed_pops, test_lda, corpus)
	real_ratios = ratios.T.tolist()
	inferred_ratios, score = ri.align_inferred_ratios(real_ratios, inferred_ratios)
	overall_inferred_ratios += np.array(inferred_ratios)
	
overall_inferred_ratios = overall_inferred_ratios / ensemble_size
blah, score = ri.align_inferred_ratios(real_ratios, overall_inferred_ratios.tolist())
results.append(score)

ri.plot_side_by_side(real_ratios, overall_inferred_ratios.tolist())



