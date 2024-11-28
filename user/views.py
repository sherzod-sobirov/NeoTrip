from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.contrib.auth.hashers import make_password
from django.urls import reverse


def my_context_processor(request):
    context = {
        "current_site_url": get_current_site(request)
    }
    return context


def forgot_password(request):
    # Ensure the email is provided before proceeding
    email = request.POST.get('email')
    if email:
        try:
            user = get_object_or_404(User, email=email)
            current_site = get_current_site(request)
            mail_subject = "Password Reset"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            reset_url = reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
            reset_link = f"{current_site.domain}{reset_url}"

            message = render_to_string('user/reset_password.html', {
                'domain': current_site.domain,
                'reset_link': reset_link
            })

            email = EmailMessage(mail_subject, message, to=[email])
            email.send()
            return render(request, 'user/login.html', {"link_sent": 1})
        except User.DoesNotExist:
            return render(request, 'user/login.html', {"error_message": "Email not found"})
    return render(request, 'user/login.html', {"error_message": "Please provide an email address."})


class LoginView(View):
    def get(self, request):
        # Login sahifasini qaytarish
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Foydalanuvchini autentifikatsiya qilish
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('main_home_view')  # Muvaffaqiyatli kirishdan keyin yo'naltirish

        # Xatoliklarni boshqarish
        if not User.objects.filter(email=email).exists():
            error_message = "Invalid email address!"  # Email noto'g'ri
        else:
            error_message = "Incorrect password!"  # Parol noto'g'ri

        return render(request, 'user/login.html', {"error_message": error_message})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main_home_view')


def email_send(request, user):
    current_site = get_current_site(request)
    mail_subject = f"MAROKAND TOUR подтверждение электронной почты"
    message = render_to_string('user/email_confirmation.html', {
        'user': user.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    email = EmailMessage(
        mail_subject,
        message,
        to=[request.POST['email']],
    )
    email.send()


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email_send(request, user)
            return render(request, 'user/signup.html', {"link_send": 1})
        return render(request, 'user/signup.html', {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'user/login.html', {"email_confirmed": 1})
    else:
        return HttpResponse("This link is expired")


from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy


class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/reset_password.html'
    success_url = reverse_lazy('password_reset_done')  # Email yuborilganidan keyin

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/reset_password_sent.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/reset_password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')  # Parol muvaffaqiyatli tiklangandan keyin

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/reset_password_complete.html'




