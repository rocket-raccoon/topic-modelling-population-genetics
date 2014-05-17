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

#Test the RMSE as a function of cohort size
lda_result = 0
num_runs = 25
partition_size = 100
for i in range(num_runs):
	
	#Generate the cohorts of the specified size
	simulator.set_cohort_size(100)
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
	print score
	lda_result += score

lda_result = float(lda_result)/num_runs

#Find results using random modelling
random_result = 0
num_runs2 = 100
for i in range(0,num_runs2):
	
	#Generate random ratios
	random_ratios = np.random.rand(4,3)
	for i in range(0, random_ratios.shape[0]):
		sum = 0
		for j in range(0, random_ratios.shape[1]):
			sum += random_ratios[i,j]
		random_ratios[i] = random_ratios[i]*(float(1)/float(sum))
	
	#Find best fit for random ratios and record score
	ri = ratio_inferrer.ratio_inferrer()
	inferred_ratios = random_ratios.tolist()
	real_ratios = ratios.T.tolist()
	for i in range(0,4):
		for j in range(0,3):
			real_ratio = real_ratios[i][j]
			inferred_ratio = inferred_ratios[i][j]
			score = score + math.pow(float(real_ratio) - float(inferred_ratio), 2)
	score = math.sqrt(score / float(4*3))
	random_result += score

random_result = float(random_result) / num_runs2

#Plot the results side by side in a bar chart
results = (lda_result, random_result)
ind = np.arange(2)
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, results, width, color='r')
plt.ylabel("RMSE")
plt.show()















