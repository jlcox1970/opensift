#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, subprocess

class Averager:
	def __init__(self):
		self._sum = 0
		self._count = 0
		
	def add(self, val):
		self._sum += val
		self._count += 1
	
	def avg(self):
		return self._sum / self._count if self._count > 0 else 0

class SiftMatcher:
	def __init__(self, databaseDirectory):
		self._databaseDirectory = databaseDirectory
		self._features = dict()
		self._addSifts()
		self._comparator = 'bin/comp'

	def _addSifts(self):
		for fileOrDir in os.listdir(self._databaseDirectory):
			_fileOrDir = self._databaseDirectory + os.path.sep + fileOrDir
			if os.path.isdir(_fileOrDir):
				self._features[fileOrDir] = []
				for siftFile in os.listdir(_fileOrDir):
					self._features[fileOrDir].append(_fileOrDir + os.path.sep  + siftFile)
	
	def _makeCompStructure(self):
		compStructure = dict()
		for key in self._features.iterkeys():
			compStructure[key] = Averager()
		return compStructure
	
	def _findBestMatch(self, matches):
		bestGroupName = None
		bestAvg = -1;
		for group, avg in matches.iteritems():
			if avg.avg() > bestAvg:
				bestAvg = avg.avg()
				bestGroupName = group
		return (bestGroupName, bestAvg)
	
	def match(self, filename):
		matches = self._makeCompStructure()
		
		for group, files in self._features.iteritems():
			for file in files:
				try:
					val = int(subprocess.check_output([self._comparator, file, filename], stderr=subprocess.STDOUT).strip())
					matches[group].add(val)
				except subprocess.CalledProcessError:
					pass
		return self._findBestMatch(matches)


if __name__ == '__main__':
	matcher = SiftMatcher('CB')
	
	print matcher.match(sys.argv[1])
