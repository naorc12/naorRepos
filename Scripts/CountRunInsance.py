import boto3
from datetime import datetime
import multiprocessing

result_list = []
Max_instance = int(40)

# Here we can add easily more filter state
FilterState = ['running']

# list of region - **will change to config file for the good order***
listRegions = ['eu-west-2', 'ap-northeast-1', 'ap-southeast-2', 'ap-south-1', 'ca-central-1', 'eu-central-1',
               'us-west-2', 'us-east-2', 'us-east-1', 'ap-northeast-2', 'us-west-1', 'eu-west-1', 'sa-east-1',
               'ap-southeast-1']

CurrentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# function that get all the instaces by the FiletrState and return temp list
def BuildRunIns(region, result_list):
    count = 0
    tmp_list = []
    session = boto3.Session(profile_name='account2', region_name=region)
    ec2 = session.resource('ec2', region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': FilterState}])
    for instance in instances:
        count += 1
        a = str(instance).split('ec2.Instance(id=')[1]
        a = a.split(')')[0]
        tmp_list.append(a)
    return tmp_list


# Func that get a list of the running instances and count them.
def CountRunInst(result_list):
    SumRunInstances = 0
    for i in result_list:
        SumRunInstances += len(i)
    return SumRunInstances


def Check_Inst(SumRunInstances, instances_file, result_list):
    if SumRunInstances > Max_instance:
        print "More Instances Running than should..."
        with open(instances_file, 'r') as RunIns:
            for line in RunIns:
                for i in result_list:
                    for j in i:
                        if j in line:
                            i.remove(j)
    else:
        print "All good, number of instances is OK."
    return result_list


# Func that get a list of lists, and build one clean list so it will be more convenience.
def Build_Final_list(result_list):
    Final_Run_List = []
    for list_instances in result_list:
        if len(list_instances) > 0:
            for instance in list_instances:
                Final_Run_List.append(instance)
    return Final_Run_List


def LogFile(logfile,SumRunInstances):
    with open(logfile, 'a+') as logfile:
        logfile.write("%s\tThe number of running instances for this time is: %s \n" % (CurrentTime, SumRunInstances))


# send Zabbix the running instances that don't recognized in the file
def SendZabbix(Final_Run_List):
    if len(Final_Run_List) > 0:
        print "There Are some Insances that running and they don't reconize:\n%s\n" \
              "please check it manual and if it's OK add them to the file...\n" % str(Final_Run_List)
    else:
        print "No Unrecognized Instances Running"


if __name__ == '__main__':
    # multiProcessing Function that go all the region async and build a list of running instances.
    pool = multiprocessing.Pool()
    for region in listRegions:
        a = pool.apply_async(BuildRunIns, args=(region, result_list), callback=result_list.append)
    pool.close()
    pool.join()

SumRunInstances = CountRunInst(result_list)
print SumRunInstances
LogFile('//Users//naorcohen//Desktop//CountInstance.log',SumRunInstances)
result_list = Check_Inst(SumRunInstances, '//Users//naorcohen//Desktop//InstanceMGMT.txt', result_list)
Final_Run_List = Build_Final_list(result_list)
SendZabbix(Final_Run_List)


