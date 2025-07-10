from django.shortcuts import render,redirect
from .models import Users
from .forms import UsersForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
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
            return redirect('store')
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
        if user is None:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            exists = User.objects.filter(email=email).exists()
            messages.error(request, 
            f"Auth failed (user exists: {exists}, active: {exists and User.objects.get(email=email).is_active})")
        else:
            auth.login(request, user)

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

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Users.objects.filter(email=email).exists:
            user = Users.objects.get(email=email)
            domain = get_current_site(request)

            mail_subject = 'Reset your password'
            message = render_to_string('users/reset_password_email.html',{
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':  default_token_generator.make_token(user)
            })

            send_email = EmailMessage(mail_subject, message, to=[user.email])
            send_email.send()
            messages.success(request, 'Check your email')
            return redirect('forgot_password')
        else:
            messages.error(request, 'Account not found')
            return redirect('forgot_password')
    return render(request, 'users/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Users._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please update your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')
    
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('new_password_confirm')

        if new_password != new_password_confirm:
            messages.error(request, 'Passwords must match')
            return redirect('reset_password') 
        
        if len(new_password) < 8:
            messages.error('Password must be at least 8 characters long')
            return redirect('reset_password')
        
        uid = request.session.get('uid')
        if not uid:
            messages.error(request, 'Session expired')
            return redirect('login')
        
        user = Users.objects.get(pk=uid)
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully')
        return redirect('login')
    else:
        return render(request, 'users/reset_password.html')


# def reset_password(request):
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('new_password_confirm')
        
#         # Валидация паролей
#         if not new_password or not confirm_password:
#             messages.error(request, 'Все поля обязательны для заполнения')
#             return redirect('reset_password')
            
#         if new_password != confirm_password:
#             messages.error(request, 'Пароли не совпадают')
#             return redirect('reset_password')
            
#         if len(new_password) < 8:
#             messages.error(request, 'Пароль должен содержать минимум 8 символов')
#             return redirect('reset_password')

#         # Получаем пользователя из сессии
#         uid = request.session.get('uid')
#         if not uid:
#             messages.error(request, 'Сессия истекла')
#             return redirect('login')
            
#         try:
#             user = Users.objects.get(pk=uid)
            
#             # Отладочный вывод (удалите после проверки)
#             print(f"Текущий хэш: {user.password}")
            
#             # Вариант 1: Стандартный способ (рекомендуется)
#             user.set_password(new_password)
            
#             # Вариант 2: Ручное хэширование (если вариант 1 не работает)
#             # user.password = make_password(new_password)
            
#             user.save()
            
#             print(f"Новый хэш: {user.password}")  # Должен начинаться с pbkdf2_sha256$
            
#             # Очищаем сессию
#             if 'uid' in request.session:
#                 del request.session['uid']
                
#             messages.success(request, 'Пароль успешно изменен!')
#             return redirect('login')
            
#         except Users.DoesNotExist:
#             messages.error(request, 'Пользователь не найден')
#             return redirect('login')
            
#     return render(request, 'users/reset_password.html')

@login_required(login_url='login')
def account(request):
    user_id = request.user.id
    user = Users.objects.get(id = user_id)
    context = {
        'user': user
    }
    return render(request ,'users/account.html',context)