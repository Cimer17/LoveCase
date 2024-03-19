from django import forms

class PromoCodeForm(forms.Form):
    promo_code = forms.CharField(max_length=20, label='Промокод')