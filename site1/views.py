from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import  RegisterForm
from django.views.generic.edit import FormView
from case.models import *


@login_required
def profile_view(request):
    user = request.user
    items = Item.objects.filter(users=user).order_by('id')
    user_items_count = items.count()
    return render(request, 'main/profile.html', {'items' : items, 'user_items_count' : user_items_count})


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
