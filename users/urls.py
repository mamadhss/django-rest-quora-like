
from django.urls import path
from .views import RegisterView


urlpatterns = [
    path('user/register/',RegisterView.as_view(),name='create_user')
        
]