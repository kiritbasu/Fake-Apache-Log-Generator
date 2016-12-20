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


# todo:
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
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT",
                    choices=['LOG', 'GZ', 'CONSOLE'])
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int,
                    default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()

outFileName = 'access_log_' + timestr + '.log' if not file_prefix else file_prefix + '_access_log_' + timestr + '.log'

for case in switch(output_type):
    if case('LOG'):
        f = open(outFileName, 'w')
        break
    if case('GZ'):
        f = gzip.open(outFileName + '.gz', 'w')
        break
    if case('CONSOLE'): pass
    if case():
        f = sys.stdout

response = ["200", "404", "500", "301"]

verb = ["GET", "POST", "DELETE", "PUT"]

resources = [
    "/p.php?e_c=Experience%20viewed&e_a=5846826ee4b09dde5a4b63c1&e_n=1%3B5846826ee4b09dde5a4b638d%3B&idsite=3&rec=1&r=069623&h=12&m=10&s=21&url=http%3A%2F%2Fwww.weirdfish.co.uk%2Fadvent-calendar%2Fkitvision%3Futm_source%3DWeird%20Fish%20Ltd%26utm_medium%3Demail%26utm_campaign%3D7812928_Advent%20Day%207%20T%20shirts%26utm_content%3DCompetition%26dm_i%3D277I%2C4NGHS%2COH3ODU%2CHCD9B%2C1&urlref=http%3A%2F%2Fwww.weirdfish.co.uk%2Fadvent-calendar%2Fkitvision%3Futm_source%3DWeird%20Fish%20Ltd%26utm_medium%3Demail%26utm_campaign%3D7812928_Advent%20Day%207%20T%20shirts%26utm_content%3DCompetition%26dm_i%3D277I%2C4NGHS%2COH3ODU%2CHCD9B%2C1&_id=0d5e80bb69e91d3b&_idts=1481112621&_idvc=1&_idn=0&_rcn=7812928_Advent%20Day%207%20T%20shirts&_refts=1481112621&_viewts=1481112621&send_image=0&pdf=1&qt=0&realp=0&wma=0&dir=0&fla=1&java=0&gears=0&ag=0&cookie=1&res=1366x768&cvar=%7B%221%22%3A%5B%22companyId%22%2C%22561682c2e4b075f709c17d0f%22%5D%2C%222%22%3A%5B%22category%22%2C%22Zmags%20experience%20interaction%22%5D%7D&bots=1",
    "/p.php?action_name=STL%20Homepage%20ENGLISH%20Desktop&idsite=3&rec=1&r=496435&h=7&m=10&s=27&url=http%3A%2F%2Fwww.linenchest.com%2Fen%2F&urlref=http%3A%2F%2Fwww.linenchest.com%2Fen%2F&_id=82790d4ad9949c9e&_idts=1481112627&_idvc=1&_idn=0&_refts=0&_viewts=1481112627&send_image=0&pdf=1&qt=0&realp=0&wma=0&dir=0&fla=0&java=1&gears=0&ag=0&cookie=1&res=1440x900&cvar=%7B%221%22%3A%5B%22%22%2C%22%22%5D%2C%222%22%3A%5B%22%22%2C%22%22%5D%7D&bots=1",
    "/p.php?action_name=Homepage%20Hero%20English%20Desktop&idsite=3&rec=1&r=495387&h=7&m=10&s=26&url=http%3A%2F%2Fwww.linenchest.com%2Fen%2F&urlref=http%3A%2F%2Fwww.linenchest.com%2Fen%2F&_id=82790d4ad9949c9e&_idts=1481112627&_idvc=1&_idn=0&_refts=0&_viewts=1481112627&send_image=0&pdf=1&qt=0&realp=0&wma=0&dir=0&fla=0&java=1&gears=0&ag=0&cookie=1&res=1440x900&cvar=%7B%221%22%3A%5B%22%22%2C%22%22%5D%2C%222%22%3A%5B%22%22%2C%22%22%5D%7D&bots=1",
    "/explore",
    "/search/tag/list",
    "/app/main/posts",
    "/posts/posts/explore",
    "/apps/cart.jsp?appID="
]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

flag = True
while (flag):
    increment = datetime.timedelta(seconds=random.randint(30, 300))
    otime += increment

    ip = faker.ipv4()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%z')
    vrb = numpy.random.choice(verb, p=[0.6, 0.1, 0.1, 0.2])

    uri = random.choice(resources)
    if uri.find("apps") > 0:
        uri += `random.randint(1000, 10000)`

    resp = numpy.random.choice(response, p=[0.9, 0.04, 0.02, 0.04])
    byt = int(random.gauss(5000, 50))
    referer = faker.uri()
    useragent = numpy.random.choice(ualist, p=[0.5, 0.3, 0.1, 0.05, 0.05])()
    f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip, dt, tz, vrb, uri, resp, byt, referer, useragent))

    log_lines = log_lines - 1
    flag = False if log_lines == 0 else True
