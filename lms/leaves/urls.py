from django.urls import path
from.views import LoginView,ApplyLeaveView,MyLeaveRequestView

urlpatterns =[
    path('login/',LoginView.as_view(),name='login'),
    path('apply/', ApplyLeaveView.as_view(), name='apply-leave'),
    path('my-leaves/', MyLeaveRequestView.as_view(), name='my-leaves'),
]