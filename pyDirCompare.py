'''
Created on 19 Oct 2012
@author: J.A. Simmons V
Program to crawl two similar directory structors and report on the differences

v1.0
in this version, we realized that the default structure contained all base files and second structure only contained
the changed files. This allowed a much simpler calculation that did not require comparing the two data structures.
'''

import os
from os.path import join, getsize
import shutil
import hashlib
import threading
import Queue
import time
paths = ['C:\\Temp\\test1\\','C:\\Temp\\test2\\']
originalKeyword = 'test1'#'Set your keyword here' #a keyword in the path of which is the original directory to measure against
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
	  files, total, root = crawlDir(self.dir)
	  self.out_queue.put([files, total, root])
	  self.queue.task_done()

class treeFiles:
    #default constructor to build require tree
    def __init__(self, name, size, hashed):
        self.name = name
        self.hashed = hashed
        self.size = float(size)

def crawlDir(dir):
    retFiles = []
    total = 0
    totalFiles = 0
    parent = ''
    for root, dirs, files in os.walk(dir):
        for f in files:
            if len(parent)==0:parent=root
            e = join(root, f)
            s = getsize(e)
            m = hashlib.md5()
            m.update(open(e).read())
            retFiles.append(treeFiles(e, s, m.digest()))
            total += s
            totalFiles +=1
    return retFiles, total, parent

#compare() will take the modified file structure and compare against the original file structure
#will only find that which is similar and retruns the final byte size of all the same files
def compare(originalStruct, modifiedStruct):
  matched = []
  sameSize = 0
  for x in modifiedStruct:
    for i in [i for i,y in enumerate(originalStruct) if y.hashed==x.hashed]:
      matched.append(x)
      sameSize = sameSize+x.size
  return sameSize
  
'''
*************************************************************************************************
**********************************  Main  *******************************************************
*************************************************************************************************
'''
print "Crawling..."
files=[] #holder to grab the processed files out of the queue
start = time.time()#when the heavy lifting started
#kick off all the threads
for i in range(len(paths)):
  t = CrawlThread(queue, out_queue)
  t.setDaemon(True)
  t.start()
#add the required items into the queue
  for path in paths:
    queue.put(path)
#wait for the queues to finish being processed before moving on
queue.join()

print 'Processing...'
while not out_queue.empty():#grab all the files out of the queue
	files.append(out_queue.get(True))
if files[0][2].find(originalKeyword)>=0:#if the original structure is in the first set of files
  #sameSize = compare(files[0][0],files[1][0])
  print '1: '+str(files[0][1])
  print '2: '+str(files[1][1])
  print str(((files[1][1]+files[0][1])/float(files[0][1]))*100)+'% difference in bytes'
elif files[1][2].find(originalKeyword)>=0:#if original structure is in the second set of files
  print '1: '+str(files[1][1])
  print '2: '+str(files[0][1])
  print str(((files[1][1]+files[0][1])/float(files[1][1]))*100)+'% difference in bytes'
else: #otherwise an error happened
  print 'Error - neither path is found as the original'  
print "Elapsed Time: %s" % (time.time() - start)
quit()
