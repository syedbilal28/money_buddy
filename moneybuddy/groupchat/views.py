from django.shortcuts import render,HttpResponse,redirect
from .forms import LoginForm,SignupForm,ProfileForm
from django.contrib.auth import login, logout,authenticate
from .models import Thread,ChatMessage,Profile,PaypalSubscription
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.dispatch import Signal
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import asyncio,json
import paypalrestsdk
from paypalrestsdk import BillingPlan
from hashlib import sha256
import requests
import random
from . import paypal
from .stripefuncs import CreateAccount,CreateCustomer,CreatePaymentMethod,CreatePlan
paypalrestsdk.configure({
    'mode':'sandbox',
    'client_id':'AWWN4IGDAUwzQQJvVtIqAMdEFr-Og8tsrgj4tt6-hnDcCRnWiX0kj8Jn5yWLsK5F9BoNWuLvcQtvBP6R',
    'client_secret':'EOHznKaggJuJEUCQNN4AVtYqB3bLTQTE3ISrzHyo9Bn-e0PJ3Do5fKPv9-OvMmtOzTkwCNHRARpLEkho'
})
stripe.api_key = "sk_test_51HpXfpJEfpDOgYo1UQu5PZvq3Rj1bVWGbW1WcyRvh2jBZpJVRyu4kJ8uVzAItLgk07ZCi90VeRHXqMANxYhode1800WXZCTuuR"
# Create your views here.
@csrf_exempt
def index(request):
    if request.method=="POST":
        print("POSTED")
        print(request.POST)
        form = LoginForm(data=request.POST)
        print(form)
        if form.is_valid():
            
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                message="Invalid Credentials"
                form=LoginForm()
                return render(request,"index.html",{"form":form,"message":message})
                
    else:

        form = LoginForm()
        
        return render(request,'index.html',{"form":form})
@login_required
def home(request):
    threads=Thread.objects.all()

    try:
        profile=Profile.objects.get(user=request.user)
    except:
        return redirect('index')
    request.session['access_token']=paypal.GenerateToken()
    access_token=request.session['access_token']
    # access_token=paypal.GenerateToken()

    context={"Threads":threads,"User":profile}
    return render(request,"threads.html",context)

def Signup(request):
    if request.method=="POST":
        signupform = SignupForm(request.POST)
        profileform=ProfileForm(request.POST,request.FILES)
        print(profileform)
        if signupform.is_valid() and profileform.is_valid():
            user=signupform.save()
            print(user)
            # try:
            profile=Profile.objects.create(
                user=user,
                country=profileform.cleaned_data['country'],
                profile_picture=profileform.cleaned_data['profile_picture']
                )
            profile.save()
            login(request,user)
            return redirect('home')
            # except:
            #     user.delete()
                
            #     signupform=SignupForm()
            #     profileform=ProfileForm()
            #     message="Error"
            #     return render(request,'signup.html',{"signupform":signupform,"profileform":profileform,"message":message})
             
    else:
        signupform = SignupForm()
        profileform=ProfileForm()
    return render(request,"signup.html", {"signupform":signupform,"profileform":profileform})

@csrf_exempt
def GetPlanId(request):
    thread_id=request.POST.get("thread_id")
    thread=Thread.objects.get(pk=int(thread_id))
    return JsonResponse({"plan_id":thread.plan_id},safe=False)
@csrf_exempt
def CreatePaypalSubscription(request):
    plan_id=request.POST.get("plan_id")
    subscription_id=request.POST.get("subscription_id")
    profile= Profile.objects.get(user=request.user)
    thread=Thread.objects.get(plan_id=plan_id)
    sub=PaypalSubscription.objects.create(user=profile,thread=thread,subscription_id=subscription_id)
    access_token=request.session.get("access_token")
    paypal.PauseSubscription(subscription_id,access_token)
    thread.participants.add(profile)
    thread.save()
    return JsonResponse({"active":True})
def inbox(request,thread_id):
    thread_=Thread.objects.get(pk=eval(thread_id))
    messages=ChatMessage.objects.filter(thread=thread_)
    try:
        profile=Profile.objects.get(user=request.user)
    except:
        return redirect('home')
    if profile==thread_.admin and thread_.status=='N' and len(thread.participants.all()) >3:
        start_check=True
    else:
        start_check=False

    context={"messages":messages,"thread":thread_,"User":profile,"Start":start_check}
    return render(request,'inbox.html',context)
def Logout(request):
    logout(request)
    return redirect ('index')
def About_us(request):
    return redirect('home')
