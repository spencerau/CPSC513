import requests
from bs4 import BeautifulSoup


url = 'http://webservices.daehosting.com/services/isbnservice.wso'

soap_body = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <IsValidISBN10 xmlns="http://webservices.daehosting.com/ISBN">
            <sISBN>0-19-852663-6</sISBN>
        </IsValidISBN10>
    </soap:Body>
</soap:Envelope>'''

header = {
    'Content-Type': 'text/xml'
}

response_xml = requests.post(url, data=soap_body, headers=header)
soup = BeautifulSoup(response_xml.text, 'lxml-xml')

result = soup.find('IsValidISBN10Result')

if response_xml.status_code == 200:
    print(result.text)
else:
    print("Failed to send request with Error Code: ", response_xml.status_code)

