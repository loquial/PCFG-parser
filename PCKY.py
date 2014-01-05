import nltk
from collections import defaultdict
#counts are a an array [unary, binary, nonterminals] of dicts

#Useful sources for understanding the algorithm: 
#https://en.wikipedia.org/wiki/Cyk_algorithm 
#https://en.wikipedia.org/wiki/Inside%E2%80%93outside_algorithm
#https://courses.cs.washington.edu/courses/cse590a/09wi/pcfg.pdf
class PCKYParser:
	def __init__(self, aCounts):
		self.UnaryCounts = aCounts[0]
		self.BinaryCounts = aCounts[1]
		self.NontermCounts = aCounts[2]
		pass
	def getUnaryProb(self, N, w):
		if N in self.UnaryCounts:
			return float(self.UnaryCounts[N].get(w, 0))/self.NontermCounts[N]
		return myNrules
	def getBinaryProb(self, N, wa, wb):
		if N in self.BinaryCounts:
			return float(self.BinaryCounts[N].get((wa,wb), 0))/self.NontermCounts[N]
	def parseSentence(self, aSent):
		myProbs = defaultdict(float)
		myWords = nltk.word_tokenize(aSent)
		myLength = len(myWords)
		myBPs = {}
		for i in range(myLength):
			if sum([self.UnaryCounts[X].get(myWords[i],0) for X in self.UnaryCounts]) < 4:
				myWord = '_RARE_'
			else:
				myWord = myWords[i]
			for aN in self.UnaryCounts:
				myProbs[i,i,aN] = self.getUnaryProb(aN, myWord)
		for spanLength in range(1,myLength):
			for spanStart in range(0,myLength-spanLength):
				spanEnd = spanStart + spanLength
				for aN in self.NontermCounts:
						myProb = 0
						myMaxProb = 0
						if aN in self.BinaryCounts:
							for (A, B) in self.BinaryCounts[aN]:
								for spanPart in range(spanStart, spanEnd):
									if(myProbs[spanStart,spanPart,A] and myProbs[spanPart+1,spanEnd,B]):
										myProb = self.getBinaryProb(aN, A, B) * myProbs[spanStart,spanPart,A] * myProbs[spanPart+1,spanEnd,B]
										if myProb > myMaxProb:
											myMaxProb = myProb
											myBP = (A, B, spanPart)
							if myMaxProb:
								myProbs[spanStart,spanEnd,aN] = myMaxProb
								myBPs[spanStart, spanEnd,aN] = myBP

		self.lastProbs = myProbs
		self.lastBPs = myBPs
		if (myProbs[0,myLength-1,'S']):
			return self.getParseTree(0,myLength-1,'S', myWords, myBPs)
		else:
			maxProb = 0
			bestN = ''
			for aN in self.NontermCounts:
				if (myProbs[0,myLength-1,aN]>maxProb):
					maxProb = myProbs[0, myLength-1, aN]
					bestN = aN
			return self.getParseTree(0, myLength-1, bestN, myWords, myBPs)

	def getParseTree(self, wa, wb, aN, aWords, aBPs):
		if wa==wb:
			return [aN, aWords[wa]]
		else:
			A, B, myPart = aBPs[wa, wb, aN]
			return [aN, self.getParseTree(wa, myPart, A, aWords, aBPs), self.getParseTree(myPart+1, wb, B, aWords, aBPs)]