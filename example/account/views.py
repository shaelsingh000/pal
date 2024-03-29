from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from blog.models import BlogPost
from .models import Account

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = 'raw_password')
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)

            if user:
                login(request, user)
                return redirect('home')
            
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'account/login.html', context)

def account_view(request, **a):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial ={
                "email": request.POST["email"],
                "username": request.POST["username"],
                "bio": request.POST["bio"],
            }
            form.save()
            context['success_message']= "Updated"
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
                "bio": request.user.bio,
            }
        )
    context['account_form']= form

    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts

    return render(request, 'account/account.html',context)

def must_authenticate_view(request):
    return render(request,'account/must_authenticate.html',{})

def other_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    user = Account.objects.filter(username=kwargs['username']).first()
    form = {
        "email":user.email,
        "username":user.username,
        "bio": user.bio,
    }
    context["account_form"]= form

    blog_posts = BlogPost.objects.filter(author=user)
    context['blog_posts'] = blog_posts

    return render(request, 'account/other_account.html',context)

def delete(request,*args):
    if not request.user.is_authenticated:
        return redirect("login")
    
    reg=Account.objects.get(username=request.user.username)
    reg.delete()
    return render(request,'account/must_authenticate.html',{})
