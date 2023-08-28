from django.urls import path
from .views import SignUp,Login,GetUsers,AllUsers

urlpatterns = [
   path('',SignUp),
   path('login/',Login),
   path('user/',GetUsers),
   path('users/',AllUsers.as_view())
]
