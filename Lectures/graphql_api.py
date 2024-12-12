import requests


url = "https://countries.trevorblades.com/"

query = """
{
    country(code: "US")
    {
        name
        capital
        currency
        languages
        {
            name
        }
    }
}
"""

response = requests.post(url, json={'query': query})
#print(response.json())
record = response.json()['data']['country']
print(record['name'])
print("Capital:", record['capital'])
print("Currency:", record['currency'])
print("Languages:")
for language in record["languages"]:
    print(language['name'])