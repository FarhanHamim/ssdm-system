from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/create/', views.profile_create_view, name='profile_create'),
    path('profile/edit/<int:pk>/', views.profile_edit_view, name='profile_edit'),
    path('profile/delete/<int:pk>/', views.profile_delete_view, name='profile_delete'),
    path('profile/<int:pk>/', views.profile_detail_view, name='profile_detail'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read_view, name='mark_notification_read'),
    path('notifications/count/', views.get_notification_count_view, name='get_notification_count'),
    path('notifications/list/', views.get_notifications_list_view, name='get_notifications_list'),
    path('update-dependent-forms/', views.update_dependent_forms, name='update_dependent_forms'),
    path('reports/', views.report_generation_view, name='report_generation'),
    path('reports/export-pdf/', views.export_pdf_view, name='export_pdf'),
    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password_confirm_view, name='reset_password_confirm'),
]
