from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import stripe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django_countries.fields import CountryField
import os

stripe.api_key=settings.STRIPE_API_KEY
# Create your models here.
def to_upload_profile_picture(instance,filename):
    # path_to_upload=os.path(instance.username+"/ProfilePicture")
    directory= os.path.join(settings.MEDIA_ROOT,instance.user.username)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,'ProfilePicture')
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"{instance.user.username}/ProfilePicture/{filename}"


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    stripe_customer_id=models.CharField(max_length=120,unique=True,null=True,blank=True)
    stripe_account_id=models.CharField(max_length=120,unique=True,null=True,blank=True)
    country=CountryField()
    payment_method_id=models.CharField(max_length=120,default=None,blank=True,null=True)
    profile_picture=models.ImageField(upload_to=to_upload_profile_picture,default='defaultprofile.jpg')
    def __str__(self):
        return self.user.username
        

class ThreadManager(models.Manager):
    def by_roomname(self, roomname):
        qlookup = Q(pk=roomname) 
        # qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).distinct()
        return qs

    def get_or_new(self, roomname):  # get_or_create
        # username = user.username
        # if username == other_username:
        #     return None
        qlookup1 = Q(pk=roomname)
        # qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False
class PaypalSubscriptionPayment(models.Model):
    payer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    thread=models.ForeignKey("Thread",on_delete=models.SET_NULL,null=True)
    amount=models.FloatField(default=0)
class PaypalSubscription(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    thread=models.ForeignKey('Thread',on_delete=models.CASCADE)
    subscription_id=models.CharField(max_length=5000)

class PaypalPayout(models.Model):
    receiver=models.ForeignKey(User,on_delete=models.CASCADE)
    plan_id=models.CharField(max_length=200,null=True)
    amount=models.FloatField()
    datetime=models.DateTimeField(auto_now_add=True)

class Thread(models.Model):
    
    admin= models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="Admin")
    participants=models.ManyToManyField(Profile,related_name="Participants")
    PAYMENT_CHOICES=[
        ("P","Paypal"),
        ("S","Stripe")
    ]
    payment_method=models.CharField(max_length=1,choices=PAYMENT_CHOICES,default=None)
    monthly_charge=models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    product_id=models.CharField(max_length=30,blank=True)
    plan_id=models.CharField(max_length=30,blank=True,null=True)
    password=models.CharField(max_length=50,null=True)
    PRIVACY_CHOICES=[
        ("P","protected"),
        ("N","Public")
    ]
    privacy=models.CharField(max_length=10,default="N",null=True)
    Status_Choices=[
        ("A","Active"),
        ("N","Not Active")
    ]
    
    status=models.CharField(max_length=1,choices=Status_Choices,default="N")
    to_receive=models.OneToOneField(Profile,on_delete=models.CASCADE,blank=True,null=True)
    cycle=models.IntegerField(default=0)
    order=models.CharField(max_length=500,null=True)

    objects = ThreadManager()
    class Meta:
        ordering=('monthly_charge',)
    def __str__(self):
        return self.admin.user.username
    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=('timestamp',)

# class Liabililities(models.Model):
