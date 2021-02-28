import requests
import json
def GenerateToken():
    url="https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers={"Accept":"application/json","Accept-Language":"en_US"}
    data={"grant_type":"client_credentials"}
    response=requests.post(url,headers=headers,data=data,auth=("AWWN4IGDAUwzQQJvVtIqAMdEFr-Og8tsrgj4tt6-hnDcCRnWiX0kj8Jn5yWLsK5F9BoNWuLvcQtvBP6R","EOHznKaggJuJEUCQNN4AVtYqB3bLTQTE3ISrzHyo9Bn-e0PJ3Do5fKPv9-OvMmtOzTkwCNHRARpLEkho"))
    data=response.json()
    access_token=data['access_token']
    return access_token
def CreateProduct(access_token,hashed_request_id,user,thread_price):
    headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'PayPal-Request-Id': hashed_request_id,
            }
            
    data={"name": f"{user.username + str(thread_price)}","type": "SERVICE"}
    data=json.dumps(data)
    
    response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products',headers=headers,data=data)
    if response.status_code != 200 or response.status_code !=201:
        access_token=GenerateToken()
        response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products',headers=headers,data=data)
        

    data=response.json()
    return data['id']
def CreatePlan(access_token,product_id,thread_price):
    url="https://api-m.sandbox.paypal.com/v1/billing/plans"
    headers={
                "Accept":"application/json",
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                "Prefer":"return=representation"
            }
    data={"product_id":f"{product_id}","name": "Basic Plan","description": "Basic plan","type":"FIXED","status":"ACTIVE","billing_cycles": [{"frequency": {"interval_unit": "MONTH","interval_count": 1},"tenure_type": "REGULAR","sequence": 1,"total_cycles": 12,"pricing_scheme": {"fixed_price": {"value": f"{thread_price}","currency_code": "USD"}}}],"payment_preferences": {"auto_bill_outstanding": "true","setup_fee_failure_action": "CONTINUE","payment_failure_threshold": 3},"taxes": {"percentage": "1","inclusive": "false"}}
    data=json.dumps(data)
    response = requests.post(url,headers=headers,data=data)
    print(response.json())
    if(response.status_code == 201):
      response=response.json()
      return response['id']
    else:
      return "Could not be created"
def PauseSubscription(subscription_id,access_token):
    url=f"https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/suspend"
    headers={
      "Content-Type":"application/json",
      "Authorization":f"Bearer {access_token}"
    }
    data={"reason":"Customer-requested pause"}
    data=json.dumps(data)
    response=requests.post(url,headers=headers,data=data)
    if response.status_code != 200 or response.status_code != 201:
      access_token=GenerateToken()
      headers={
      "Content-Type":"application/json",
      "Authorization":f"Bearer {access_token}"
    }
    response=requests.post(url,headers=headers,data=data)
def ResumeSubscription(subscription_id,access_token):
  url=f"https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/activate"
  headers={
      "Content-Type":"application/json",
      "Authorization":f"Bearer {access_token}"
    }
  data={"reason":"Reactivating on customer request"}
  data=json.dumps(data)
  response=requests.post(url,headers=headers,data=data)
  if response.status_code != 200 or response.status_code != 201:
    access_token=GenerateToken()
    headers={
    "Content-Type":"application/json",
    "Authorization":f"Bearer {access_token}"
  }
  response=requests.post(url,headers=headers,data=data)
def CreateSubscription():
    url="https://api-m.sandbox.paypal.com/v1/billing/subscriptions"
    headers={
        "Accept": "application/json" ,
   "Authorization": f"Bearer {access_token}" ,
   "Prefer": "return=representation" ,
   "Content-Type": "application/json" 
    }
    data={
        "plan_id": f"{plan_id}",
      "start_time": "2020-02-27T06:00:00Z",
      "subscriber": {
        "name": {
          "given_name": "John",
          "surname": "Doe"
        },
        "email_address": "customer@example.com"
      },
      "application_context": {
        "brand_name": "example",
        "locale": "en-US",
        "shipping_preference": "SET_PROVIDED_ADDRESS",
        "user_action": "SUBSCRIBE_NOW",
        "payment_method": {
          "payer_selected": "PAYPAL",
          "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
        },
        "return_url": "https://example.com/returnUrl",
        "cancel_url": "https://example.com/cancelUrl"
      }
    }

def SendPayout(email_receiver,amount,payout_id,access_token):
  url="https://api-m.sandbox.paypal.com/v1/payments/payouts"
  headers={
    "Content-Type":"application/json",
    "Authoization":f"Bearer {access_token}"
  }
  data={
    "sender_batch_header":{
      "sender_batch_id":f"{payout_id}",
      "email_subject": "You have a payout!",
      "email_message": "You have received a payout! Thanks for using our service!"
    },
    "items":[
      {
        "recipient_type": "EMAIL",
      "amount": {
        "value": f"{amount}",
        "currency": "USD"
      },
      "note": "Thanks for your patronage!",
      "sender_item_id": f"{payout_id}",
      "receiver": f"{email_receiver}"
      }
    ]
  }
  data=json.dumps(data)
  try:
    response=requests.post(url,headers=headers,data=data)
  except:
    access_token=GenerateToken()
    response=requests.post(url,headers=headers,data=data)
  response=response.json()
  return response