from django.shortcuts import render,HttpResponse,redirect
from .forms import LoginForm,SignupForm
from django.contrib.auth import login, logout,authenticate
from .models import Thread,ChatMessage,Profile
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

stripe.api_key = "sk_test_51HpXfpJEfpDOgYo1UQu5PZvq3Rj1bVWGbW1WcyRvh2jBZpJVRyu4kJ8uVzAItLgk07ZCi90VeRHXqMANxYhode1800WXZCTuuR"
# Create your views here.
@csrf_exempt
def index(request):
    if request.method=="POST":
        print("POSTED")
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

        form = LoginForm()
        return render(request,'index.html',{"form":form})
def home(request):
    threads=Thread.objects.all()
    # Participants=[]
    # for i in threads:
    #     Participants.append(len(i.participants))
    # print(Participants)
    context={"Threads":threads}
    return render(request,"threads.html",context)

def Signup(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') #FUNCTION KA NAAM
    else:
        form = SignupForm()
    return render(request,"signup.html", {"form":form})
    
def inbox(request,thread_id):
    thread_=Thread.objects.get(pk=int(thread_id))
    messages=ChatMessage.objects.filter(thread=thread_)
    context={"messages":messages,"thread":thread_}
    return render(request,'inbox.html',context)
def Logout(request):
    logout(request.user)
    return redirect ('index')
def About_us(request):
    return redirect('home')

def Create_Thread(request):
    created_by=request.user
    print(request.POST)
    thread_price=request.POST.get("price")
    product=stripe.Product.create(name=f"{request.user.username}")
    plan=stripe.Plan.create(
        product=product.id,
        nickname='Initial Plan',
        interval='month',
        currency='usd',
        amount=thread_price,
    )
    thread_new=Thread.objects.create(admin=request.user,total_buyout=thread_price,product_id=product.id,plan_id=plan.id)
    return redirect('home')
@csrf_exempt
def Join_Thread(request):
    thread_id=request.POST.get("thread_id")
    thread_to_join=Thread.objects.get(pk=thread_id)
    thread_to_join.participants.add(request.user)
    thread_to_join.save()
    user=User.objects.get(pk=request.user.id)
    profile=Profile.objects.get(user=user)
    
    subscription = stripe.Subscription.create(
    customer=profile.stripe_id,
    items=[{'plan': thread_to_join.plan_id}],
        )
    return redirect('home')