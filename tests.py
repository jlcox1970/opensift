#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alg2 import SiftMatcher

import os, sys, subprocess
import threading

def runTestCase(group, siftFile, filename):
	result = matcher.match(filename)
	print group, siftFile, result


if __name__ == '__main__':
	tests_dir = 'tests'
	databaseDirectory = 'CB'
	
	matcher = SiftMatcher(databaseDirectory)
	
	for fileOrDir in os.listdir(tests_dir):
		_fileOrDir = tests_dir + os.path.sep + fileOrDir
		if os.path.isdir(_fileOrDir):
			for siftFile in os.listdir(_fileOrDir):
				if not siftFile.startswith('.') and not siftFile.endswith('.sift'):
					thread = threading.Thread(target=runTestCase, args=(fileOrDir, siftFile, _fileOrDir + os.path.sep  + siftFile))
					thread.start()

