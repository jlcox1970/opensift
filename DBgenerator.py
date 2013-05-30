#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, subprocess

if __name__ == '__main__':
	logo_dir = 'logo'
	siftfeat = 'bin/siftfeat'
	databaseDirectory = 'CB'
	
	for fileOrDir in os.listdir(logo_dir):
		_fileOrDir = logo_dir + os.path.sep + fileOrDir
		if os.path.isdir(_fileOrDir):
			for idx, siftFile in enumerate(os.listdir(_fileOrDir)):
				devNull = open('/dev/null', 'w')
				filename = _fileOrDir + os.path.sep  + siftFile
				siftFilename = databaseDirectory + os.path.sep + fileOrDir + os.path.sep  + str(idx+1) + '.sift'
				try:
					print [siftfeat, filename, '-o'+siftFilename+'.sift', '-x']
					subprocess.check_call([siftfeat, filename, '-o', siftFilename, '-x'], stderr=devNull)
				except subprocess.CalledProcessError:
					print ':('

