import requests

# Define the season and round
season = 2024
round_number = 24

# Construct the API URL
url = f"http://ergast.com/api/f1/{season}/{round_number}/driverStandings.json"

# Send the GET request to the Ergast API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Extract the driver standings
    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    # Print the standings
    for driver in standings:
        print(f"Position: {driver['position']}, Driver: {driver['Driver']['familyName']}, Points: {driver['points']}")
else:
    print(f"Failed to retrieve data: {response.status_code}")
