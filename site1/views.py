import hashlib
from django.shortcuts import render
from case.models import *
from django.http import JsonResponse
from telegram import *

def gethash(request):
    return render(request, 'main/hash.html')

def provably_fair(request):
    if request.method == 'GET':
        received_hash = request.GET.get('hash')
        username = request.GET.get('username')
        chosen_item_id = request.GET.get('chosen_item_id')
        case_id = request.GET.get('case_id')
        if username and chosen_item_id and case_id:
            # Формируем строку данных для хеширования
            hash_data = f"{username}-{chosen_item_id}-{case_id}".encode()
            hash_result = hashlib.md5(hash_data).hexdigest()
            # Сравниваем полученный хеш с хешем из запроса
            if hash_result == received_hash:
                return JsonResponse({'result': 'OK'})
            else:
                return JsonResponse({'result': 'FAIL'})
        else:
            # Если не переданы все необходимые параметры, возвращаем сообщение об ошибке
            return JsonResponse({'error': 'Не все параметры переданы'})
    else:
        return JsonResponse({'error': 'Неверный метод запроса'})