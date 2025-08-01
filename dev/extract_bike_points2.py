import json
import time
from datetime import datetime
import requests

url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

#setting up wait and try again mechanic
max_tries = 3
current_try = 0
wait_time = 3

while current_try < max_tries:
    try:
        # 1. Check if the request was successful (status code 200)
        response.raise_for_status()

        # 2. Check if there is data within the JSON
        data = response.json()
        if len(data) < 50:
            raise Exception('JSON returned too short')
        
        # 3. is data stale?
        now = datetime.now() #what is the time now
        modified_dates = [] #creates an empty list
        for item in data:   # looks through each item in data
            for prop in item.get("additionalProperties", []): # Try to get the list under 'additionalProperties'. If it doesn’t exist, just use an empty list so the loop won’t crash
                if "modified" in prop and isinstance(prop["modified"], str): # Checks if the word "modified" is a key in this dictionary (prop).
                    modified_dates.append(prop["modified"]) # If yes, it takes the value of the "modified" field (a date/time string) and adds it to the modified_dates list.
        max_date_str = max(modified_dates)
        max_modified_date = datetime.strptime(max_date_str, '%Y-%m-%dT%H:%M:%S.%fZ') # Finds the latest (maximum) date string from the list modified_dates
       #max_modified_date = datetime.strptime(max(modified_dates, '%Y-%m-%dT%H:%M:%S.%fZ')) # Finds the latest (maximum) date string from the list modified_dates
        delta = now - max_modified_date #calculates the difference between now and that latest modified date.

        # 3. contd. Will error if the API is stale
        if delta.days > 2:
            raise Exception('Stale data, oh no')
        
        #outputting the file as a json in the data folder
        filename = now.strftime('%Y-%m-%d_%H-%M-%S')
        filepath = 'data/' + filename + '.json'
        with open(filepath, 'w') as file: # This opens the file at that path for writing ('w')
            json.dump(data, file, indent=2) # This writes the data into the file in JSON format.
        
        break   # end the while loop

    # 1. if status != 200 then print the error. Handeling request related errors
    except requests.exceptions.RequestException as e:
        print(e)
    # handles all other exceptions, like JSON or your custom one
    except Exception as e:
        print(e)
    # catch all for all other error types
    except:
        print('Oops')
    
    #while loop mechanism to make the script wait before trying again
    current_try += 1 #add 1 to the current_try variable.
    print('waiting') 
    time.sleep(wait_time) # This pauses the program for wait_time in seconds

if current_try == max_tries:
    print('Too many tries')