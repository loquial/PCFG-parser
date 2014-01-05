from PCKY import PCKYParser
import nltk
from nltk.corpus import treebank
from nltk import Tree
#nltk has a sample of the penn treebank (10%) and some other treebanks as well
#http://nltk.org/book/ch08.html
#use these to create a pcfg, unlexcialized, then annotated lexicalized?

#create counts of binary rules, unary rules and nonterminals
#ie: VP: V N 30 times
#N: cat
#ADJP 100


def CountTree(aTree, aCounts):
	#tree height of 2 means only leaves, ie terminals.
	aCounts[2][aTree.node] = aCounts[2].get(aTree.node,0) + 1
	if(aTree.height() == 2):
		if aTree.node not in aCounts[0]:
			aCounts[0][aTree.node] = dict()
		mySubDict = aCounts[0][aTree.node]
		mySubDict[aTree[0]] = mySubDict.get(aTree[0],0) + 1
	elif(len(aTree) > 1):	#binary rules
		if aTree.node not in aCounts[1]:
			aCounts[1][aTree.node] = dict()
		mySubDict = aCounts[1][aTree.node]
		mySubDict[(aTree[0].node,aTree[1].node)] = mySubDict.get((aTree[0].node, aTree[1].node), 0) + 1
		CountTree(aTree[0], aCounts)
		CountTree(aTree[1], aCounts)
	else:
		#collapse certain structures (like NP->NN->word)
		mySubTree = aTree[0]
		myNewTree = Tree(aTree.node+"+"+mySubTree.node,[mySubTree[0]])
		CountTree(myNewTree, aCounts)


def getPennCounts():
	#aCorpus is a nltk corpus object, index to get each sentence's tree
	#script to generate counts from corpus first
	theCorpusPrefix = "wsj_"
	theCorpusCount = 200
	theCorpusSuffix = ".mrg"
	sents = 0

	#unary rules, binary rules, nonterminals
	theCounts = [None] * 3
	theReverseCounts = [None]*2
	theCounts[0] = dict()
	theCounts[1] = dict()
	theCounts[2] = dict()

	for i in range(1,theCorpusCount):
		theCurrentCorpusTitle = theCorpusPrefix + ("0" * (4-len(str(i)))) + str(i) + theCorpusSuffix
		aCorpus = treebank.parsed_sents(theCurrentCorpusTitle)
		aSentCount = len(aCorpus)
		for j in range(aSentCount):
			myTree = aCorpus[j]
			CountTree(myTree, theCounts)
			sents = sents + 1
	return theCounts
def writeToFile(aCounts, aFileName):
	myFile = open(aFileName, 'w')
	for aN in aCounts[0]:
		for aResult in aCounts[0][aN]:
			myFile.write("%d UNARY %s %s\n" % (aCounts[0][aN][aResult], aN, aResult))
	for aN in aCounts[1]:
		for aResult in aCounts[1][aN]:
			myFile.write("%d BINARY %s %s %s\n" % (aCounts[1][aN][aResult], aN, aResult[0], aResult[1]))
	for aN in aCounts[2]:
		myFile.write("%d NONTERM %s\n" % (aCounts[2][aN], aN))

def readFromFile(aFileName):
	myFile = open(aFileName, 'r')
	myCounts = [dict(), dict(), dict()]
	for line in myFile:
		fields = line.strip().split(' ')
		n, ruleType, args = int(fields[0]), fields[1], fields[2:]
		if ruleType == 'NONTERM':
			myCounts[2][args[0]] = n
		elif ruleType == 'UNARY':
			if(args[0] not in myCounts[0]):
				myCounts[0][args[0]] = dict()
			myCounts[0][args[0]][args[1]] = n
		else: # BINARY
			if(args[0] not in myCounts[1]):
				myCounts[1][args[0]] = dict()
			myCounts[1][args[0]][tuple(args[1:])] = n
	return myCounts