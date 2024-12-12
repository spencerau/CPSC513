import requests


url = "https://api.weather.gov/gridpoints/SGX/39,65/forecast"

respones = requests.get(url)

if respones.status_code == 200:
    #print(respones.json())
    data = respones.json()
    for record in data['properties']['periods']:
        print(record['name'] + ":", record['detailedForecast'])
        print()
else:
    print("Failed to send request with Error Code: ", respones.status_code)