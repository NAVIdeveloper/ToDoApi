from django.urls import path,include
from .views import *

urlpatterns = [
    path("register/",     Register),
    path("task/",         Task_View),
    path("task/<int:pk>/",One_Task_View),
    path("task/filter/",  Filter_Task_View),    
    path("task/update/<int:pk>/",Update_Task_View),
    path("login/",Login)
]