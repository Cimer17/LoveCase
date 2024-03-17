import hashlib
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import  RegisterForm
from django.views.generic.edit import FormView
from case.models import *
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from telegram import *


@login_required
def profile_view(request):
    user = request.user
    items = Item.objects.filter(users=user).order_by('-useritem__received_at')
    user_items_conclusion_false = UserItem.objects.filter(user=user, conclusion=True).order_by('item__id').count()
    paginator = Paginator(items, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_items_count = items.count()
    total = user_items_count - user_items_conclusion_false
    data = {
        'total'  : total, 
        'user_items_count': user_items_count,
        'items_conclusion' : user_items_conclusion_false, 
        'page_obj': page_obj
    }
    data['user_items'] = UserItem.objects.all().count()
    data['user_count'] = User.objects.all().count()
    return render(request, 'main/profile.html', context=data)

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

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
    
@login_required
def send_message_to_telegram(request):
    user = request.user
    # Получаем все объекты UserItem для данного пользователя с conclusion=False
    user_items_conclusion_false = UserItem.objects.filter(user=user, conclusion=False)
    count_fal = user_items_conclusion_false.count()
    if count_fal == 0:
        return HttpResponse("Нет предметов для вывода")
    # Создаем словарь для хранения количества каждого предмета
    items_count_dict = {}
    # Заполняем словарь количеством каждого предмета
    for user_item in user_items_conclusion_false:
        item_name = user_item.item.name
        items_count_dict[item_name] = items_count_dict.get(item_name, 0) + 1
    # Формируем список строк для сообщения в телеграм
    items_list = [f"{index + 1}. {name} - {count} шт." for index, (name, count) in enumerate(items_count_dict.items())]
    user_items_conclusion_false.update(conclusion=True) 
    # Формируем текст сообщения
    message = f'Вывод для пользователя {user}'
    info = f'Количество предметов - {count_fal}'
    data = {
        'message': message,
        'info': info,
        'items_list': items_list,  # Добавляем список предметов в данные для отправки в Telegram
    }
    send_news_to_telegram(data)
    return HttpResponse("Сообщение отправлено")
