import requests
import datetime

# Function to query the PRH API for companies registered within the last week
def query_companies_recent_registration():
    print("Querying for companies registered within the last week")

    # Define the base URL for the PRH API
    base_url = "https://avoindata.prh.fi/bis/v1"

    # Calculate the date one week ago from today
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    formatted_date = one_week_ago.strftime('%Y-%m-%d')

    # Define specific parameters
    params = {
        'totalResults': 'true',
        'maxResults': '1000',
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

        # Iterate through each company in the results
        for company in data['results']:
            print(f"\nCompany: {company['name']}")
            print(f"  Business ID: {company['businessId']}")
            print(f"  Registration Date: {company['registrationDate']}")

            # Display all available data for each company
            for key, value in company.items():
                if key not in ['name', 'businessId', 'registrationDate']:
                    print(f"  {key.capitalize()}: {value}")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

# Example usage
query_companies_recent_registration()
