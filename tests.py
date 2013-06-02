#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alg2 import SiftMatcher

import os, sys, subprocess
import threading, multiprocessing

def runTestCase(threadLimiter, group, siftFile, filename):
	threadLimiter.acquire()
	try:
		result = matcher.match(filename)
		print group, siftFile, result
	finally:
		threadLimiter.release()
		

if __name__ == '__main__':
	tests_dir = 'tests'
	databaseDirectory = 'CB'
	
	matcher = SiftMatcher(databaseDirectory)
	threadLimiter = threading.BoundedSemaphore(multiprocessing.cpu_count())
	
	for fileOrDir in os.listdir(tests_dir):
		_fileOrDir = tests_dir + os.path.sep + fileOrDir
		if os.path.isdir(_fileOrDir):
			for siftFile in os.listdir(_fileOrDir):
				if not siftFile.startswith('.') and not siftFile.endswith('.sift'):
					args = (threadLimiter, fileOrDir, siftFile, _fileOrDir + os.path.sep  + siftFile)
					thread = threading.Thread(target=runTestCase, args=args)
					thread.start()

