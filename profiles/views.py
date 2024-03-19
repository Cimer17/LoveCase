from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import  RegisterForm
from django.views.generic.edit import FormView
from case.models import Item, UserItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from telegram import send_news_to_telegram

@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    items = Item.objects.filter(users=profile_user).order_by('-useritem__received_at')
    user_items_conclusion_false = UserItem.objects.filter(user=profile_user, conclusion=True).order_by('item__id').count()
    paginator = Paginator(items, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_items_count = items.count()   
    total = user_items_count - user_items_conclusion_false
    data = {
        'total': total, 
        'user_items_count': user_items_count,
        'items_conclusion': user_items_conclusion_false, 
        'page_obj': page_obj,
        'profile_user': profile_user
    }
    data['user_items'] = UserItem.objects.all().count()
    data['user_count'] = User.objects.all().count()
    data['keys_count'] = profile_user.profile.keys_count
    return render(request, 'main/profile.html', context=data)

@login_required
def profiles(request):
    user = request.user
    return redirect(f'/profile/{user.id}')

@login_required
def send_message_to_telegram(request):
    user = request.user
    # Получаем все объекты UserItem для данного пользователя с conclusion=False
    user_items_conclusion_false = UserItem.objects.filter(user=user, conclusion=False)
    count_fal = user_items_conclusion_false.count()
    if count_fal == 0:
        return JsonResponse({"error": "Нет предметов для вывода!"})
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
    return JsonResponse({"message": f"{user}, запрос на вывод предметов для отправлен!"})

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)