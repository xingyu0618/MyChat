from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from ..models import User
from ..forms import AvatarForm, DisplayNameForm, ProfileForm

class BaseProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile_edit")

    def get_object(self, queryset=None):
        profile, _ = User.objects.get_or_create(user=self.request.user)
        return profile


class ProfileEditView(BaseProfileUpdateView):
    form_class = ProfileForm

class AvatarUpdateView(BaseProfileUpdateView):
    form_class = AvatarForm
    template_name = "accounts/avatar_edit.html"
    success_url = reverse_lazy("avatar_edit")

class DisplayNameUpdateView(BaseProfileUpdateView):
    form_class = DisplayNameForm
    template_name = "accounts/display_name_edit.html"
    success_url = reverse_lazy("display_name_edit")
