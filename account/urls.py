from django.contrib.auth.views import LoginView 
from django.urls import path


from .views import create_token
from .forms import LoginForm

app_name = 'account'


urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html', form_class=LoginForm), name='login'),
    path('create_token/', create_token , name =  "api_token" )
]
