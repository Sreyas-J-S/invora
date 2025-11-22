from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='invoice/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='invoice/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='invoice/password_change_done.html'), name='password_change_done'),
    path('accounts/profile/', views.edit_profile, name='edit_profile'),
    path('', views.create_invoice, name='home'),

    path('create_product/', views.create_product, name='create_product'),
    path('view_product/', views.view_product, name='view_product'),
    path('edit_product/<int:pk>', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    # path('upload_product_excel', views.upload_product_from_excel,
    #      name='upload_product_excel'),
    # path('create_customer/', views.create_customer, name='create_customer'),
    # path('view_customer/', views.view_customer, name='view_customer'),
    # path('edit_customer/<int:pk>', views.edit_customer, name='edit_customer'),
    # path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),

    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    # path('delete_all_invoice/', views.delete_all_invoice,
    #      name='delete_all_invoice'),
    # path('download_all_invoice/', views.download_all,
    #      name='download_all_invoice'),
    path('download_all_invoice/', views.download_all, name='download_all_invoice'),
    path('view_invoice_detail/<int:pk>/',
         views.view_invoice_detail, name='view_invoice_detail'),
    path('monthly_profit/', views.monthly_profit, name='monthly_profit'),
]
