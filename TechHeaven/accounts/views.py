from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from .forms import SignUpForm, CustomAuthenticationForm, CustomSetPasswordForm, CustomPasswordResetForm
from .token import account_activation_token

User = get_user_model()



def home_view(request):
    return render(request, 'layout.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # make sure still inactive (redundant safety)
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = request.build_absolute_uri(reverse('activate', args=[uid, token]))

            message = f'Hi {user.email}, click here to activate your account: {activation_link}'
            send_mail('Activate your account', message, settings.EMAIL_HOST_USER, [user.email])
            print(f"Activation link: {activation_link}")  # Debugging line

            return render(request, 'accounts/email_sent.html', {'email': user.email})
        else:
            return HttpResponse('Invalid form submission.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Account activated successfully! <a href="/login/">Login here</a>')
    else:
        return HttpResponse('Activation link invalid!')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))
                message = f'Hi {user.email}, click here to reset your password: {reset_link}'
                send_mail('Password Reset', message, settings.EMAIL_HOST_USER, [user.email])

            return render(request, 'accounts/email_sent.html', {'email': email})
    else:
        form = CustomPasswordResetForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Password reset successful! <a href="/login/">Login here</a>')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'accounts/reset_password_form.html', {'form': form})
    else:
        return HttpResponse('Reset link invalid or expired.')
