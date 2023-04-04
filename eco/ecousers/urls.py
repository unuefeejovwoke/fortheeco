from django.urls import path
from . import views

app_name = 'ecousers'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name="resetpassword_validate"),
    path('resetPassword/', views.resetPassword, name="resetPassword"),
    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_project/', views.userProject, name='user_project'),
    path('user_ideas/', views.userIdea, name='user_ideas'),
    
    path('problems/<slug:slug>/delete/', views.delete_problem, name='problem_delete'),
    path('projects/<slug:slug>/delete/', views.delete_project, name='project_delete'),
    
    path('change_password/', views.change_password, name='change_password'),
    path('social/signup/', views.signup_redirect,name='signup_redirect'),
]