# @csrf_exempt
def Create_Thread(request):
    created_by=request.user
    print(request.POST)
    payment_method= request.POST.get("payment_method")
    print(payment_method)
    thread_price=int(request.POST.get("price"))
    thread_privacy=request.POST.get("privacy")
    profile=Profile.objects.get(user=request.user)
    
    try:
        thread_password=request.POST.get("password")
        print(thread_password)
        hashed_password=sha256(thread_password.encode('utf-8')).hexdigest()
        print(hashed_password)
    except:
        thread_privacy="N"
        hashed_password=None
    if payment_method =="stripe":
        thread_price*=100
        if profile.stripe_customer_id == None:
            account= CreateAccount(created_by)
            if type(account) == str:
                 response=JsonResponse({"message":account},safe=False)
            CreateCustomer(created_by)
        if profile.payment_method_id == None:
            return JsonResponse({"message":"CardInput"},safe=False)
        product=stripe.Product.create(name=f"{request.user.username}")
        plan= CreatePlan(product,thread_price)
        thread_new=Thread.objects.create(
        admin=profile,
        monthly_charge= thread_price/100,
        product_id=product.id,
        plan_id=plan.id,
        privacy=thread_privacy,
        password=hashed_password,
        payment_method=payment_method
    )
    else:
        print("PAYPALLL")
        req_id=request.user.username+str(random.randint(0,999999999))
        hashed_request_id=sha256(req_id.encode('utf-8')).hexdigest()
        
        # global access_token
        access_token=request.session.get('access_token')
        product=paypal.CreateProduct(access_token,hashed_request_id,request.user,thread_price)
        plan=paypal.CreatePlan(access_token,product,thread_price)
        thread_new=Thread.objects.create(
            admin=profile,
            monthly_charge= thread_price,
            product_id=product,
            plan_id=plan,
            payment_method="paypal",
            privacy=thread_privacy,
            password=hashed_password
        )
    return JsonResponse({"message":"Success"},status=200)
@csrf_exempt
def Join_Thread(request):
    

    thread_id=request.POST.get("thread_id")
    thread_password=request.POST.get("password")
    print(thread_id,thread_password)
    hashed_password=sha256(thread_password.encode('utf-8')).hexdigest()
    profile=Profile.objects.get(user=request.user)
    if profile.stripe_customer_id == None:
        customer=CreateCustomer(request.user)
    if profile.stripe_account_id == None:
        account=CreateAccount(request.user)
    if profile.payment_method_id== None:
        return JsonResponse({"message":"No Card"}) 
    thread_to_join=Thread.objects.get(pk=thread_id)
    if thread_to_join.password != hashed_password:
        return JsonResponse({"message":"Incorrect password"})
    thread_to_join.participants.add(profile)
    thread_to_join.save()
    user=User.objects.get(pk=request.user.id)
    

    return JsonResponse({"Thread":thread_id,"message":"Success"},safe=False)

def Start(request,thread_id):
    thread=Thread.objects.get(pk=int(thread_id))
    thread.status="A"
    thread.save()
    members=thread.participants.all()
    if len(members) <4:
        return render(request,"inbox.html",{"alert":True,"message":"Cannot start until 4 members Join"})
    profiles=[]
    print(members)
    if thread.payment_method =="stripe":
        for i in members:
            profile_user=Profile.objects.get(user=i)
            profiles.append(profile_user)
            try:
                subscription = stripe.Subscription.create(
                customer=profile_user.stripe_customer_id,
                items=[{'plan': thread.plan_id}],
                    )
            except:
                return HttpResponse(f"{User.objects.get(pk=i.pk).username} has no payment source attached")
    else:
        subscriptions=PaypalSubscription.objects.filter(thread=thread)
        access_token=request.session.get("access_token")
        for i in subscriptions:
            try:
                paypal.ResumeSubscription(i.subscription_id,access_token)
            except:
                return HttpResponse("Some error has occured while Starting")
            
    context={'active':True}
    return render(request,'inbox.html',context)
    # return redirect(inbox(request,thread_id))

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  event = None

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    # Then define and call a method to handle the successful payment intent.
    # handle_payment_intent_succeeded(payment_intent)
  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    # Then define and call a method to handle the successful attachment of a PaymentMethod.
    # handle_payment_method_attached(payment_method)
  # ... handle other event types
  elif event.type =="invoice.paid" and event.data.object.lines.data.type=="subscription":
      raise Exception ("STOPPP FOUND USERRR")
      print("Making payment to user")
      plan_id=event.data.object.lines.data[0].plan
      thread=Thread.objects.get(plan_id=plan_id)
      receiver= thread.to_receive
      stripe.Transfer.create(
        amount=event.data.amount,
        currency="usd",
        destination=receiver.stripe_account_id,
        
        )

  else:
    print(event)
    print('Unhandled event type {}'.format(event.type))

  return HttpResponse(status=200)

def CardInput(request):
    if request.method=="POST":
        
        card=request.POST.get("card")
        cvc=request.POST.get("cvc")
        exp_month=request.POST.get("exp_month")
        exp_year=request.POST.get("exp_year")
        user=request.user
        profile=Profile.objects.get(user=request.user)
        if profile.stripe_customer_id == None:
            customer=CreateCustomer(request.user)
        if profile.stripe_account_id == None:
            account= CreateAccount(request.user)
        try:
            Payment_Method=CreatePaymentMethod(card,cvc,exp_month,exp_year)
        except:
            message="Invalid Card Credentials"
            return render(request,'cardinput.html',{"message":message})
        profile.payment_method_id=Payment_Method.id
        profile.save()
        try:
            stripe.PaymentMethod.attach(
                Payment_Method.id,
                customer=profile.stripe_customer_id
            )
        except:
            return HttpResponse(f"{user.username} has incomplete data")
        return redirect("home")
    return render(request,"cardinput.html")
def paypalhook(request):
    # return HttpResponse(status=200)
    print(request.POST)