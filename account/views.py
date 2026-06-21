from django.contrib.auth import password_validation, views
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST, require_GET

from . import forms
from .models import CustomUser

import random
import string
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings

_pw_reset_store = {}

ACCOUNT_PROFILE_URL = "account:profile"


class RegistrationView(generic.CreateView):
    form_class = forms.CustomUserCreationForm
    model = CustomUser
    success_url = "/"
    template_name = "account/registration.html"

    def form_invalid(self, form):
        message = password_validation.password_validators_help_text_html()
        return self.render_to_response(
            self.get_context_data(form=form, message=message)
        )


@require_GET
def profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    data = {
        "user name": user.user_name,
        "email": user.email,
        "gender": user.gender,
        "country": user.country.name,
        "city": user.city,
        "birth date": user.birth_date,
    }
    context = {"data": data, "form": forms.ImageForm(), "person": user}
    return render(request, "account/profile.html", context)


@require_POST
def change_image(request):
    form = forms.ImageForm(request.POST, request.FILES)
    if form.is_valid() and form.cleaned_data["main_image"] is not None:
        form.save(request.user)
    return redirect(ACCOUNT_PROFILE_URL, user_id=request.user.id)


@require_POST
def remove_image(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.main_image = forms.default_image[user.gender]
    user.save()
    return redirect(ACCOUNT_PROFILE_URL, user_id=id)


class UpdateProfile(generic.UpdateView):
    form_class = forms.ChangeProfileForm
    model = CustomUser
    pk_url_kwarg = "id"
    template_name = "account/change_profile.html"
    message = "This form is not valid"

    def get_success_url(self):
        return reverse_lazy(ACCOUNT_PROFILE_URL, kwargs={"user_id": self.object.id})

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form, message=self.message)
        )


class PasswordChange(views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = "account/change_password.html"

    def get_success_url(self):
        return reverse_lazy(ACCOUNT_PROFILE_URL, kwargs={"user_id": self.request.user.id})

    def form_invalid(self, form):
        message = password_validation.password_validators_help_text_html()
        return self.render_to_response(
            self.get_context_data(form=form, message=message)
        )


class EmailChange(UpdateProfile):
    form_class = forms.ChangeEmailForm
    template_name = "account/change_email.html"
    message = "Password and/or email is not valid"


class UserList(generic.ListView):
    model = CustomUser
    page_kwarg = 12
    context_object_name = "persons"
    template_name = "account/users.html"

    def get_queryset(self):
        category = self.kwargs.get("category")
        if category == "Staff":
            return CustomUser.objects.filter(is_staff=True)
        if category == "Blocked users":
            return CustomUser.objects.filter(is_active=False)
        if category == "Customers":
            return CustomUser.objects.filter(is_active=True, is_staff=False)
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        category = self.kwargs.get("category")
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            "All users",
            "Staff",
            "Customers",
            "Blocked users",
        )
        if category is not None:
            context["current_category"] = category
        return context


@staff_member_required
@require_POST
def blacklist(request, user_id, category):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_staff or request.user.is_superuser:
        user.is_active = not user.is_active
        user.save()
    return redirect("account:users", category=category)


@staff_member_required
@require_POST
def permissions(request, user_id, category):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_staff or request.user.is_superuser:
        user.is_staff = not user.is_staff
        user.save()
    return redirect("account:users", category=category)


@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        code = ''.join(random.choices(string.digits, k=6))
        # store temporarily in memory mapped by email
        _pw_reset_store[email] = {'code': code, 'user_id': getattr(user, 'id', None)}

        # send email (best-effort)
        try:
            send_mail(
                'Seu código de verificação',
                f'Seu código é: {code}',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'no-reply@example.com',
                [email],
                fail_silently=True,
            )
        except Exception:
            pass

        # redirect to verify page
        request.session['pw_reset_email'] = email
        return redirect('account:password_reset_verify')

    return render(request, 'account/password_reset_request.html')


@require_http_methods(["GET", "POST"])
def password_reset_verify(request):
    email = request.session.get('pw_reset_email')
    if not email:
        return redirect('account:password_reset_request')

    if request.method == 'POST':
        code = request.POST.get('code')
        entry = _pw_reset_store.get(email)
        if entry and entry.get('code') == code:
            request.session['pw_reset_verified'] = True
            return redirect('account:password_reset_new')
        else:
            return render(request, 'account/password_reset_verify.html', {'error': 'Código inválido.'})

    return render(request, 'account/password_reset_verify.html')


@require_http_methods(["GET", "POST"])
def password_reset_new_password(request):
    email = request.session.get('pw_reset_email')
    verified = request.session.get('pw_reset_verified')
    if not email or not verified:
        return redirect('account:password_reset_request')

    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return render(request, 'account/password_reset_new.html', {'error': 'As senhas não coincidem.'})
        # find user
        entry = _pw_reset_store.get(email, {})
        user_id = entry.get('user_id')
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(password)
                user.save()
                # cleanup
                _pw_reset_store.pop(email, None)
                request.session.pop('pw_reset_verified', None)
                request.session.pop('pw_reset_email', None)
                return redirect('account:password_reset_done')
            except CustomUser.DoesNotExist:
                pass
        return render(request, 'account/password_reset_new.html', {'error': 'Usuário não encontrado.'})

    return render(request, 'account/password_reset_new.html')


def password_reset_done(request):
    return render(request, 'account/password_reset_done.html')
