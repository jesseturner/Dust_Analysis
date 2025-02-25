import sys 
import json
import datetime
import certifi
import urllib3

# Create a PoolManager instance to make requests.
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

# Set the URL for the GES DISC API endpoint for dataset searches
url = 'https://disc.gsfc.nasa.gov/service/datasets/jsonwsp'

# Prompt for search string keywords
# This will keep looping and prompting until search returns an error-free response
done = False
while done is False :
  myString=''
  while len(myString) < 1 : 
    myString = input("Enter search keywords: ")

  # Set up the JSON WSP request for API method: search
  search_request = {
    'methodname': 'search',
    'type': 'jsonwsp/request',
    'version': '1.0',
    'args': {'search': myString}
  }

  # Submit the search request to the GES DISC server
  hdrs = {'Content-Type': 'application/json',
          'Accept': 'application/json'}
  data = json.dumps(search_request)
  r = http.request('POST', url, body=data, headers=hdrs)
  response = json.loads(r.data)

  # Check for errors
  if response['type']=='jsonwsp/fault' :
    print('ERROR! Faulty request. Please try again.')
  else : 
    done = True
print('OK')

# Indicate the number of items in the search results
total = response['result']['totalResults']
if total == 0 :
    print('Zero items found')
elif total == 1 : 
    print('1 item found')
else :          
    print('%d items found' % total)

# Report on the results: DatasetID and Label
if total > 0 :
    for item in response['result']['items']:
        print('%-20s  %s' % (item['dataset']['id'], item['dataset']['label']))

# Report on the results: DatasetID and Landing Page URL
if total > 0 :
    for item in response['result']['items']:
        print('%-20s  %s' % (item['dataset']['id'], item['link']))

# Report on the results: DatasetID and variable subsetting information
varSubset = False
for item in response['result']['items']:
    # Check for subset services
    if item['services']['subset']: 
        for ss in item['services']['subset']:
            # make sure variable subsetting is supported
            if 'variables' in ss['capabilities'] and 'dataFields' in ss :
                print('The %s service supports variable subsetting for %s' % 
                      (ss['agentConfig']['agentId'],item['dataset']['id']))
                print('Variable names are:')
                varSubset = True
                # Print a list of variable names and descriptions
                for var in ss['dataFields']:
                    print(var['value'])
                print()
if varSubset is False: 
    print('Variable subsetting is not available for %s' % item['dataset']['id'])

# Write out the complete results to a file
fname='my_search_results.txt'
f = open(fname,'w')
f.write(json.dumps(response, indent=2, sort_keys=True))
f.close()
print('Complete metadata for each search result item has been written out to '+fname)