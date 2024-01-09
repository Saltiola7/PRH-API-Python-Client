import requests
import datetime
import json

# Function to query the PRH API for companies registered within the last 3 days
def query_companies_recent_registration():
    print("Querying for companies registered within the last 3 days")

    # Define the base URL for the PRH API
    base_url = "https://avoindata.prh.fi/bis/v1"

    # Calculate the date 3 days ago from today
    three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
    formatted_date = three_days_ago.strftime('%Y-%m-%d')

    # Define specific parameters
    params = {
        'totalResults': 'true',
        'maxResults': '3',  # Change this to 3 to only retrieve the first 3 companies
        'resultsFrom': '0',
        'companyRegistrationFrom': formatted_date
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        total_results = data['totalResults']
        print(f"Total recently registered companies: {total_results}")

        # Prepare a list to store the data of all companies
        all_companies_data = []

        # Iterate through each company in the results
        for company in data['results']:
            # Make an additional request for each company using its business ID
            company_response = requests.get(f"{base_url}/{company['businessId']}")
            if company_response.status_code == 200:
                company_data = company_response.json()
                # Add the company data to the list
                all_companies_data.append(company_data)
            else:
                print(f"Failed to retrieve data for company {company['businessId']}. Status Code: {company_response.status_code}, Response: {company_response.text}")

        # Write the data of all companies to a JSON file
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(all_companies_data, f, indent=2, ensure_ascii=False)
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

# Example usage
query_companies_recent_registration()