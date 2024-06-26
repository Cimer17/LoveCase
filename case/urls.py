from .views import *
from site1.views import *
from django.urls import path

urlpatterns = [ 
    path('', index, name='index'),
    path('case/', cases, name='cases'),
    path('case/<int:id>/', case_page, name='news_detail'),
    path('choose_item/', choose_item, name='choose_item'),
    path('get_items/', get_items, name='get_items'),
    path('provablyfair/', provably_fair, name='provably_fair'),
    path('gethash/', gethash, name='gethash'),
]