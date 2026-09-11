from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/', views.customer_panel, name='customer_panel'),
    path('seller/', views.seller_panel, name='seller_panel'),
    path('payment/', views.payment_view, name='payment'),
     path('history/', views.order_history, name='order_history'),
]
