from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users
import bcrypt

# Create your views here.
def index_page(request):
    return render(request, 'index_page.html')

def register_page(request):
    return render(request, 'register_page.html')

def login_page(request):
    return render(request, 'login_page.html')

def register(request):
    errors = Users.objects.user_validator(request.POST)
    if request.method == 'POST':
        if errors: 
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/user/register_page')
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = Users.objects.create(
            f_name=request.POST['f_name'],
            l_name=request.POST['l_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            password=hash_pw
        )
        request.session['logged_user'] = new_user.id
        return redirect('/user/account_page')
    return redirect('/user/register_page')

def login(request):
    if request.method == 'POST':
        user = Users.objects.filter(email=request.POST['email'])
        # Use filter over get because if there is no email that matches request.POST an error will occur, filter does not do this
        if user:  # saying if there is a user, boolean
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                # compares the Posted password to the one stored within the database
                # Puts the logged in user to session, only if the password is correct.
                request.session['logged_user'] = log_user.id
                return redirect('/user/account_page')
        messages.error(request, "Email or password are incorrect")
    return redirect('/user/login_page')

def account_page(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in to be here!")
        return redirect('/')
    context = {
        'logged_user': Users.objects.get(id=request.session['logged_user']),
    }
    return render(request, 'account_page.html', context)

def update_info(request):
    errors = Users.objects.user_update_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/user/account_page')
    user = Users.objects.get(id=request.session['logged_user'])
    user.f_name = request.POST['f_name']
    user.l_name = request.POST['l_name']
    user.email = request.POST['email']
    user.address = request.POST['address']
    user.city = request.POST['city']
    user.state = request.POST['state']
    user.save()
    return redirect('/user/account_page')

def logout(request):
    request.session.flush()
    return redirect('/')