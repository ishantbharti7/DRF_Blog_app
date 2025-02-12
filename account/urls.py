from django.urls import path
from account.views import Registerview,Login
urlpatterns = [
    path('register/', Registerview.as_view()),
    path('login/', Login.as_view()),
]