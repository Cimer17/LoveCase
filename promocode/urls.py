from .views import paymants
from django.urls import path

urlpatterns = [ 
    path('paymants/', paymants, name='paymants')
]