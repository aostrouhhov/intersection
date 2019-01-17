import os
import sys
import time
import numpy as np
import cupy as cp

grammar_path = sys.argv[1]
graph_path = sys.argv[2]
answer_path = sys.argv[3]

class GrammarRule():
	def __init__(self, from1, to1, to2):
		self.from1 = from1
		self.to1 = to1
		self.to2 = to2

def algorithm():
	changed = False
	for rule in rulesList:
		temp = nontermMatrices[rule.from1]
		nontermMatrices[rule.from1] = temp + (nontermMatrices[rule.to1] @ nontermMatrices[rule.to2])
		changed = changed | (not np.array_equal(cp.asnumpy(nontermMatrices[rule.from1]), cp.asnumpy(temp)))
	return changed

if __name__ == "__main__":
	nontermDict = dict() # key = term, value = producer-nonterm
	nontermMatrices = dict() # key = nonterm, value = matrix

	print('Reading amount of vertices in graph...')

	file_graph = open(graph_path, 'r')
	graph_lines = file_graph.read().splitlines()
	file_graph.close()

	# Find amount of vertices in graph to know matrices size
	num_vertices = 0
	for line in graph_lines:
		lexemas = line.split(' ')
		num_vertices = max(num_vertices, int(lexemas[0]), int(lexemas[2]))
	
	num_vertices += 1

	print('Reading grammar...')

	file_grammar = open(grammar_path, 'r')
	grammar_lines = file_grammar.read().splitlines() 
	file_grammar.close()

	rulesList = []

	for line in grammar_lines:
		lexemas = line.split(' ')
		if len(lexemas) == 3:
			rulesList.append(GrammarRule(lexemas[0], lexemas[1], lexemas[2]))
		if len(lexemas) == 2:
			try:
				nontermDict[lexemas[1]].append(lexemas[0])
			except KeyError:
				nontermDict[lexemas[1]] = []
				nontermDict[lexemas[1]].append(lexemas[0])

		# Init matrices for all nonterms, fill them with 'False'
		nontermMatrices.update({lexemas[0]: cp.array(np.zeros((num_vertices,num_vertices), dtype=bool))})

	print('Reading graph...')

	file_graph = open(graph_path, 'r')
	graph_lines = file_graph.read().splitlines()
	file_graph.close()

	for line in graph_lines:
		lexemas = line.split(' ')
		# Add 'True' to (i,j) for all nonterms from which term can be produced
		try:
			for nonterm in nontermDict[lexemas[1]]:
				nontermMatrices[nonterm][int(lexemas[0])][int(lexemas[2])] = True
		except KeyError:
			continue

	print("Calculating...")
	# Let's start multiplication!
	start = time.time()

	while True:
		changed = algorithm()
		if changed == False:
			break

	end = time.time()
	print("Done in {}s".format(end - start))

	print("Writing answer to {}...".format(answer_path))

	with open(answer_path, 'a') as file_answer:
		for nonterm in nontermMatrices:
			file_answer.write(nonterm)
			matrix = cp.asnumpy(nontermMatrices[nonterm])
			for i in range (0, num_vertices):
				for j in range (0, num_vertices):
					if matrix[i][j] == True:
						file_answer.write(" {} {}".format(i, j))
			file_answer.write("\n")

	print("Done")

	# To check manually
	# listoflists = []
	# a_list = []
	# for i in range (0, num_vertices):
	# 	a_list.append('')
	# for i in range (0, num_vertices):
	# 	listoflists.append(list(a_list))

	# for key in nontermMatrices:
	# 	matrix = cp.asnumpy(nontermMatrices[key])
	# 	for i in range (0, num_vertices):
	# 		for j in range (0, num_vertices):
	# 			if matrix[i][j] == True:
	# 				if listoflists[i][j] == '':
	# 					listoflists[i][j] = listoflists[i][j] + key
	# 				else:
	# 					listoflists[i][j] = listoflists[i][j] + " " + key

	# print("Answer:")
	# for list1 in listoflists:
	# 	print(list1)
