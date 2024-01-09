import requests
import datetime

# Function to query the PRH API for companies in a given city within the last month
def query_companies(city_name):
    print(f"Querying for companies in {city_name} within the last month")

    # Define the base URL for the PRH API
    base_url = "https://avoindata.prh.fi/bis/v1"

    # Calculate the date one month ago from today
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    formatted_date = one_month_ago.strftime('%Y-%m-%d')

    # Define specific parameters
    params = {
        'totalResults': 'true',
        'maxResults': '1000',
        'resultsFrom': '0',
        'registeredOffice': city_name,
        'companyForm': 'OY',
        'companyRegistrationFrom': formatted_date
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        total_results = data['totalResults']
        print(f"Total companies in {city_name}: {total_results}")

        # Iterate through each company in the results
        for company in data['results']:
            print(f"Company: {company['name']}")

            # Check for contact details and print if available
            if 'contactDetails' in company:
                for contact in company['contactDetails']:
                    if contact.get('source') == 0:  # Check if source is 'joint'
                        print(f"  Contact Detail: {contact.get('value', 'No value available')}, Type: {contact.get('type', 'No type available')}")
            else:
                print("  No contact details available")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

# Example usage
query_companies('Helsinki')
