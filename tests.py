#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alg2 import SiftMatcher, Averager

import os, sys, subprocess
import threading, multiprocessing

class TestCase(threading.Thread):
	def __init__(self, threadLimiter, matches, matcher, group, siftFile, filename):
		super(TestCase, self).__init__()
		self.threadLimiter = threadLimiter
		self.matches = matches
		self.matcher = matcher
		self.group = group
		self.siftFile = siftFile
		self.filename = filename

	def run(self):
		self.threadLimiter.acquire()
		try:
			result = self.matcher.match(self.filename)
			if self.group == result[0]:
				self.matches[self.group].add(1)
			else:
				self.matches[self.group].add(0)
			print self.group, self.siftFile, result
		finally:
			self.threadLimiter.release()
		

if __name__ == '__main__':
	tests_dir = 'tests'
	databaseDirectory = 'CB'
	
	matcher = SiftMatcher(databaseDirectory)
	threadLimiter = threading.BoundedSemaphore(multiprocessing.cpu_count())
	matches = matcher.makeCompStructure()
	threads = []
	
	print 'TEST CASES'
	print '---------------------------------------'
	
	for fileOrDir in os.listdir(tests_dir):
		_fileOrDir = tests_dir + os.path.sep + fileOrDir
		if os.path.isdir(_fileOrDir):
			for siftFile in os.listdir(_fileOrDir):
				if not siftFile.startswith('.') and not siftFile.endswith('.sift'):
					thread = TestCase(threadLimiter, matches, matcher, fileOrDir, siftFile, _fileOrDir + os.path.sep  + siftFile)
					thread.start()
					threads.append(thread)
	
	[x.join() for x in threads]
	
	print '\nRESULTS'
	print '---------------------------------------\n'*2
	
	results = dict((group, str(round(avg.avg()*100, 2))+'%') for group, avg in matches.iteritems() if avg._count > 0)
	print results
	
	sum = 0
	for avg in matches.itervalues():
		sum += avg.avg()
	print 'avg:', str(round(sum/len(results)*100, 2))+'%'
