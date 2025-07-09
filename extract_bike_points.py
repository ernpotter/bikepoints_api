import json
import time
from datetime import datetime
import requests

response = requests.get('https://api.tfl.gov.uk/BikePoint')

#set up wait and try again mechanic
max_tries = 3
current_try = 0
wait_time = 60

while current_try<max_tries:
    try:
        #will error if the status code is not 200
        response.raise_for_status()

        data = response.json()

        #will error if no json is returned from the API call
        if len(data)<50:
            raise Exception('json returned too short')
        
        #setting up to test if data is within 2 days of today, otherwise the API might be stale
        now = datetime.now()
        modified_dates = []
        for item in data:
            for prop in item.get("additionalProperties", []):
                if "modified" in prop:
                    modified_dates.append(prop["modified"])
        max_modified_date = datetime.strptime(max(modified_dates),'%Y-%m-%dT%H:%M:%S.%fZ')
        delta = now-max_modified_date

        #will error if the API is stale
        if  delta.days > 2:
            raise Exception('Stale data, oh no')

        #outputting the file as a json in the data folder
        filename = now.strftime('%Y-%m-%d_%H-%M-%S')
        filepath = 'data/' + filename + '.json'
        with open(filepath, 'w') as file:
            json.dump(data, file)
        break

    except requests.exceptions.RequestException as e:
        print(e)
    except Exception as e:
        print(e)
    except:
        print('Oops')

    #while loop mechanism to make the script wait before trying again
    current_try += 1
    print('waiting')
    time.sleep(wait_time)

if current_try == max_tries:
    print('Too many tries')