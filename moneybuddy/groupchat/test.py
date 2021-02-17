import requests
#Get Token
headers={
    "Accept":"application/json",
    "Accept-Language":"en_US",
}
data={
    "grant_type":"client_credentials"

}
response =requests.post("https://api.sandbox.paypal.com/v1/oauth2/token",headers=headers,data=data,auth=('AWWN4IGDAUwzQQJvVtIqAMdEFr-Og8tsrgj4tt6-hnDcCRnWiX0kj8Jn5yWLsK5F9BoNWuLvcQtvBP6R','EOHznKaggJuJEUCQNN4AVtYqB3bLTQTE3ISrzHyo9Bn-e0PJ3Do5fKPv9-OvMmtOzTkwCNHRARpLEkho'))
data=response.json()
print(data['access_token'])
# import paypalrestsdk
# res= paypalrestsdk.configure({
#     'mode':'sandbox',
#     'client_id':'AWWN4IGDAUwzQQJvVtIqAMdEFr-Og8tsrgj4tt6-hnDcCRnWiX0kj8Jn5yWLsK5F9BoNWuLvcQtvBP6R',
#     'client_secret':'EOHznKaggJuJEUCQNN4AVtYqB3bLTQTE3ISrzHyo9Bn-e0PJ3Do5fKPv9-OvMmtOzTkwCNHRARpLEkho'
# })
# print(res)
# Create a product
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {data["access_token"]}',
    'PayPal-Request-Id': 'ea12344OHAFOSIHG12407asdflAaofaifh2390147asfhASADA',
}
data='{"name": "Video Streaming Service","description": "Video streaming service","type": "SERVICE", "category":"ELECTRONIC_CASH"}'
response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products',headers=headers,data=data)
print(response.json())
# print(response.text)

# curl -v -X GET https://api-m.sandbox.paypal.com/v1/catalogs/products?page_size=2&page=1&total_required=true \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer Access-Token"
