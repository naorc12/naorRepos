#! /usr/bin/python

import mandrill
import csv

template_name = raw_input("Insert a template name:\n")
csv_file = raw_input("Insert a CSV file with the known format:\n Insert -h or -help for help\n")
if str(csv_file) == '-help' or str(csv_file) == '-h':
    print "You need to create a template with the following format:\n" \
          "\tThe First column always should be the email you want to send to\n" \
          "\tThe other column depends on the template, if the template require a message (*|message|*) so the column should called 'message'.\n" \
          "\tThe rows under should be the value of the column, each rows describe different email.\n" \
          "More information can be found in " \
          "'https://confluence.aka.lgl.grungy.us/display/RAVELLO/Mandrill+Guide'"
    exit()

parameter_list = []
column = []
merge_vars =[]
# The api key, with him we send the email, can be found under setting in mandrill web.
mandrill_api_key = '3gF70BI6RKf5XklWt5kf5Q'
with open(csv_file, 'rb') as csvfile:
    #read the CSV file
    spamreader = csv.reader(csvfile, skipinitialspace=True)
    firstline = True
    for row in spamreader:
        # if this is the first line which mean this is the key for the template so we save it in side.
        if firstline == True:
            for i in range(len(row)):
                column.append(row[i])
            firstline =False
            continue
        # appand to menu list with all the parameter from CSV.
        parameter_list.append(row)


for list in parameter_list:
    client = mandrill.Mandrill(apikey=mandrill_api_key)
    for i in range(1, len(list)):
        print column[i], list[i]
        # build the global merge vars to send for the template,
        # build as first row is the names and the value is each one of the rows in CSV file.
        merge_vars.append({"name": column[i], "content": list[i]})

    message = {'from_email': 'naor.cohen@oracle.com',
               'to': [{'email': list[0],
                       'name': list[0],
                       'type': 'to'}
                      ],
               ## global_merge_vars - are the parameter to give the template
               # (example: shows in template as *|message|* we send "name": 'message', "content": 'value' )
                   "global_merge_vars": merge_vars
               }

    # This the command to send mail with mandrill.
    result = client.messages.send_template(template_name=template_name,
                                           template_content=[],
                                           message=message)
    print "email sent to: %s" % list[0]



