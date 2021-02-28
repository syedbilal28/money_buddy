from django.contrib import admin
from .models import ChatMessage,Thread,ThreadManager,Profile,PaypalSubscription
# Register your models here.
admin.site.register(Profile)
admin.site.register(PaypalSubscription)
class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)
