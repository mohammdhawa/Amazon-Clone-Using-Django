from django.shortcuts import render, redirect
from .forms import SignupForm, UserActivateForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile
from products.models import (Product, Brand, Review)
from orders.models import Order

# Create your views here.

def signup(request):
    '''
        - create new user
        - send email: code
        - redirect: activate
    '''
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            user = form.save(commit=False)
            user.is_active = False

            form.save() # trigger signal --> create profile: code
            profile = Profile.objects.get(user__username=username)

            send_mail(
                "Activate Your Account",
                f"Welcome {username}\nUse this code {profile.code} to activate your account.",
                "ismekbektop@gmail.com",
                [f"{email}"],
                fail_silently=False,
            )

            return redirect(f'/accounts/{username}/activate')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def user_activate(request, username):
    '''
    - code --> activate user
    - redirect: login
    '''
    profile = Profile.objects.get(user__username=username)
    if request.method == 'POST':
        form = UserActivateForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if profile.code == code:
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
                profile.save()

                return redirect('login')

    else:
        form = UserActivateForm()

    return render(request, 'accounts/activate.html', {'form': form})


def dashboard(request):
    products_count = Product.objects.count()
    brands_count = Brand.objects.count()
    reviews_count = Review.objects.count()
    orders_count = Order.objects.count()
    users_count = User.objects.count()

    new_prodcucts = Product.objects.filter(flag='New').count()
    sale_products = Product.objects.filter(flag='Sale').count()
    feature_products = Product.objects.filter(flag='Feature').count()

    context = {
        'products_count': products_count,
        'brands_count': brands_count,
        'reviews_count': reviews_count,
        'orders_count': orders_count,
        'users_count': users_count,
        'new_prodcucts': new_prodcucts,
        'sale_products': sale_products,
        'feature_products': feature_products,
    }

    return render(request, 'accounts/dashboard.html', context)
