from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.home, name="login"),
    path('create/', views.create, name="create"),
    path('add_subuser/', views.add_subuser, name="add_subuser"),
    path('get_subuser/', views.get_subuser, name="get_subuser"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('reset_token/', views.reset_token, name="reset_token"),
    path('test_token/', views.test_token, name="test_token"),
    # path('reset_password/',
    #      auth_views.PasswordResetView.as_view(
    #          template_name="reset_password/password_reset.html"),
    #      name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
    #     template_name="reset_password/password_reset_sent.html"), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name="reset_password/password_reset_form.html"), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name="reset_password/password_reset_done.html"), name="password_reset_complete"),
]
