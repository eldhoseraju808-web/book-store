from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.reg),
    path('login',views.log),
    path('details',views.details),
    path('edit',views.edit),
    path('delete/<int:idl>',views.delete,name='delete'),
    path('products',views.product),
    path('books',views.books),
    path('cart/<int:idn>',views.cart,name='cart'),
    path('viewcart',views.viewcart),
    path('cartdelete/<int:pid>',views.cartdelete,name='cartdelete'),
]
