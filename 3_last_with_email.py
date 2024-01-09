import requests
import datetime
import json

# Function to query the PRH API for companies registered within the last 3 months
def query_companies_recent_registration():
    print("Querying for companies registered within the last 3 months")

    # Define the base URL for the PRH API
    base_url = "https://avoindata.prh.fi/bis/v1"

    # Calculate the date 3 months ago from today
    three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)
    formatted_date = three_months_ago.strftime('%Y-%m-%d')

    # Define specific parameters
    params = {
        'totalResults': 'true',
        'maxResults': '100',  # Retrieve 100 companies at a time
        'resultsFrom': '0',
        'companyRegistrationFrom': formatted_date
    }

    # Prepare a list to store the data of all companies
    all_companies_data = []

    # Keep making requests until we find 3 companies with contact details
    while len(all_companies_data) < 3:
        # Make the API request
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            total_results = data['totalResults']
            print(f"Total recently registered companies: {total_results}")

            # Iterate through each company in the results
            for company in data['results']:
                # Make an additional request for each company using its business ID
                company_response = requests.get(f"{base_url}/{company['businessId']}")
                if company_response.status_code == 200:
                    company_data = company_response.json()
                    # Check if the company has 'contactDetails' key and it's not empty
                    if 'contactDetails' in company_data and company_data['contactDetails']:
                        # Add the company data to the list
                        all_companies_data.append(company_data)
                        # If we have found 3 companies with contact details, stop searching
                        if len(all_companies_data) == 3:
                            break
                else:
                    print(f"Failed to retrieve data for company {company['businessId']}. Status Code: {company_response.status_code}, Response: {company_response.text}")

            # If we have found 3 companies with contact details, stop making requests
            if len(all_companies_data) == 3:
                break

            # If we haven't found 3 companies yet, move on to the next 100 companies
            params['resultsFrom'] += 100
        else:
            print(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

    # Write the data of all companies to a JSON file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(all_companies_data, f, indent=2, ensure_ascii=False)

# Example usage
query_companies_recent_registration()