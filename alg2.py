#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, subprocess, math

class Averager:
	def __init__(self):
		self._sum = 0.
		self._count = 0
		self._array = []
		
	def add(self, val):
		self._sum += val
		self._array.append(val)
		self._count += 1
	
	def avg(self):
		return round(self._sum / self._count, 2) if self._count > 0 else 0
	
	def stdev(self):
		if self._count > 0:
			mean = self._sum / self._count
			sum2 = sum([ (mean - x)**2 for x in self._array])
			return math.sqrt(sum2 / self._count)
	def maxVal(self):
		return max(self._array) if len(self._array) > 0 else 0

class SiftMatcher:
	def __init__(self, databaseDirectory):
		self._databaseDirectory = databaseDirectory
		self._features = dict()
		self._addSifts()
		self._comparator = 'bin/comp'
		self._siftfeat = 'bin/siftfeat'

	def _addSifts(self):
		for fileOrDir in os.listdir(self._databaseDirectory):
			_fileOrDir = self._databaseDirectory + os.path.sep + fileOrDir
			if os.path.isdir(_fileOrDir):
				self._features[fileOrDir] = []
				for siftFile in os.listdir(_fileOrDir):
					self._features[fileOrDir].append(_fileOrDir + os.path.sep  + siftFile)
	
	def makeCompStructure(self):
		compStructure = dict()
		for key in self._features.iterkeys():
			compStructure[key] = Averager()
		return compStructure
	
	def _findBestMatch(self, matches, strategy):
		if strategy == 'max':
			bestGroupName = None
			bestAvg = -1;
			for group, avg in matches.iteritems():
				if avg.maxVal() > bestAvg:
					bestAvg = avg.maxVal()
					bestGroupName = group
			return (bestGroupName, bestAvg)
		elif strategy == 'avg':
			bestGroupName = None
			bestAvg = -1;
			for group, avg in matches.iteritems():
				if avg.avg() > bestAvg:
					bestAvg = avg.avg()
					bestGroupName = group
			return (bestGroupName, bestAvg)
		elif strategy == 'stdev':
			bestGroupName = None
			bestAvg = -1;
			for group, avg in matches.iteritems():
				if avg.stdev() > bestAvg:
					bestAvg = avg.stdev()
					bestGroupName = group
			return (bestGroupName, round(bestAvg, 2))
		elif strategy == 'avg-stdev':
			ranking = []
			for group, avg in matches.iteritems():
				ranking.append((group, avg))
			ranking.sort(key=lambda tup: -(tup[1]).avg())
			
			ranking = [ (group, avg.stdev()) for group, avg in ranking[:3]]
			ranking.sort(key=lambda tup: -tup[1])
			return (ranking[0][0], round(ranking[0][1], 2))
		elif strategy == 'stdev-avg':
			ranking = []
			for group, avg in matches.iteritems():
				ranking.append((group, avg))
			ranking.sort(key=lambda tup: -(tup[1]).stdev())
			
			ranking = [ (group, avg.avg()) for group, avg in ranking[:3]]
			ranking.sort(key=lambda tup: -tup[1])
			return (ranking[0][0], ranking[0][1])
		else:
			raise Exception('No strategy')
	
	def match(self, filename, strategy = 'avg'):
		matches = self.makeCompStructure()
		basename = os.path.splitext(filename)[0]
		devNull = open('/dev/null', 'w')
		try:
			subprocess.check_call([self._siftfeat, filename, '-o'+basename+'.sift', '-x'], stderr=devNull)
		except subprocess.CalledProcessError:
			print 'Cannot open file'
			return ()
		
		for group, files in self._features.iteritems():
			for file in files:
				try:
					val = int(subprocess.check_output([self._comparator, file, basename+'.sift'], stderr=devNull).strip())
					matches[group].add(val)
				except subprocess.CalledProcessError:
					pass
		os.remove(basename + '.sift')
		return self._findBestMatch(matches, strategy)


if __name__ == '__main__':
	matcher = SiftMatcher('CB')
	
	print matcher.match(sys.argv[1])
