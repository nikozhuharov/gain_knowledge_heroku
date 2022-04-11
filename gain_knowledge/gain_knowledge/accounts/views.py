from django.http import HttpResponseRedirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, logout
from django.urls import reverse_lazy

from gain_knowledge.accounts.forms import CreateProfileForm, EditProfileForm, ChangePasswordForm, LoginForm
from gain_knowledge.accounts.models import Profile, GainKnowledgeUser, CurrentResult


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    form_class = LoginForm
    success_url = reverse_lazy('list categories')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class UserRegisterView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('login user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object is a Profile instance
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })

        return context


class EditProfileView(views.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class DeleteProfileView(views.DeleteView):
    model = Profile
    template_name = 'accounts/profile_delete.html'
    fields = ('first_name', 'last_name', 'picture', 'date_of_birth', 'email', 'gender')

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        user = GainKnowledgeUser.objects.filter(id=self.object.user_id)
        current_result = CurrentResult.objects.filter(user_id=self.object.user_id)
        self.object.delete()
        user.delete()
        current_result.delete()

        return HttpResponseRedirect(success_url)


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm


class LogoutView(views.RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):

        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)

