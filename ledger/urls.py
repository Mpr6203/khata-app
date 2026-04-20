from django.urls import path
from . import views

urlpatterns = [

    # 🏠 Home → Customer List
    path('', views.customer_list, name='customer_list'),

    # 📊 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 👤 Customer Detail (Khata page)
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),

    path('transaction/edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
    path('transaction/delete/<int:id>/', views.delete_transaction, name='delete_transaction'),

    path('payment/edit/<int:id>/', views.edit_payment, name='edit_payment'),
    path('payment/delete/<int:id>/', views.delete_payment, name='delete_payment'),

]