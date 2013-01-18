19 Oct 2012
@author: J.A. Simmons V

pyDirCompare.py

This is a small python script that I created in order to compare two directory structures and byte-wise compare them to determine what percentage has been changed/customized.

A variable is called named 'paths' that contain the two directories to compare, and uses the variable 'originalKeyword' to later determine which path is the original path. This after-the fact determination is because I wrote this script to be threaded and since the threads could finish at different times, I wanted a way to determine which results were from which thread.