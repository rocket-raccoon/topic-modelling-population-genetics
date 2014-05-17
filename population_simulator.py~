#Dependencies
import random, math
import numpy as np
import scipy
import os
from scipy.stats import mode

class population_simulator():
	
	def __init__(self):
		self.no_loci = 5000
		self.freq = .002
		self.no_individuals = 100
		self.batch_size = min(self.no_loci, 1000)
		self.no_batches = self.no_loci / self.batch_size
		self.k = 1 / self.freq 
	
	def set_cohort_size(self, size):
		self.no_individuals = size
	
	def set_population_ratios(self, ratios):
		self.ratios = ratios
		self.no_ancestral_pops, self.no_admixed_pops = ratios.shape
	
	def generate_ancestral_allele_freqs(self, testing=0):
		w = math.log(self.k)
		if testing == 0:
			ancestral_pops = np.zeros((self.no_ancestral_pops, self.no_loci))
			for i in xrange(self.no_ancestral_pops):
				ancestral_pops[i,:] = [math.exp(w*random.random()-w) for x in xrange(self.no_loci)]
			self.ancestral_pops = ancestral_pops
		else:
			self.no_loci = self.no_ancestral_pops
			ancestral_pops = np.zeros((self.no_ancestral_pops, self.no_loci))
			for i in xrange(self.no_ancestral_pops):
				ancestral_pops[i,:] = [0 for x in xrange(self.no_loci)]
				ancestral_pops[i,i] = 1
			self.ancestral_pops = ancestral_pops
	
	def generate_admixed_allele_freqs(self, ancestral_pops, ratios):
		ancestral_pops = np.array(ancestral_pops)
		n = len(ancestral_pops.T)
		admixed_pop = [0 for x in xrange(n)]
		for i in xrange(n):
			admixed_pop[i] = np.dot(ancestral_pops[:,i], ratios)
		return admixed_pop
	
	def generate_cohort(self, no_individuals, pop_density, pop, begin):
		cohort = np.zeros((no_individuals, len(pop_density)))
		allele_sample = np.random.rand(2, no_individuals, len(pop_density))
		for j in xrange(len(pop_density)):
			v1=allele_sample[0,:,j] <= pop_density[j]
			v2=allele_sample[1,:,j] <= pop_density[j]
			cohort[:,j] = v1.astype(int) + v2.astype(int)
		del allele_sample 
		a = np.array(mode(cohort)[0]);
		for i in xrange(no_individuals):
			name = 'individuals/pop%dindiv%d.txt' % (pop,i)
			filename = open(name, 'a')
			Ind = [x for x in xrange(len(pop_density))]
			Ind = np.array(Ind)
			Ind = Ind + begin - 1
			for j in range(len(pop_density)):
				if(a.T[j]!=cohort[i,j]):
					filename.write('%dV%d ' % (Ind[j]+1,cohort[i,j]))
			filename.close()
	
	def clear_genomes(self):
		individuals = os.listdir("individuals")
		for individual in individuals:
			os.remove("individuals/" + individual)
	
	def generate_genomes(self):
		self.clear_genomes()
		for i in xrange(self.no_admixed_pops):
			pops = self.generate_admixed_allele_freqs(self.ancestral_pops, self.ratios[:,i])
			k = 0
			indices = [t for t in range(self.batch_size)] 
			for j in range(self.no_batches):
				k = j
				ix = np.array(indices) + k*self.batch_size
				self.generate_cohort(self.no_individuals, pops[ix[0]:ix[len(ix)-1]], i, k*self.batch_size)









	
