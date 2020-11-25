from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('signup/',views.Signup,name="signup"),
    path('home/<str:thread_id>',views.inbox,name="inbox")
]