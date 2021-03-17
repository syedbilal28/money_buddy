from django.contrib import admin
from .models import PaypalPayout,ChatMessage,Thread,ThreadManager,Profile,PaypalSubscription,PaypalSubscriptionPayment
# Register your models here.
admin.site.register(Profile)
admin.site.register(PaypalSubscription)
admin.site.register(PaypalPayout)
admin.site.register(PaypalSubscriptionPayment)
class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)
