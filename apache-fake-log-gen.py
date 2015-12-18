#!/usr/bin/python
import time
import datetime
import pytz
import random
import gzip
import sys
import argparse
from faker import Faker
from random import randrange

#todo:
# - generate Gaussian distribution of responses and verbs
# - allow writing different patterns (Common Log, Custom log, error log etc)
# - log rotation

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
parser.add_argument("--output", "-o", dest='output_type', help="Output [.Log File,.gz File,Console]", choices=['LOG','GZ','CONSOLE'] )
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate", type=int, default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="File Prefix", type=str)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type

faker = Faker()

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

response=["200","404","500","301"]

verb=["GET","POST","DELETE","PUT"]

resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.opera, faker.internet_explorer, faker.chrome, faker.safari]

for i in xrange(0,log_lines):
	increment = datetime.timedelta(seconds=random.randint(30,300))
	otime += increment

	ip = faker.ipv4()
	dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
	tz = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%z')
	vrb = random.choice(verb)

	uri = random.choice(resources)
	if uri.find("apps")>0:
		uri += `random.randint(1000,10000)`

	resp = random.choice(response)
	byt = random.randint(1000,10000)
	referer = faker.uri()
	useragent = random.choice(ualist)()
	f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip,dt,tz,vrb,uri,resp,byt,referer,useragent))
