from django.shortcuts import render, redirect
from .models import PromoCode, UsedPromoCode
from django.contrib.auth.decorators import login_required
from .forms import PromoCodeForm
from telegram import send_activate_promo

@login_required
def paymants(request):
    form = PromoCodeForm()
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            promo_code = form.cleaned_data['promo_code']
            try:
                promo = PromoCode.objects.get(code=promo_code)
                if promo.is_single_use and promo.activations_left == 0:
                    return render(request, 'main/paymants.html', {'form': form, 'error': 'Промокод уже использован'})
                elif UsedPromoCode.objects.filter(user=request.user, promo_code=promo).exists():
                    return render(request, 'main/paymants.html', {'form': form, 'error': 'Промокод уже был введен вами!'})
                else:
                    user_profile = request.user.profile
                    user_profile.add_key(promo.keys_count)
                    if promo.is_single_use:
                        promo.activations_left -= 1
                        promo.save()
                    UsedPromoCode.objects.create(user=request.user, promo_code=promo)
                    
                    data = {
                        'title' : f'⚡Пользователь {request.user} ввёл промокод - {promo_code}',
                        'message' : f'Промкод дал {promo.keys_count}🔑',
                    }
                    send_activate_promo(data)
                    
                    return redirect('paymants')
            except PromoCode.DoesNotExist:
                return render(request, 'main/paymants.html', {'form': form, 'error': 'Промокод недействителен'})
    return render(request, 'main/paymants.html', {'form': form})