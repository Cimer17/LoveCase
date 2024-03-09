from case.views import *
from django.urls import path

urlpatterns = [ 
    path('', index, name='index'),
    path('choose_item', choose_item, name='choose_item'),
    path('get_items', get_items, name='get_items'), 
    path('case/<int:id>/', case_page, name='news_detail'),
]