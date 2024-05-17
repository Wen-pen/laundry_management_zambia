from django.urls import path
from . import views

urlpatterns = [
    path("", views.default, name="default"),
    path('dashboard/<int:page>', views.dashboard, name='dashboard'),
    path('orders/<int:quantity>', views.orders, name='orders'),
    path('accounts/signup', views.signup, name='signup'),
    path('prices', views.prices, name='prices'),
    path("rejected", views.rejected, name='rejected'),
    path('payments/<str:methods>', views.payments, name='payments'),
    path('view_items/<int:id>', views.view_items, name="view_items"),
    path('profile', views.profile_view, name='profile'),
]