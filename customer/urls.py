from django.urls import path
from .views import SignupCustomerView,  LoginCustomerJWTView

urlpatterns = [
    path('signup/', SignupCustomerView.as_view(), name='signup'),
    # path('login/', LoginCustomerView.as_view(), name='login'),  # For Token-based login
    path('login-jwt/', LoginCustomerJWTView.as_view(), name='login-jwt'),  # Uncomment if using JWT
]