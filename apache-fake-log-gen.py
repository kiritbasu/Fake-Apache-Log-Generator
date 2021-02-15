#!/usr/bin/python
import time
import datetime
import pytz
import numpy
import random
import gzip
import zipfile
import sys
import argparse
from faker import Faker
from random import randrange
from tzlocal import get_localzone
local = get_localzone()

#todo:
# allow writing different patterns (Common Log, Apache Error log etc)
# log rotation


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT", choices=['LOG','GZ','CONSOLE'] )
parser.add_argument("--log-format", "-l", dest='log_format', help="Log format, Common or Extended Log Format ", choices=['CLF','ELF'], default="ELF" )
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int, default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)
parser.add_argument("--sleep", "-s", help="Sleep this long between lines (in seconds)", default=0.0, type=float)
parser.add_argument("--repeat", "-r", dest='repeat', help="Repeat the fake log function 1 to N", type=int, default=1)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type
log_format = args.log_format
repeat = args.repeat

faker = Faker()

response=["200","404","500","301"]

verb=["GET","POST","DELETE","PUT"]

resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

def create_log(log_lines):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	otime = datetime.datetime.now()

	outFileName = 'access_log_'+timestr+'.log' if not file_prefix else file_prefix+'_access_log_'+timestr+'.log'

	for case in switch(output_type):
		if case('LOG'):
			f = open(outFileName,'w')
			break
		if case('GZ'):
			f = gzip.open(outFileName+'.gz','w')
			break
		if case('CONSOLE'): pass
		if case():
			f = sys.stdout
	flag = True
	while (flag):
		if args.sleep:
			increment = datetime.timedelta(seconds=args.sleep)
		else:
			increment = datetime.timedelta(seconds=random.randint(30, 300))
		otime += increment

		ip = faker.ipv4()
		dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
		tz = datetime.datetime.now(local).strftime('%z')
		vrb = numpy.random.choice(verb,p=[0.6,0.1,0.1,0.2])

		uri = random.choice(resources)
		if uri.find("apps")>0:
			uri += str(random.randint(1000,10000))

		resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
		byt = int(random.gauss(5000,50))
		referer = faker.uri()
		useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
		if log_format == "CLF":
			f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s\n' % (ip,dt,tz,vrb,uri,resp,byt))
		elif log_format == "ELF": 
			f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip,dt,tz,vrb,uri,resp,byt,referer,useragent))
		f.flush()

		log_lines = log_lines - 1
		flag = False if log_lines == 0 else True
		if args.sleep:
			time.sleep(args.sleep)

for x in range(repeat):
	create_log(log_lines)