#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, subprocess

class Maximum:
	def __init__(self):
		self._max = 0
	def add(self, val):
		if(val > self._max) :
			self._max = val
	def maximum(self):
		return self._max;

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
	
	def _makeCompStructure(self):
		compStructure = dict()
		for key in self._features.iterkeys():
			compStructure[key] = Maximum()
		return compStructure
	
	def _findBestMatch(self, matches):
		bestGroupName = None
		bestMax = -1;
		for group, maximum in matches.iteritems():
			if maximum.maximum() > bestMax:
				bestMax = maximum.maximum()
				bestGroupName = group
		return 'Propably it is ' + bestGroupName + ' (' + str(bestMax) + ' feats)'
	
	def match(self, filename):
		matches = self._makeCompStructure()
		basename = os.path.splitext(filename)[0]
		devNull = open('/dev/null', 'w')
		try:
			subprocess.check_call([self._siftfeat, filename, '-o'+basename+'.sift', '-x'], stderr=devNull)
		except subprocess.CalledProcessError:
			print 'Cannot open file'
			return ()
		
		for group, files in self._features.iteritems():
			print group
			for file in files:
				try:
					val = int(subprocess.check_output([self._comparator, file, basename+'.sift'], stderr=devNull).strip())
					matches[group].add(val)
					print 'Result: ' + str(val)
				except subprocess.CalledProcessError:
					pass
		os.remove(basename + '.sift')
		
		return self._findBestMatch(matches)


if __name__ == '__main__':
	matcher = SiftMatcher('CB')
	
	print matcher.match(sys.argv[1])
