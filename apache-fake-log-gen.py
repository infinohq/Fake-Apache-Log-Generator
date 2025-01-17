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

def parse_size_limit(size_limit):
    unit_dict = {'k': 1024, 'm': 1024**2, 'g': 1024**3}
    size_unit = size_limit[-1].lower()
    if size_unit.isdigit():
        size_value = int(size_limit)
    else:
        size_value = int(size_limit[:-1]) * unit_dict.get(size_unit, 1)
    return size_value


parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--log-format", "-l", dest='log_format', help="Log format, Common or Extended Log Format ", choices=['CLF','ELF'], default="ELF" )
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int, default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)
parser.add_argument("--sleep", "-s", help="Sleep this long between lines (in seconds)", default=0.0, type=float)
parser.add_argument("--month", "-m", help="Month to use", default=1, type=int)
parser.add_argument("--size", help="Size limit of the generated file (e.g., 100k, 10m, 1g)", default="1m", type=str)


args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
log_format = args.log_format
month = args.month

size_limit = parse_size_limit(args.size)

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime(2023, args.month, 1)

outFileName = 'access_log_'+timestr+'.log' if not file_prefix else file_prefix+'_access_log_'+timestr+'.log'

response=["200","404","500","301"]

verb=["GET","POST","DELETE","PUT"]

resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

flag = True
total_bytes = 0
while (flag):
    increment = datetime.timedelta(seconds=0.01)
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
        log_line = '%s - - [%s %s] "%s %s HTTP/1.0" %s %s' % (ip,dt,tz,vrb,uri,resp,byt)
    elif log_format == "ELF":
        log_line = '%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"' % (ip,dt,tz,vrb,uri,resp,byt,referer,useragent)

    print(log_line)

    total_bytes += len(log_line)
    log_lines = log_lines - 1
    flag = False if total_bytes > size_limit and log_lines <= 0 else True

    if args.sleep:
        time.sleep(args.sleep)
