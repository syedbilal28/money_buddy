from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('signup/',views.Signup,name="signup"),
    path('home/<str:thread_id>',views.inbox,name="inbox"),
    path('logout/',views.Logout,name="Logout"),
    path('aboutus/',views.About_us,name="aboutus"),
    path('create_thread/',views.Create_Thread,name="create-thread"),
    path('join/',views.Join_Thread,name="Join"),
    path('Start/<str:thread_id>/',views.Start,name="Start"),
    path("hooks/",views.my_webhook_view,name="Hook"),
    path("card/",views.CardInput,name="CardInput"),
    path("plan/",views.GetPlanId,name="Plan"),
    path("PaypalSubscribe/",views.CreatePaypalSubscription,name="CreateSubscription"),
    path("Paypalhook/",views.paypalhook,name="paypalHook"),
    path("how-it-works/",views.howitworks,name="HowItWorks")
]
