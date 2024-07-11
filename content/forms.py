# content/forms.py

from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'price'] 

class StockSearchForm(forms.Form):
    company_name = forms.CharField(max_length=100, label='Company Name', widget=forms.TextInput(attrs={
        'placeholder': 'Enter company name or symbol',
        'class': 'form-control'
    }))



def search_stock(request):
    form = StockSearchForm()
    if request.method == 'POST':
        form = StockSearchForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            # Perform search or other actions with company_name
            # Example: search_results = Stock.objects.filter(name__icontains=company_name)
            # Replace with your search logic
            return render(request, 'content/search_results.html', {'form': form, 'company_name': company_name})
    return render(request, 'content/search_stock.html', {'form': form})