# GoogleSearchEngine

Mimic Google's search engine using python, html, and css.

This was a project done for the CSC326: Programming Languages Course.
We re-created Google's Search engine by using Bottle.

The project contains the following:

1. aws_setup.py - AWS one-click deployment script
2. aws_terminate.py - AWS instance termination script
3. frontend.py - Frontend implementation 
4. client_secret_346297252987-gessg0ftmins8qrsdkkh8lgv9ask1occ.apps.googleusercontent.com.json
5. crawler.py: Crawler implementation built on top of starter code.
6. dump.rdb - Database file containing results from crawler
7. dump.json - json file with data from database 
8. urls.txt - URLs for testing crawler functionality
9. credentials_template.csv
10. error.tpl - Template for error page 
11. homepage.tpl - Template for homepage page 
12. homepageanon.tpl - Template for homepage page 
13. pagination.tpl - Template for results page 
14. paginationAnon.tpl - Template for results page 
15. run_backend_test.py - Backend tests
16. my_key.pem - key for AWS
17. style.css
18. group24_csc326_2018.pdf - Final Report

# Lab 4

AWS:

To run aws_setup.py, my_key.pem, credentials.csv, and lab4_group_24.tar.gz (must be named this with a folder called GoogleSearchEngine-master inside that contains a file called frontend.py with the frontend implementation). The credentials.csv file should be similar to the credentials_template.csv file. 

# Lab 2

AWS:

Instance created: Monday, November 12, 2018
Instance Terminated!

Public IP address of live web server: 54.161.255.192

Public DNS: ec2-54-161-255-192.compute-1.amazonaws.com   

To view search engine, go to http://54.161.255.192:80/ or http://ec2-54-161-255-192.compute-1.amazonaws.com.

Benchmark Setup:

1. Used the following commands on Ubuntu:

a. sudo apt-get install apache2-utils

b. sudo apt-get install sysstat dstat

2. On another computer, used this command: ab -n 1000 -c 50 http://35.172.205.127:80/?keywords=csc326+lab2

3. On Ubuntu, used this command to get utilization of CPU, memory, disk IO,
   and network when max performance is sustained: dstat -cmdn

Benchmarking results can be found in RESULT file.

# Lab 3

AWS:

Instance created: Wednesday, November 28, 2018

Public IP address of live web server: 54.145.203.98

Public DNS: ec2-54-145-203-98.compute-1.amazonaws.com 

To view search engine, go to http://54.145.203.98:80/ or http://ec2-54-145-203-98.compute-1.amazonaws.com.

Benchmark Setup:

1. Used the following commands on Ubuntu:

a. sudo apt-get install apache2-utils

b. sudo apt-get install sysstat dstat

2. On another computer, used this command: ab -n 1000 -c 50 http://54.161.255.192:80/?keywords=csc326+ece

Benchmarking results can be found in LAB3RESULTS file.

Frontend:

The frontend searches the keywords against the persistent storage generated by the backend by converting dump.rdb to a json file (dump.json). The rdb file is converted to a json file using the command 'rdb --command json dump.rdb'. To use this command, rdbtools must be installed using 'pip install rdbtools python-lzf'. The frontend parses this json file to get the URLs, and these URLs are displayed using static pagination.

Information on how to access the frontend on AWS and the Public DNS of the frontend on AWS will be provided when marking for this lab starts.

The frontend from lab 2 can be found at http://54.161.255.192:80/ or http://ec2-54-161-255-192.compute-1.amazonaws.com.

Backend:
To run the backend to test for the pagerank functionality, run on terminal the commands:
redis-server
python run_backend_test.py (MAC & LINUX)

Command 1 will start up the redis server so that you can persistently store the data structures used in crawler.
Command 2 will run the code in the python file, which crawls through the urls listed in url.txt and stores the necessary information from Lab 1. It then calls the pagerank.py file given in class and computes the pages ranks of the links that were craled through, pretty-printing them.

Any time you want to use the pagerank function, call the crawler_page_ranks method in the crawler class, which will calculate the page ranks of the urls for you.

The search engine from lab 3 can be found at http://54.145.203.98:80/ or http://ec2-54-145-203-98.compute-1.amazonaws.com.

