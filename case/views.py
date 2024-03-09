from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
import random

def case_page(request):
    return render(request, 'main/case.html')

def index(request):
    return render(request, 'main/index.html')

def cases(request):
    return render(request, 'main/cases.html')

def choose_item(request):
    # Получаем все элементы с количеством больше 0
    items = Item.objects.filter(quantity__gt=0)
    if not items.exists():
        return JsonResponse({'error': 'No items available'})
    # Рассчитываем общий шанс для выбора элемента
    total_chance = sum(item.chance for item in items)
    # Генерируем случайное число в диапазоне от 0 до общего шанса
    rand_num = random.uniform(0, total_chance)
    cumulative_chance = 0
    chosen_item = None
    # Выбираем победителя на основе случайного числа
    for item in items:
        cumulative_chance += item.chance
        if rand_num <= cumulative_chance:
            chosen_item = item
            # Уменьшаем количество предметов у победителя
            chosen_item.quantity -= 1 
            chosen_item.save() 
            break
    if chosen_item:
        # Возвращаем победителя и все элементы
        items = Item.objects.all()
        serialized_items = [{'name': item.name, 'img_url': item.img.url, 'chance': item.chance, 'rare' : item.rare } for item in items]
        return JsonResponse({'winner': {'name': chosen_item.name, 'img_url': chosen_item.img.url, 'rare' : chosen_item.rare}, 'items': serialized_items})
    else:
        return JsonResponse({'error': 'Failed to choose item'})


def get_items(request):
    items = Item.objects.all()
    serialized_items = [{'name': item.name, 'img_url': item.img.url, 'rare' : item.rare} for item in items]
    return JsonResponse({'items': serialized_items})