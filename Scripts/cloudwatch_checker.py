import boto3,os
import operation_util

session = boto3.Session(profile_name='mgmt_naor')
for region in operation_util.list_server:
    client = session.client('cloudwatch',region_name=region)
    response = client.describe_alarms(
        StateValue='O'
    )
    print "found %s alaram for region %s:\n" % (len(response[u'MetricAlarms']), region)
    for alarm in response[u'MetricAlarms']:
        print alarm[u'AlarmName']
        print alarm['StateReason']
        print '----------------------------------------------------'
    print '\n'
# print response[u'MetricAlarms'][1]
# print response[u'MetricAlarms'][1][u'AlarmName']
# print response[u'MetricAlarms'][1]['StateReason']
# [u'AlarmName]
# ['StateReason']
print operation_util.list_server

with open('//opt//zabbix//externalscripts//externalscriptsLogs//aws_maintenance//aws_main_deployment.log',
          'a+') as pmlog:
    pmlog.write(CurrentTime + '\n')
    # copy the events to the log
    with open('//tmp//aws_maintenance_production_deployment.log', 'r') as tmpmlog:
        pmlog.write(tmpmlog.read())

from datetime import datetime
CurrentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
listRegions = operations_utilities.list_regions