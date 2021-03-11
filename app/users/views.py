from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from guardian.mixins import PermissionRequiredMixin as ObjectPermissionRequiredMixin
from oidc_provider.models import UserConsent

from .forms import UserForm

UserModel = get_user_model()


class UserProfileView(ObjectPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/user_detail.html'
    form_class = UserForm
    permission_required = ['users.change_user', 'users.view_user']
    success_message = _('Your profile has been updated successfully!')

    def get_context_data(self, **kwargs):
        ctx = super(UserProfileView, self).get_context_data(**kwargs)
        user = self.get_object()
        consents = UserConsent.objects.filter(user=user).order_by('-id')
        ctx.update({'consents': consents})
        return ctx

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user-profile')
