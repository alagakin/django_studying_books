from django.urls import path, include
from .views import HomePageView, AboutView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about')
]