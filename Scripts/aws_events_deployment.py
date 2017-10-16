#! /usr/bin/python

from datetime import datetime
import os
listRegions=['eu-west-2','ap-northeast-1','ap-southeast-2','ap-south-1','ca-central-1','eu-central-1','us-west-2','us-east-2','us-east-1','ap-northeast-2','us-west-1','eu-west-1','sa-east-1','ap-southeast-1']
CurrentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
list_event = []
list_filter_events = []

FilterKeys=['[Completed]','[Canceled]']

#Func that build the Index and return an array that include all the events, every event in own cell
def buildIndex(file,expt,limit):
    with open (file, 'r') as AW:
        list_event = []
        for line in AW:
            if expt in line:
                event_instance=line
                line = AW.next()
                while limit not in line:
                    event_instance+=line
                    line = AW.next()
                event_instance+=line
                list_event.append(event_instance)
        return list_event

#Func that remove the cell that contain the FilterKey
def FilterParameter(list_event,FilterKey):
    list_filter_events = []
    for i in list_event:
            if FilterKey not in i:
                list_filter_events.append(i)
    return list_filter_events

for i in listRegions:
       # Here is AWS command to get all the events
        os.system("(aws ec2 describe-instance-status --region %s --filter 'Name=event.code,Values=instance-reboot,system-reboot,system-maintenance,instance-retirement,instance-stop' "
         "| grep 'AvailabilityZone\|InstanceId\|Description\|NotAfter\|NotBefore'| tr -d ',' >> /tmp/aws_maintenance_production_deployment.log)"%i)

with open('//opt//zabbix//externalscripts//externalscriptsLogs//aws_maintenance//aws_main_deployment.log','a+') as pmlog:
        pmlog.write(CurrentTime+'\n')
        # copy the events to the log
        with open('//tmp//aws_maintenance_production_deployment.log','r') as tmpmlog:
            pmlog.write(tmpmlog.read())

list_event = buildIndex('//tmp//aws_maintenance_production_deployment.log','"AvailabilityZone":','"NotBefore":')
for FilterKey in FilterKeys:
    list_filter_events = FilterParameter(list_event,FilterKey)

#build a file with the relevance event for send to Zabbix.
with open('//tmp//aws_filtered_events_deployment.log','w') as afelog:
    for event in list_filter_events:
        afelog.write(event)

#send to zabbix the relevant events 
command = ("""zabbix_sender  -k aws_maintenance_production_deployment -o  "$(cat /tmp/aws_filtered_events_deployment.log | tr -s [:space:] ' '|sed 's/" "/"\\n"/g')" -z 54.83.19.153 -s AWS_Events -vv""")
os.system("%s"%command)

# delete the temp file 
os.remove('//tmp//aws_maintenance_production_deployment.log')
os.remove('//tmp//aws_filtered_events_deployment.log')