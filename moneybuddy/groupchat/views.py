from django.shortcuts import render,HttpResponse,redirect
from .forms import LoginForm,SignupForm
from django.contrib.auth import login, logout,authenticate
from .models import Thread,ChatMessage,Profile
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.dispatch import Signal
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import asyncio
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
    # Participants=[]
    # for i in threads:
    #     Participants.append(len(i.participants))
    # print(Participants)
    context={"Threads":threads,"User":profile}
    return render(request,"threads.html",context)

def Signup(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            if type(user)==str:
                form=SignupForm()
                message=user
                return render(request,'signup.html',{"form":form,"message":message})
            login(request,user)
            return redirect('CardInput') 
    else:
        form = SignupForm()
    return render(request,"signup.html", {"form":form})
    
def inbox(request,thread_id):
    thread_=Thread.objects.get(pk=int(thread_id))
    messages=ChatMessage.objects.filter(thread=thread_)
    try:
        profile=Profile.objects.get(user=request.user)
    except:
        return redirect('home')
    if request.user==thread_.admin and thread_.status=='N':
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

def Create_Thread(request):
    created_by=request.user
    print(request.POST)
    thread_price=int(request.POST.get("price"))*100
    product=stripe.Product.create(name=f"{request.user.username}")
    profile=Profile.objects.get(user=request.user)
    plan=stripe.Plan.create(
        product=product.id,
        nickname='Initial Plan',
        interval='month',
        currency='usd',
        amount=thread_price,
    )
    thread_new=Thread.objects.create(admin=profile,monthly_charge= thread_price/100,product_id=product.id,plan_id=plan.id)
    return redirect('home')
@csrf_exempt
def Join_Thread(request):
    thread_id=request.POST.get("thread_id")
    profile=Profile.objects.get(user=request.user)
    thread_to_join=Thread.objects.get(pk=thread_id)
    thread_to_join.participants.add(profile)
    thread_to_join.save()
    user=User.objects.get(pk=request.user.id)
    

    return JsonResponse({"Thread":thread_id},safe=False)

def Start(request,thread_id):
    thread=Thread.objects.get(pk=int(thread_id))
    thread.status="A"
    members=thread.participants.all()
    profiles=[]
    print(members)
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
        profile=Profile.objects.get(user=request.user)
        try:
            Payment_Method=stripe.PaymentMethod.create(
                type="card",
                card={
                    "number":card,
                    "cvc":cvc,
                    'exp_month':exp_month,
                    'exp_year':exp_year
                }
            )
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