import requests
import datetime

# Define the base URL for the API
base_url = "https://avoindata.prh.fi/"

# Calculate the date range for the last month
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

# Format the dates in the required format (YYYY-MM-DD)
start_date_str = start_date.isoformat()
end_date_str = end_date.isoformat()

# Define the endpoint for company contact information
endpoint = f"bis/v1?totalResults=false&maxResults=1000&resultsFrom=0&registeredFrom={start_date_str}&registeredTo={end_date_str}"

# Construct the full URL
full_url = base_url + endpoint
print(f"Requesting URL: {full_url}")

# Make the API request
response = requests.get(full_url)

# Check if the request was successful
if response.status_code == 200:
    companies = response.json().get('results', [])
    for company in companies:
        company_name = company.get('name')
        company_email = company.get('email')
        print(f"Company Name: {company_name}, Email: {company_email}")
else:
    print(f"Failed to retrieve data from the API. Status Code: {response.status_code}, Response: {response.text}")
