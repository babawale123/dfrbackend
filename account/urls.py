from django.urls import path
from .views import SignUp,Login,GetUsers,AllUsers,detailView,NewDetailView

urlpatterns = [
   path('',SignUp),
   path('login/',Login),
   path('user/',GetUsers),
   path('users/',AllUsers.as_view()),
   path('users/<int:pk>/',detailView),
   path('new/<int:pk>/',NewDetailView.as_view()),


   
]
