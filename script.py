#!/usr/bin/python

#**************************************
# This Python Script accomplishes the following task:
#------------------------------------
# 1. This script takes a csv file as input file which has following pattern: ip,hostname
# 2. Script then tries to make a connection with port 22,25,80,110,443,8080,8008 (one by one).
# 3. Responses (Banner Response) to store in a text file or display on screen, in following pattern: ip, hostname, port, banner_response.
# 4. Banner could be ssh banner or smtp banner or http head response.
# 5. Input is csv and output should be in csv comaptible format which can either be stored in a text file or prefered to be displayed on screen.
# 6. The script has a port array at top where custom port numbers can be defined.
#------------------------------------
# This archive contains: sample input/output files as infile/ofile and script.
# Simply run this script (script.py) and Enjoy!.
# Tested on Ubuntu, Fedora, CentOs, Mac with Python version 2.7.3.
# Created by geeksScript | Sanchit (http://geeksScript.com), Dated: 04-04-2013.
#************************************** 

from __future__ import print_function
import csv, sys, os, time
import telnetlib, urllib2, socket
import os.path

#Port array (values can be added later)
ports=[22,25,80,110,443,8008,8080]

err=0;
try:
	print("Enter input file name: ",end="")
	inputf = raw_input()
	print("Enter output file name: ",end="")
	outf = raw_input()

	print("Checking if files exist..",end="")
	if ((os.path.isfile(inputf)) and (os.path.isfile(outf))) == False:
	        print("File(s) do not exist, Exiting")
       	else:
		print(" Files Exist")
		print("Processing! Please wait.. It may take time depending on your input file contents")
		ifile  = open(inputf, "r")
		reader = csv.reader(ifile)


		old_stdout = sys.stdout
		in_file = open(outf,"a")

		def blocked():
        		{
				print((ip + ", " + host + ", " + str(pno) + ", Connection Error/Port Blocked!"))
        		}

		try:
			for i in reader:
				ip= i[0]
				host= i[1]		
		
				for pno in ports:
					if pno == 80 or pno == 8008 or pno == 8080:
						try:
					        	sys.stdout = in_file
							tn = telnetlib.Telnet(ip,pno, 5)
        						tn.write(b"HEAD / HTTP/1.0\n")
        						tn.write(b"Host: host\n\n")
        						s = tn.read_all().replace('\r\n'," #")
        						print((ip + ", " + host + ", " + str(pno) + ", "),end="")
							print (s);
        						sys.stdout = old_stdout
						except:
							blocked();  
					elif pno == 443:
						try:
							sys.stdout = in_file
     							socket.setdefaulttimeout(6)
							request = urllib2.Request('https://'+ ip + ':443')
       							request.get_method = lambda : 'HEAD'
        						response = urllib2.urlopen(request)
        						ab = response.info()
							print((ip + ", " + host + ", " + str(pno) + ", "),end="")
        						print(str(ab).replace('\r\n', "#"))
							sys.stdout = old_stdout
						except:
        						blocked();
					else:
						try:
                        				sys.stdout = in_file 
                              				tn1 = telnetlib.Telnet(ip,pno, 5)
                              				tn1.write(b"quit")
                                       			z = tn1.read_until(b"\n", 1).replace('\r\n',"")
							print((ip + ", " + host + ", " + str(pno) + ", "),end="")
             	                      			print (z);
							sys.stdout = old_stdout
	                	       		except:
        	               	        		blocked();	
	
		except:
			print("Input File Error, Syntax should be: x.x.x.x,hostname");
			err=1;

finally:
	if ((os.path.isfile(inputf)) and (os.path.isfile(outf))) == False:
		sys.exit(1);
	
	elif err == 1:
		in_file.close();ifile.close();
		sys.exit(1);

	else:
		sys.stdout = old_stdout
		in_file.close();ifile.close();
		print("Completed.. Data saved in: "+ outf);
		print("Do you want to display contents of output file[y/N]:", end="");
		ans = raw_input();
		if ans == "y" or ans == "Y":
			print("Contents will be displayed with a line break:");time.sleep(2.5);
			f=open(outf,'r')
			for i in f:
				print(i);
			sys.exit(0);
		else:
                     	print("Bye")
			sys.exit(0);

