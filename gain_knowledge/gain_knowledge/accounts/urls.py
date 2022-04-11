from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from gain_knowledge.accounts.views import UserLoginView, UserRegisterView, ProfileDetailsView, EditProfileView, \
    DeleteProfileView, ChangeUserPasswordView, LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('eidt/<int:pk>', EditProfileView.as_view(), name='profile edit'),
    path('delete/<int:pk>', DeleteProfileView.as_view(), name='profile delete'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('list categories')), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout user'),
]