from django.shortcuts import render,HttpResponse,redirect
from .forms import LoginForm,SignupForm
from django.contrib.auth import login, logout,authenticate
from .models import Thread,ChatMessage
# Create your views here.
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
    context={"messages":messages}
    return render(request,'inbox.html',context)