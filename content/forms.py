from django import forms
from django_select2 import forms as select2forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'price']
        
    symbol = select2forms.ModelSelect2Widget(
        queryset=Stock.objects.all(),
        search_fields=['symbol__icontains', 'name__icontains'],
        attrs={'data-minimum-input-length': 1})

class StockSearchForm(forms.Form):
    company_name = forms.CharField(max_length=100, label='Enter company name or symbol', widget=forms.TextInput(attrs={
        'placeholder': 'name or (AAA),(AAAA)',
        'class': 'form-control'
    }))
