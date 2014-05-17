def cohort_simulator_full(n,pop_density,pop,begin):
		cohort = zeros((n, len(pop_density)));
		allele_sample = random.rand(2,n,len(pop_density)); 
		
		for j in range(len(pop_density)):
			v1=allele_sample[0,:,j] <= pop_density[j];
			v2=allele_sample[1,:,j] <= pop_density[j];
			cohort[:,j] = v1.astype(int) + v2.astype(int); 
		#print(cohort)
		del allele_sample ; 
		a=array(mode(cohort)[0]); # a is the matrix of the mode of each loci site and b tells you at each loci, how many times the mode occurs
		for i in range(n):
			name='files/pop%dindiv%d.txt' % (pop,i)
			#name2="test/pop%dindiv%d.txt" % (pop,i)
			filename = open(name,'a')
			#filename2 = open(name2,'w')
			#Ind = find((base ~= cohort(i,:)) == 1) ;
			# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			# %comment the below line when you do not want everything to be printed
			# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			Ind = [x for x in range(len(pop_density))];
			Ind=array(Ind);
			# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			Ind = Ind + begin - 1;  
			#count=0;
			for j in range(len(pop_density)):
				if(a.T[j]!=cohort[i,j]):filename.write('%dV%d ' % (Ind[j]+1,cohort[i,j])); #count=count+1;
				#filename.write('%dV%d ' % (Ind[j]+1,cohort[i,j]));
			filename.close(); 
			#print(count)
		#return( cohort, LL ,Token )






	
