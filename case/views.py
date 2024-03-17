from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from case.urls import *
from django.db.models import Sum
from django.urls import reverse
from django.shortcuts import redirect
import random
import hashlib

def index(request):
    cases_popular = Case.objects.order_by('-id')[:6]
    categories = Category.objects.all()
    data = {
        'cases' : cases_popular,
        'categories' :categories,
    }
    data['user_items'] = UserItem.objects.all().count()
    data['user_count'] = User.objects.all().count()
    return render(request, 'main/index.html', context=data)

def case_page(request, id):
    case = get_object_or_404(Case, id=id)
    items = Item.objects.filter(cases=id).order_by('-rare')
    total_quantity = Item.objects.filter(cases=id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    data = {
        'title': case.name.upper(),
        'img_case': case.img_certificates,
        'items' : items,
        'case_items_count': total_quantity,
    }
    data['user_items'] = UserItem.objects.all().count()
    data['user_count'] = User.objects.all().count()
    return render(request, 'main/case.html', context=data)



def choose_item(request):
    user = request.user
    id = request.GET.get("id")
    # Получаем все элементы с количеством больше 0
    items = Item.objects.filter(cases=id).filter(quantity__gt=0)
    if not items.exists():
        # Если предметы закончились, возвращаем соответствующий ответ
        return JsonResponse({'end': True})
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
            UserItem.objects.create(user=user, item=chosen_item) 
            # Хешируем важные данные, связанные с выбором элемента, для обеспечения "доказуемой справедливости"
            hash_data = f"{user.username}-{chosen_item.id}-{id}".encode()
            hash_result = hashlib.md5(hash_data).hexdigest()
            Game.objects.create(user=user, chosen_item_id=chosen_item.id, case_id=id, hash_value=hash_result)
            link_hash = f'{reverse("index")}gethash/?hash={hash_result}&username={user}&chosen_item_id={chosen_item.id}&case_id={id}'
            break

    if chosen_item:
        # Возвращаем победителя, все элементы и хеш данных
        items = Item.objects.filter(cases=id)
        serialized_items = [{'name': item.name, 'img_url': item.img.url, 'chance': item.chance, 'rare' : item.rare } for item in items]
        return JsonResponse({'winner': {'name': chosen_item.name, 'img_url': chosen_item.img.url, 'rare' : chosen_item.rare}, 'items': serialized_items, 'hash': hash_result, 'link_hash' : link_hash})
    else:
        return JsonResponse({'error': 'Failed to choose item'})



def get_items(request):
    id = request.GET.get("id")
    items = Item.objects.filter(cases=id)
    serialized_items = [{'name': item.name, 'img_url': item.img.url, 'rare' : item.rare} for item in items]
    total = sum(item.quantity for item in items)
    end = total == 0
    return JsonResponse({'items': serialized_items, 'end' : end})


def cases(request):
    return redirect('/')