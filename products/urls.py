from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('stores/', views.stores_list_view, name='stores'),
    path('stores/<int:store_id>/', views.store_detail_view, name='store_detail'),
    path('stores/create/', views.create_store_view, name='create_store'),
    path('stores/<int:store_id>/add-product/', views.add_product_view, name='add_product'),
]
