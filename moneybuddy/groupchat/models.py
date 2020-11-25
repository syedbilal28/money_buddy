from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import stripe
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
stripe.api_key=settings.STRIPE_API_KEY
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    stripe_id=models.CharField(max_length=120)

@receiver(post_save,sender=User)
def _on_update_user(sender,instance,created,**kwargs):
    if created:
        customer=stripe.Customer.create(
            email=instance.email,
            name=instance.get_full_name(),
            metadata={
                'user_id':instance.pk,
                'username':instance.username
            },
            description="Created from django",
            )
        profile=Profile.objects.create(user=instance,stripe_id=customer.id)
        profile.save()

class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username):  # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
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
    

class Thread(models.Model):
    
    admin= models.ForeignKey(User,on_delete=models.CASCADE,related_name="Admin")
    participants=models.ManyToManyField(User)
    total_buyout=models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        ordering=('total_buyout',)
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
    status= models.CharField(max_length=10,default="Sent")
    class Meta:
        ordering=('timestamp',)