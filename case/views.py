from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.urls import reverse
from case.urls import *
from django.db.models import Sum
from telegram import *
from profiles.models import UserProfile
from .hash import *
import random

def index(request):
    cases_popular = Case.objects.order_by('-id')[:6]
    categories = Category.objects.all()
    data = {
        'cases' : cases_popular,
        'categories' :categories,
    }
    data['user_items'] = UserItem.objects.all().count()
    data['user_count'] = User.objects.all().count()
    if request.user.is_authenticated:
        user = request.user
        data['keys_count']= user.profile.keys_count
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
    if request.user.is_authenticated:
        user = request.user
        data['keys_count']= user.profile.keys_count
    return render(request, 'main/case.html', context=data)


def choose_item(request):
    user = request.user
    id = request.GET.get("id")
    # Получаем все элементы с количеством больше 0
    items = Item.objects.filter(cases=id).filter(quantity__gt=0)
    user_profile = UserProfile.objects.get(user=user)
    case = get_object_or_404(Case, pk=id)
    
    if user_profile.keys_count <= 0:
        return JsonResponse({'error': 'Недостаточно ключей для открытия кейса!'})
    
    if items.count() == 0:
        return JsonResponse({'error': 'В кейсе закончились предметы!'})    
    
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
            user_profile.remove_key()
            
            
            server_seed = get_server_seed()
            client_seed = generate_client_seed()
            nonce = get_nonce()
            hash_result = calculate_hash(server_seed, client_seed, nonce)
            UserItem.objects.create(
                user=user,
                item=chosen_item,
                case=case,
                client_seed=client_seed,
                server_seed=server_seed,
                nonce=nonce,
                hash_seed = hash_result,
            )
            link_hash = f'{reverse("index")}gethash/?hash={hash_result}'
            break

    if chosen_item:
        # Возвращаем победителя, все элементы и хеш данных
        items = Item.objects.filter(cases=id)
        serialized_items = [{'name': item.name, 'img_url': item.img.url, 'chance': item.chance, 'rare' : item.rare } for item in items]
        return JsonResponse({'winner': {'name': chosen_item.name, 'img_url': chosen_item.img.url, 'rare' : chosen_item.rare}, 'items': serialized_items, 'hash': hash_result, 'link_hash' : link_hash, 'keys_count': user_profile.keys_count})
    else:
        return JsonResponse({'error': 'Failed to choose item'})

def gethash(request):
    return render(request, 'main/hash.html')

def provably_fair(request):
    if request.method == 'GET':
        hash_value = request.GET.get('hash')
        user_items = UserItem.objects.filter(hash_seed=hash_value)
        if user_items.exists():
            user_item = user_items.first()  # Получаем первый объект UserItem из QuerySet
            user_info = user_item.user.username  # Получаем имя пользователя
            item_info = user_item.item.name  # Получаем название предмета
            case_info = user_item.case.name  # Получаем название кейса
            client_seed_info = user_item.client_seed 
            server_seed_info = user_item.server_seed 
            nonce_info = user_item.nonce
            return JsonResponse({
                'user': user_info,
                'item': item_info,
                'case': case_info,
                'client_seed': client_seed_info,
                'server_seed': server_seed_info,
                'nonce': nonce_info
            })
        else:
            return JsonResponse({'message': 'Об этом хэше нет информации...'})
    else:
        return JsonResponse({'error': 'Не все параметры переданы'})



def get_items(request):
    id = request.GET.get("id")
    items = Item.objects.filter(cases=id)
    serialized_items = [{'name': item.name, 'img_url': item.img.url, 'rare' : item.rare} for item in items]
    total = sum(item.quantity for item in items)
    end = total == 0
    return JsonResponse({'items': serialized_items, 'end' : end})


def cases(request):
    return redirect('/')