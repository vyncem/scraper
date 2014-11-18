#!/usr/bin/python

##
## Script targets a webpage and retrieves link hrefs based on a filter.
## arguments: URL, filter
##

import re
import sys
from bs4 import BeautifulSoup
import subprocess

def getPage(link):
    cmdWget = "wget -q " + link
    p = subprocess.Popen(cmdWget, shell=True, stderr=subprocess.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()


def getFiles():
    cmdList = "ls [0-9]*"
    p = subprocess.Popen(cmdList, shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()

#    p = subprocess.Popen(cmdList, shell=True, stderr=subprocess.PIPE)
#    while True:
#        out = p.stderr.read(1)
#        if out == '' and p.poll() != None:
#            break
#        if out != '':
#            sys.stdout.write(out)
#            sys.stdout.flush()

    return output.split('\n')

def getEmail(file):
    try:
        soup = BeautifulSoup(open(file))
    except:
        return "No such file: " + file

    links = soup('a')
    
    refs=[]
    for link in links:
        refs.append(link.get('href'))
        
    try:        
        reg=re.compile('^mailto')
        result = (filter(reg.match, refs)[0]).split(':')[1]
    except:
        result = file

    return result


def getLinks(file):
    soup = BeautifulSoup(open(file))
    links = soup('a')

    refs=[]
    for link in links:
        refs.append(link.get('href'))


    reg=re.compile('^https://zen*')
    result = filter(reg.match, refs)
        
    return result

if __name__ == "__main__":
    file = "CoderDojo Zen.html"
    links = getLinks(file)

    for link in links:
        getPage(link)
 
    files = getFiles()
  
    for file in files:
        print (getEmail(file))
    
    
