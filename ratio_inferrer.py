#Get dependencies
import itertools
import math
import numpy as np
import matplotlib.pyplot as plt

class ratio_inferrer():
	
	#Estimates cohort population makeup by average LDA averages over individuals	
	def get_inferred_ratios(self, partition_size, num_individuals, num_groups, lda_model, corpus):
		inferred_ratios = []
		average = [0,0,0]		
		for i in range(0, (num_individuals/partition_size)*num_groups):
			corp = corpus[i]
			breakdown = lda_model[corp]
			for composition in breakdown:
				topic = composition[0]
				percent = composition[1]
				average[topic] = average[topic] + percent
			if (i+1) % (num_individuals/partition_size) == 0:
				average = [float(a) / (num_individuals/partition_size) for a in average]
				inferred_ratios.append(average)
				average = [0,0,0]
		return inferred_ratios
		
	#Matches LDA hidden topics to ancestral populations by minimizing RMSE
	def align_inferred_ratios(self, true_ratios, inferred_ratios):
		n = len(true_ratios[0])
		no_pops = len(true_ratios)
		permutations = list(itertools.permutations(range(1,n+1)))
		best_permutation = 0
		best_rmse_score = 100000
		for permutation in permutations:
			score = 0.0
			for i in range(0, no_pops):
				for j in range(0,n):
					true_ratio = true_ratios[i][j]
					permutation[j]-1
					inferred_ratio = inferred_ratios[i][permutation[j]-1]
					score = score + math.pow(float(true_ratio) - float(inferred_ratio), 2)
			score = math.sqrt(score / float(no_pops*n))
			if(score < best_rmse_score):
				best_rmse_score = score
				best_permutation = permutation
		aligned_ratios = []
		for ratio in inferred_ratios:
			temp = []
			for p in best_permutation:
				temp.append(ratio[p-1])
			aligned_ratios.append(temp)
		return aligned_ratios, best_rmse_score
	
	#Takes in a set of ratios (either real or inferred) and plots it using stacked bar chart
	def plot_ratio_distribution(self, ratios):
		no_pops = len(ratios)
		n = len(ratios[0])
		proportions = []
		for i in range(0, n):
			temp = []			
			for j in range(0, no_pops):
				temp.append(ratios[j][i])
			proportions.append(temp)
		colors = ['r', 'y', 'b', 'g', 'o']
		ind = np.arange(no_pops)
		width = 0.35
		height = [0 for i in range(0, no_pops)]
		for i in range(0, n):
			if i == 0:
				plt.bar(ind, proportions[i], width, color = colors[i])
			else:
				height = [sum(x) for x in zip(height, proportions[i-1])]
				plt.bar(ind, proportions[i], width, color = colors[i], bottom=height)
		plt.yticks(np.arange(0,1,.1))
		plt.show()
	
	#Plots both the real and inferred ratios side by side for comparison
	def plot_side_by_side(self, real_ratios, inferred_ratios):
		#Set the parameters of the chart
		no_pops = len(real_ratios)
		n = len(real_ratios[0])
		colors = ['r', 'y', 'b', 'g', 'o']
		ind = np.arange(no_pops)
		width = 0.7
		#Plot the real_ratios first
		height = [0 for i in range(0, no_pops)]		
		proportions = []
		for i in range(0, n):
			temp = []			
			for j in range(0, no_pops):
				temp.append(real_ratios[j][i])
			proportions.append(temp)
		for i in range(0, n):
			if i == 0:
				plt.bar(ind, proportions[i], width, color = colors[i])
			else:
				height = [sum(x) for x in zip(height, proportions[i-1])]
				plt.bar(ind, proportions[i], width, color = colors[i], bottom=height)
		#Then plot the inferred ratios
		height = [0 for i in range(0, no_pops)]
		proportions = []
		for i in range(0, n):
			temp = []			
			for j in range(0, no_pops):
				temp.append(inferred_ratios[j][i])
			proportions.append(temp)
		for i in range(0, n):
			if i == 0:
				plt.bar(ind+6, proportions[i], width, color = colors[i])
			else:
				height = [sum(x) for x in zip(height, proportions[i-1])]
				plt.bar(ind+6, proportions[i], width, color = colors[i], bottom=height)
		plt.yticks(np.arange(0,1,.1))
		plt.show()









			
		
