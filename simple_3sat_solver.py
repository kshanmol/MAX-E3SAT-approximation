# Simple 3-SAT solver. More like a "maximizer of satisfied clauses".
# Satisfies atleast 7/8 clauses of any Boolean 3-SAT formula
# Based on derandomization of the simple Monte Carlo algorithm of random assignment
# Time complexity O(n*m), where n is the number of variables and m is the number of clauses

# Observations
# 1. Performs much better in practice when number of variables is of the same order or greater than the number of clauses
#	 Try n = 10000, m = 1000 
# 2. Things get interesting with really less number of variables. The fraction of satisfied clauses approaches its lower bound.
#    Try n = 10, m = 1000000

import random

def randomVariable(n):
	return random.randint(0,2*n-1)

def getRandomFormula(n,m):

	f = []

	for i in range(m):
		f.append([])
		for j in range(3):
			f[i].append(randomVariable(n))
	return f

def printFormula(f, n, m):

	for idx,cl in enumerate(f):
		print "( ",
		if(cl[0] < n):
			print "x{} | ".format(cl[0]) , 
		else:
			print "!x{} | ".format(cl[0]-n) ,
		if(cl[1] < n):
			print "x{} | ".format(cl[1]), 
		else:
			print "!x{} | ".format(cl[1]-n),
		if(cl[2] < n):
			print "x{} )".format(cl[2]),
		else:
			print "!x{} )".format(cl[2]-n),
		if(idx != m - 1):
			print " & ",

def monteCarloSolve(f,n,m):

	randomAssignment = []

	for i in range(n):
		randomAssignment.append(random.choice([True, False]))
	for i in range(n):
		randomAssignment.append(not randomAssignment[i])

	satisfiedClauses = []

	for i in range(m):
		if(randomAssignment[f[i][0]] or randomAssignment[f[i][1]] or randomAssignment[f[i][2]] ):
			satisfiedClauses.append(i)

	# print "Number of satisfied clauses: ", len(satisfiedClauses)
	# print "Fraction of satisfied clauses: ", len(satisfiedClauses)/float(m)
	# print satisfiedClauses

	return len(satisfiedClauses) >= (7/8.)*m

def lasVegasSolve(f,n,m):

	done = False
	runCount = 0

	while(not done):
		done = monteCarloSolve(f,n,m)
		runCount += 1

	print "Number of calls to MC from Las Vegas: ", runCount

def derandomizedSolve(f,n,m):

	#Assigning
	assignment = []
	clauseStatus = []

	for i in range(m):
		clauseStatus.append(-1)

	for i in range(n):

		trueCount = 0
		falseCount = 0

		for idx,clause in enumerate(f):

			if(clauseStatus[idx] == -1):
				if(i in clause):
					trueCount += 1
				if(i+n in clause):
					falseCount += 1

		assignment.append(trueCount > falseCount)
		for idx,clause in enumerate(f):
			if(i + (trueCount <= falseCount)*n in clause):
				clauseStatus[idx] = 1

	for i in range(n):
		assignment.append(not assignment[i])

	#Checking
	satisfiedClauses = []

	for i in range(m):
		if(assignment[f[i][0]] or assignment[f[i][1]] or assignment[f[i][2]] ):
			satisfiedClauses.append(i)

	print "Number of satisfied clauses: ", len(satisfiedClauses)
	print "Fraction of satisfied clauses: ", len(satisfiedClauses)/float(m)	

def main():
	
	#Number of clauses
	m = 1000

	#Number of variables
	n = 1000

	formula = getRandomFormula(n,m)

	#printFormula(formula, n, m)
	#lasVegasSolve(formula,n,m)
	derandomizedSolve(formula,n,m)

if __name__ == '__main__':
	main()
