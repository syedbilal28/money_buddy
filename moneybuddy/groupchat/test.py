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
print(response.json())
# Create a product
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer A21AAJSyqSzvhuW6g52RUoWmE4AZZrep2oUl2cFut_or5vBuyxq_IgHYhkzObP_1fMvHh4OzQRKs7qGjTuMoj5gNvrm5q4y5A',
#     'PayPal-Request-Id': 'CJLAT8A9QJ4YQ',
# }
# data='{"name": "Video Streaming Service","description": "Video streaming service","type": "SERVICE","category": "SOFTWARE","image_url": "https://example.com/streaming.jpg","home_url": "https://example.com/home"}'
# response = requests.get('https://api-m.sandbox.paypal.com/v1/catalogs/products?page_size=2&page=1&total_required=true', headers=headers)
# print(response.text)

# curl -v -X GET https://api-m.sandbox.paypal.com/v1/catalogs/products?page_size=2&page=1&total_required=true \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer Access-Token"
