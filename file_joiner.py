#Dependencies
import os
import re

#Takes an input directory of text files, joins them into one file, and saves it on disk
class file_joiner():
	
	def set_input_folder(self, directory):
		self.directory = directory
	
	def join_files(self, partition_size):
		
		def tryint(s):
			try:
				return int(s)
			except:
				return s
		
		def alphanum_key(s):
			#Turn a string into a list of string and number chunks "z23a" -> ["z", 23, "a"]
			return [ tryint(c) for c in re.split('([0-9]+)', s) ]
		
		def sort_nicely(l):
			#Sort the given list in the way that humans expect
			l.sort(key=alphanum_key)
		
		txt_files = [f for f in os.listdir(self.directory) if ".txt" in f]
		sort_nicely(txt_files)
		counter = 1
		f = open('corpus/my_corpus.txt', 'w')
		for txt_file in txt_files:
			doc = open(self.directory + "/" + txt_file).read().strip("\n")
			f.write(doc)
			if counter % partition_size == 0:
				counter = 1
				f.write("\n")
			else:
				counter += 1
		f.close()













		

