'''
Created on 19 Oct 2012

@author: J.A. Simmons V
Program to crawl two similar directory structors and report on the differences
'''

import os
from os.path import join, getsize
import shutil
import hashlib
import threading
import Queue
import time
#paths = ['C:\\Temp\\test1\\','C:\\Temp\\test2\\']
paths = ['C:\\Program Files\\Loansoft\\Default\\Production','C:\\Program Files\\Loansoft\\Cornerstone\\PRODUCTION']
queue = Queue.Queue()
out_queue = Queue.Queue()

class CrawlThread(threading.Thread):
  def __init__(self, queue, out_queue):
    threading.Thread.__init__(self)
    self.queue = queue
    self.out_queue = out_queue

  def run(self):
    while True:
	  #grabs host from queue
	  self.dir = self.queue.get()
	  files, total = crawlDir(self.dir)
	  self.out_queue.put([files, total])
	  self.queue.task_done()

class treeFiles:

    #default constructor to build require tree
    def __init__(self, name, size, hashed):
        self.name = name
        self.hashed = hashed
        self.size = size

def crawlDir(dir):
    retFiles = []
    total = 0
    totalFiles = 0
    for root, dirs, files in os.walk(dir):
        for f in files:
            e = join(root, f)
            s = getsize(e)
            m = hashlib.md5()
            m.update(open(e).read())
            retFiles.append(treeFiles(e, s, m.digest()))
            total += s
            totalFiles +=1
    return retFiles, total

def compare(dir1, dir2):
  matched = []
  sameSize = 0
  if len(dir1) >= len(dir2):
	greater = dir1
	less = dir2
  else: 
    greater = dir2
    less = dir1
  for x in less:
    for i in [i for i,y in enumerate(greater) if y.hashed==x.hashed]:
      matched.append(x)
      sameSize = sameSize+abs(y.size - x.size)
  return sameSize
  
print "Crawling..."
dirFiles = []
dirTotal = []
files=[]
count = len(paths)
start = time.time()
for i in range(len(paths)):
  t = CrawlThread(queue, out_queue)
  t.setDaemon(True)
  t.start()
  for path in paths:
    queue.put(path)
queue.join()
files=[]
print 'Processing...'
while not out_queue.empty():
	files.append(out_queue.get(True))
sameSize = compare(files[0][0],files[1][0])
print 'File 1:'+str(files[0][1])+' Diff: '+str(files[0][1]-sameSize)
print 'File 2:'+str(files[1][1])+' Diff: '+str(files[1][1]-sameSize)
print 'FLIP-----------------'
sameSize = compare(files[1][0],files[0][0])
print 'File 1:'+str(files[0][1])+' Diff: '+str(files[0][1]-sameSize)
print 'File 2:'+str(files[1][1])+' Diff: '+str(files[1][1]-sameSize)

print "Elapsed Time: %s" % (time.time() - start)
'''results = []
for e in dir1Files:
    for e in dir2Files:
        print True
print dir1+' = '+str(dir1Total)
print dir2+' = '+str(dir2Total)
print (float((dir2Total-dir1Total))/float(dir1Total))*100
print "Done!"'''
