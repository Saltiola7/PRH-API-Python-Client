import requests
import datetime

# Define the base URL for the PRH API
base_url = "https://avoindata.prh.fi/"

# Calculate the date range for the last month
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

# Format the dates in the required format (YYYY-MM-DD)
start_date_str = start_date.isoformat()
end_date_str = end_date.isoformat()

# Define the endpoint for company contact information
# Adjust this endpoint based on the specific data you're fetching
endpoint = f"tr/v1/publicnotices?totalResults=true&maxResults=1000&resultsFrom=0&noticeRegistrationFrom={start_date_str}&noticeRegistrationTo={end_date_str}"

# Make the API request
response = requests.get(base_url + endpoint)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(data)  # This is just for demonstration, adjust it based on your needs
else:
    print(f"Failed to retrieve data from the API. Status Code: {response.status_code}, Response: {response.text}")
