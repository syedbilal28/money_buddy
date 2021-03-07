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
url="https://api-m.sandbox.paypal.com/v1/billing/subscriptions/I-LW269F49NGF1/transactions?start_time=2018-01-21T07:50:20.940Z&end_time=2022-08-21T07:50:20.940Z"
headers={
    "Content-Type":"application/json",
    "Authorization":f"Bearer {access_token}"
  }
  
response=requests.get(url,headers=headers)
  
response=response.json()
print(response)