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

def normalize_url(url):
    if url.startswith("http://"):
        url = "https://" + url[7:]
    elif not url.startswith("https://"):
        url = "https://" + url

    return url

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        try:
            yield self.match
        except StopIteration:
            return

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

parser.add_argument("--domain","-d", help="domain of current website", type=str, default='domain.com')
parser.add_argument("--min_ip", help="minimum value to before changing IP",type=int,default=1)
parser.add_argument("--max_ip", help="maximum value to before changing IP",type=int,default=4)
parser.add_argument("--auth_page",help="Authentification page, script will post this page.", default="/auth")
parser.add_argument("--register_page",help="Authentification page, script will post this page.", default="/register")

parser.add_argument('--datetime',help="The timestamp marking the initiation of log entries, regardless of whether it falls in the past or the future.", default=datetime.datetime.now(), type=lambda s: datetime.datetime.strptime(s, '%Y%m%d-%H%M%S'),)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type
log_format = args.log_format


domain = normalize_url(args.domain)
min_ip = args.min_ip
max_ip = args.max_ip
auth_page = args.auth_page
register_page = args.register_page

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = args.datetime

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

verb=["GET","POST"]

resources=["/","/register","/articles","/printed-books","/membership","/events","/events/event?id=","/search/tag/","/auth","/posts/posts/explore","/wp-content/cart.php?id="]
categories = ["Fiction","Non-Fiction","Mystery","Science Fiction","Fantasy","Romance","Historical Fiction","Biography","Autobiography","Self-Help","Travel","Cooking","Health","History","Science","Philosophy","Religion","Art","Music","Sports","Children's","Young Adult","Poetry","Drama","Comics","Graphic Novels","Business","Economics","Psychology","Education","Technology","Reference","Politics","Crime","Horror","Thriller","Adventure","Memoir"]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

flag = True
count=0
ip=""
useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
sameIP = 2
while (flag):
    if args.sleep:
        increment = datetime.timedelta(seconds=args.sleep)
    else:
        increment = datetime.timedelta(seconds=random.randint(30, 300))
    otime += increment
    if not ip: 
        ip = faker.ipv4()
        useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
        referer = faker.uri()
        sameIP = random.randint(min_ip, max_ip)
        count = 0
    elif count%sameIP == 0:
        ip = faker.ipv4()
        useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
        referer = faker.uri()
        sameIP = random.randint(min_ip, max_ip)
        count = 0
    else:
        referer = domain + uri # get last url

    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    vrb = numpy.random.choice(verb,p=[0.8,0.2])

    uri = random.choice(resources)
    if uri.find("id=")>0:
        uri += str(random.randint(10,3400))
    if uri.find("/tag/") > 0:
        uri += random.choice(categories)
    if uri.find(auth_page)>=0 or uri.find(register_page)>=0:
        resp = "POST"
    else:
        resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
    byt = int(random.gauss(5000,50))
    if log_format == "CLF":
        f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s\n' % (ip,dt,tz,vrb,uri,resp,byt))
    elif log_format == "ELF": 
        f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip,dt,tz,vrb,uri,resp,byt,referer,useragent))
    f.flush()

    log_lines = log_lines - 1
    flag = False if log_lines == 0 else True
    if args.sleep:
        time.sleep(args.sleep)
    count+=1
