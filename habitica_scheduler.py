#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
from datetime import date
from datetime import datetime
import requests
import json
from habitica_keys import get_user_keys

print("Program ran at " + str(datetime.now()))

url = 'https://habitica.com/api/v3/tasks/user'

keys = get_user_keys() #In habitica_keys, returns a dictionary.
headers = {"x-api-user":keys["user"],"x-api-key":keys["api-key"], 'content-type': 'application/json'}

habitica_file = open("/Users/2017-A/Desktop/added_to_habitica.txt", "r")
already_added = []
for line in habitica_file:
    already_added.append(list(line.rstrip()))
habitica_file.close()
habitica_file = open("/Users/2017-A/Desktop/added_to_habitica.txt", "a")

upcoming = open("/Users/2017-A/Desktop/upcoming.txt")

for original_line in upcoming:
    line = list(original_line.rstrip())
    if line != []:
        day = int(line[0])*10+int(line[1])
        month = int(line[3])*10+int(line[4])
        year = int(line[6])*1000+int(line[7])*100+int(line[8])*10+int(line[9])
        the_day = date(year, month, day)
        the_day_as_string = str(day)+"/"+str(month)
        difference = (the_day - date.today()).days
        if difference < 7:
            if line not in already_added:
                item = "".join(line[11:])
                payload = {'text': item, 'type': "todo", 'date': the_day_as_string, 'priority': 2}
                response = requests.post(url, data=json.dumps(payload), headers=headers)
                if json.loads(response.content)["success"]:
                    habitica_file.write(original_line)
                    print(original_line + " added\n")
                else:
                    print("Error connecting to server")
