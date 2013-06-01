#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, subprocess
from alg2 import SiftMatcher

if __name__ == '__main__':
	tests_dir = 'tests'
	databaseDirectory = 'CB'
	
	matcher = SiftMatcher(databaseDirectory)
	
	for fileOrDir in os.listdir(tests_dir):
		_fileOrDir = tests_dir + os.path.sep + fileOrDir
		if os.path.isdir(_fileOrDir):
			for siftFile in os.listdir(_fileOrDir):
				if not siftFile.startswith('.'):
					print fileOrDir,siftFile,
					print matcher.match(_fileOrDir + os.path.sep  + siftFile)

