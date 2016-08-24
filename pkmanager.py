#!/usr/bin/env python

import os, sys
from sys import *
import argparse

## Author: Victor Huang, victorhuangpro@gmail.com
##  Aug 23, 2016
## system reserved keywords can be added on later
system_keywords = ["INSTALL", "REMOVE", "LIST", "BROWSER", "DEPEND", "DNS", "HTML", "NETCARD", "TCPIP", "TELNET" ] #, "HELP", "CLEANALL"] 
depend_dict = {}     ## for each real-time parsing for "DEPEND" command, add here dynamically
parent_dict = {}
installed_module = []  ## maintain module: append when install, delete when remove 
input_lines = []  ## keep back track of each line input, in case later cross reference or 
                     ## new features like history feature added on later.
def list_mode( ):
  for item in installed_module:
    print item 
  #print "list!...." 

def depend_mode( words ):
  if len(words) < 2:
    print "depend takes at least 2 operand !"
    return 1
  for ii in range( 2, len(words)):
    if words[ii] not in parent_dict:
      parent_dict[words[ii]] = []
      parent_dict[words[ii]].append( words[1]) # any key in parent_dict has kids dependency 
    else:
      parent_dict[words[ii]].append( words[1]) # any key in parent_dict has kids dependency 

    if words[1] not in depend_dict:
      depend_dict[words[1]] = []  ## init first time 

      depend_dict[words[1]].append( word[ii] )   
    else:
      depend_dict[words[1]].append( word[ii] )   

  return 0

def install_mode( words ):
  if len(words) < 2:
     print "install command must follow by a  module!" 
     return 1 

  for ii in range( 1, len(words)):
    if words[ii] not in installed_module:
      if words[ii] in depend_dict:
        plist = depend_dict[words[ii]] 
        for item in plist:
          if item not in installed_module:
            print "installing " + item
            installed_module.append(item)

      print "installing " + words[ii]
      installed_module.append(words[ii])
  return 0

def remove_mode( words ):
  if len(words) < 2:
     print "remove command must follow by a  module!" 
     return 1

  for ii in range( 1, len(words)):
    if words[ii] not in installed_module:
      print "not yet install, ignoring removal for " + words[ii]
      continue 
    if words[ii] in parent_dict:
       #installed_module.remove(words[ii])
       print words[ii]+" is still required !"
    else:
       print words[ii]+" removed."
       installed_module.remove(words[ii])
       print parent_dict
       print depend_dict

def do_oneline( readline ):
  words = readline.split()
  if words[0] not in system_keywords:
    print "command <"+words[0]+"> unrecognized."
  else:
     print readline
     if "DEPENDS" == words[0]:
      depend_mode( words )
     if "INSTALL" == words[0]:
       install_mode( words )
     
     if "HELP" == words[0]:
      help_mode( words )
     if "REMOVE" == words[0]:
      remove_mode( words )
     if "LIST" == words[0]:
      list_mode(  )
     if "CLEANALL" == words[0]:
      cleanall_mode( words )

def interactive():
 in_ii = 0
 while True:
    print "\n>"

    readline = sys.stdin.read() #vline
    readline = readline.strip()  ## error tolerant for extra space at line beginging and ending 
    input_lines [in_ii] = readline 
    do_oneline( readline )


def batch_test(filename) : 
  outf = open( filename+".log.txt", "w") 
  lines0 = open( filename, "r").readlines()
  lines = [ line.strip() for line in lines0 ]
  for ii in range( 0, len(lines) ):
    outf.write( "\n>" ) 
    readline = lines[ii]   ## error tolerant for extra space at line beginging and ending 
    if 0 == len(readline): 
      continue
    do_oneline( readline )
  outf.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", type=str, default="i",
                        help="interactive==product mode")
    parser.add_argument("--batchtest mode, use with fileinput", type=str, default="batch",                        help="batch file contains serialized files simulating input stream")

    parser.add_argument("--batch-filename", type=str, default="batch_input.txt",
                        help="interactive==product mode")
    
    args = parser.parse_args()
    #------------
    batch_test( "batch_input.txt" )
    #interactive()

    

