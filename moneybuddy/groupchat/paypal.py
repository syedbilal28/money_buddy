import requests
def GenerateToken():
    url="https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers={"Accept":"application/json","Accept-Language":"en_US"}
    data={"grant_type":"client_credentials"}
    response=requests.post(url,headers=headers,data=data,auth=("AWWN4IGDAUwzQQJvVtIqAMdEFr-Og8tsrgj4tt6-hnDcCRnWiX0kj8Jn5yWLsK5F9BoNWuLvcQtvBP6R","EOHznKaggJuJEUCQNN4AVtYqB3bLTQTE3ISrzHyo9Bn-e0PJ3Do5fKPv9-OvMmtOzTkwCNHRARpLEkho"))
    data=response.json()
    access_token=data['access_token']
    return access_token