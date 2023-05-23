import requests

# Set Infoblox appliance IP and credentials
infoblox_url = 'InfoBlox Server IP'
username = input("Enter your Infoblox username: ")
password = input("Enter your Infoblox password: ")

while True:
    # Set the alias and target hostname for the CNAME record
    alias = input("Enter the alias you are creating the CNAME record for: ")
    target = input("Enter the target CNAME alias you would like to implement: ")

    # Search for existing CNAME record
    response = requests.get(infoblox_url + 'record:cname?name=' + alias, auth=(username, password), verify=False)

    if response.status_code == 200:
        existing_records = response.json()
        if len(existing_records) > 0:
            existing_record = existing_records[0]
            existing_alias = existing_record.get('name')
            existing_target = existing_record.get('canonical')
            print(f'A CNAME record with the name {existing_alias} already exists with target {existing_target} \U0001F606. ')
            user_response = input("Do you want to replace the existing CNAME record? (y/n)")
            if user_response.lower() == "y":
                # Build the data for the PUT request
                data = {
                    'name': alias,
                    'canonical': target,
                    'view': 'default',
                }
                # Send the PUT request to update the CNAME record
                response = requests.put(infoblox_url + 'record:cname/' + existing_record['_ref'], auth=(username, password), json=data, verify=False)
                if response.status_code == 200:
                    print('CNAME record updated successfully!')
                else:
                    print(f'Error updating CNAME record, status code {response.status_code}, error: {response.content}')
            else:
                print("Skipping CNAME record update process.")
        else:
            # Build the data for the POST request
            data = {
                'name': alias,
                'canonical': target,
                'view': 'default',
            }

            # Send the POST request to create the CNAME record
            response = requests.post(infoblox_url + 'record:cname', auth=(username, password), json=data, verify=False)

            # Check the response status code to see if the request was successful
            if response.status_code == 201:
                print('CNAME record created successfully!')
    else:
        print('Sorry! There was an error creating or updating the CNAME record.', response.content)
    
    user_response = input("Do you want to make another CNAME record? (y/n)")
    if user_response.lower() == "n":
        print("Thank you for using the The Infoblox CNAME Creator!")
        break
