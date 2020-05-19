'''
Script for creating a new Management zone in Dynatrace
The script first checks if there is already an Management zone with the same name
and based on the result it updates it or creates on new one
'''

import requests
import json
import sys

CONFIGFILE=sys.argv[1]

# Enter your own environment id and API key token here
YOUR_ENV_ID = ''
YOUR_API_TOKEN = ''

headers = {'Content-Type' : 'application/json', 'Authorization' : 'Api-Token ' + YOUR_API_TOKEN }
url1 = 'https://' + YOUR_ENV_ID + '.live.dynatrace.com/api/config/v1/managementZones/validator'
url2 = 'https://' + YOUR_ENV_ID + '.live.dynatrace.com/api/config/v1/managementZones'

f = open(CONFIGFILE)
payload = json.load(f)


def checkExistingMgmtZones(url, mzone, headers):
  r = requests.get(url,  headers=headers)
  response_json = r.content.decode('utf8').replace("'", '"')
  temp_json = json.loads(response_json)
  existing_mzones = []
  for value in (temp_json.get('values')):
    existing_mzones.append(value.get('name'))
  if mzone in existing_mzones:
    return True
  else:
    return False


def getExistingMgmtZonesId(url, mzone, headers):
  r = requests.get(url, headers=headers)
  response_json = r.content.decode('utf8').replace("'", '"')
  temp_json = json.loads(response_json)
  existing_mzones_id = []
  for value in (temp_json.get('values')):
    if (value.get('name')) == mzone:
      existing_mzones_id.append(value.get('id'))
  return existing_mzones_id

# get the desired name of the Management Zone from json to check if it already exist
new_mzone_name = payload.get('name')
result = checkExistingMgmtZones(url2, new_mzone_name, headers)

# if the Management Zone already exist get the ID needed to update it
if result:
  mzone_id = getExistingMgmtZonesId(url2, new_mzone_name, headers)
  print("Modifying existing Management Zone {} ...".format(new_mzone_name))
  url = url2 + "/" + mzone_id[0]
  mod_response = requests.put(url, json=payload, headers=headers)
  if mod_response.status_code == 204:
    print("Management Zone {} modified successfully ".format(new_mzone_name))



# based on the result proceed in creating a new Mgmnt zone
if not result:
  print ("Creating new Management Zone called: ", new_mzone_name)
  r = requests.post(url1, json=payload, headers=headers)

  if r.status_code == 204: # validation succeded
      r = requests.post(url2, json=payload, headers=headers)
      if (r.status_code) == 201:
        print("Management Zone {} created successfully ".format(new_mzone_name))

