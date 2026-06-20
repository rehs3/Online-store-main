from django.contrib.auth import password_validation, views
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST, require_GET

from . import forms
from .models import CustomUser

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
