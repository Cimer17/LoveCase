from case.views import *
from django.urls import path

urlpatterns = [ 
    path('', index, name='index'),
    path('case/', case_page, name='case'),
    path('choose_item', choose_item, name='choose_item'),
    path('get_items', get_items, name='get_items'), 
    path('cases/', cases, name='index'),
]