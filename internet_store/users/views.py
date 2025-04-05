from django.shortcuts import render,redirect
from .models import Users
from .forms import UsersForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
# from django.views.generic import UpdateView, DeleteView, DetailView

# Create your views here.
def registration(request):
    error = ''
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            card_number = form.cleaned_data['card_number']

            user = Users.objects.create_user(first_name=first_name, last_name=last_name,
                                            password=password, email=email, card_number=card_number)
            user.save()
            return redirect('home')
        else:
            error = 'The form was filled out incorrectly'
    
    form = UsersForm()

    data = {
        'form': form,
        'error': error
        }
    # GET request
    return render(request, 'users/registration.html', data)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Fill in all fields")
            return render(request, 'users/login.html')
        
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('store')
        else:
            messages.error(request, "Incorrect email or password")
    
    # GET request or authentication error
    return render(request, 'users/login.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out of your account.')
    return redirect('login')
