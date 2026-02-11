from django.urls import path
from.views import LoginView,ApplyLeaveView,MyLeaveRequestView,ApproveLeaveView,RejectLeaveView,AllLeaveRequestView

urlpatterns =[
    path('login/',LoginView.as_view(),name='login'),
    path('apply/', ApplyLeaveView.as_view(), name='apply-leave'),
    path('my-leaves/', MyLeaveRequestView.as_view(), name='my-leaves'),
    path('approve/<int:id>/', ApproveLeaveView.as_view(), name='approve-leave'),
    path('reject/<int:id>/', RejectLeaveView.as_view(), name='reject-leave'),
    path('all-leaves/', AllLeaveRequestView.as_view(), name='all-leaves'),

]