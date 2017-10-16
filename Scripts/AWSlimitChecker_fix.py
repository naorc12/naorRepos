#!/usr/bin/env python

#import packages#
from awslimitchecker.checker import AwsLimitChecker
import os,time
import operations_utilities
import logging
import pprint
import argparse
import json


start = time.time()

auto_complete = '_limit.conf'
problems_regions_dict = {"ca-central-1": "canada", "us-east-2": "ohio"}
default_file_name = 'default'+auto_complete

with open ('//opt//zabbix//externalscripts//AWSlimitchecker//%s' % default_file_name) as default_limit:
    default_limit_dict = json.load(default_limit)
                                                       

#get parameters from user#
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-r", "--region", dest="myRegionVariable",help="region?", metavar="REGION")
parser.add_argument("-z", "--zabbix_host", dest="myZabbixHost",help="host?", metavar="ZABBIXHOST")
args = parser.parse_args()

#logs#
logging.basicConfig()
logger = logging.getLogger()
logger = logging.getLogger('AWSlimitchecker')
hdlr = logging.FileHandler('/opt/zabbix/externalscripts/externalscriptsLogs/AWSlimitchecker/AWSlimitchecker.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

#parameter for the initiator script#
# You can find the Project AwsLimitChecker in this link: https://github.com/jantman/awslimitchecker


region = args.myRegionVariable
print region
region = 'ca-central-1'
checker = AwsLimitChecker(region=region)
if region in problems_regions_dict.keys():
    limit_path = str(problems_regions_dict[region]) + str(auto_complete)
    with open ('//opt//zabbix//externalscripts//AWSlimitchecker//%s' % limit_path) as limit_conf:
        problems_regions_dict[region] = json.load(limit_conf)
try:
    checker.find_usage()
except:
    pass
#print args.myRegionVariable
#print args.myZabbixHost
for aws_module, svc_limits in sorted(checker.get_limits().items()):
    for limit_name, limit in sorted(svc_limits.items()):
        if 'Firehose' not in aws_module:
            try:
                print("{aws_module} '{limit_name}': usage={current_usage} (limit={limit_value})".format(
                    aws_module=aws_module,
                    limit_name=limit_name,
                    current_usage=limit.get_current_usage_str(),
                    limit_value=limit.get_limit()
                ))
                limit_name = limit_name.replace(" ", "_")
                limit_name=limit_name.replace('(', '')
                limit_name=limit_name.replace(')', '')
                limit_name = limit_name
                current_usage = limit.get_current_usage_str()
                if current_usage != '<unknown>':
                    current_usage = int(current_usage)
                    logger.info('zabbix send usage '+ args.myZabbixHost +' ' + limit_name + ' usage = ' + str(current_usage))
                    operations_utilities.send_zabbix_values(limit_name,current_usage,'54.83.19.153',args.myZabbixHost)

                limit_value = limit.get_limit()
                limit_value = str(limit_value)
                logger.info('zabbix send limit value '+ args.myZabbixHost + ' '  + limit_name + ' limit = '  + str(limit_value))
                limit_value = int(limit_value)
                #replace problematic chars ( or ), cannot be sent to zabbix
                limit_name=limit_name.replace('(', '')
                limit_name=limit_name.replace(')', '')
                limit_name = limit_name.replace(" ", "_")
                if region in problems_regions_dict.keys():
                    print region
                    if limit_name in problems_regions_dict[region].keys() and limit_value == default_limit_dict[limit_name]:
                        print limit_name, limit_value
                        limit_value = problems_regions_dict[region][limit_name]
                        print "Your new Value is: " + str(limit_value)
                operations_utilities.send_zabbix_values(limit_name+"_limit",limit_value,'54.83.19.153',args.myZabbixHost)
            except:
                pass
        else:
            continue

logger.info('aws limit checker Finito')
end = time.time()
print(end - start)
