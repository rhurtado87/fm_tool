# pages/views.py
from django.shortcuts import render , redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

def home(request):
    return render(request, 'pages/home.html')

def portfolio(request):
    return render(request, 'pages/portfolio.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_vail():
            #send email
            email_to = "google@gmail.com"
            email_from = form.cleaned_data["email"]
            name = form.changed_data["name"]
            message = form.cleaned_data["message"]

            html = render_to_string("pages/email.html", request.POST)

            send_mail(
                "Message from " + name,
                message,
                email_from,
                [email_to],
                html_message=html
            )
            return redirect("contact")

    else:
        form = ContactForm()

    return render(request, 'pages/help.html', {"form": form })

def market(request):
    return render(request, 'content/market.html')

def transactions(request):
    return render(request, 'pages/transactions.html')