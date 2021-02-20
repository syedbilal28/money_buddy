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
access_token=data['access_token']
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
    'Authorization': f'Bearer A21AAJL9RpRn3cHgx8-hBWeRhizW93lEZVkiWDEhyKzXjSqxoAXHhE7H2y1SNJ59HNlKZCloo19J5djznVUeBkwkm_BGfaPYQ',
    'PayPal-Request-Id': 'ea12344OHAFsaasfIHG12407asdflAaofaifh2390147asfhASADA',
}
data='{"name": "New Product","type":"SERVICE"}'
# response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products',headers=headers,data=data)
# print(response.json())
# print("response of product req",response.status_code)
# print(response.text)
product_id="PROD-4MS302206K188063B"
thread_price=10
url="https://api-m.sandbox.paypal.com/v1/billing/plans"
headers={
            "Accept":"application/json",
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            "Prefer":"return=representation"
        }
data={"product_id":f"{product_id}","name": "Basic Plan","description": "Basic plan","type":"FIXED","status":"CREATED","billing_cycles": [{"frequency": {"interval_unit": "MONTH","interval_count": 1},"tenure_type": "TRIAL","sequence": 1,"total_cycles": 12},{"frequency": {"interval_unit": "MONTH","interval_count": 1},"tenure_type": "REGULAR","sequence": 2,"total_cycles": 12,"pricing_scheme": {"fixed_price": {"value": f"{thread_price}","currency_code": "USD"}}}],"payment_preferences": {"auto_bill_outstanding": "true","setup_fee_failure_action": "CONTINUE","payment_failure_threshold": 3},"taxes": {"percentage": "1","inclusive": "false"}}
import json
data=json.dumps(data)
response = requests.post(url,headers=headers,data=data)
response=response.json()
print(response)
# curl -v -X GET https://api-m.sandbox.paypal.com/v1/catalogs/products?page_size=2&page=1&total_required=true \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer Access-Token"
