from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'questions',views.QuestionsViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('questions/<slug:slug>/answer/',views.AnswerCreateAPIView.as_view()),
    path('questions/<slug:slug>/answers/',views.AnswerListAPIView.as_view()),
    path('questions/<slug:slug>/like/',views.QuestionLikeAPIView.as_view()),
    path('questions/<slug:slug>/answers/<int:pk>/',views.AnswerRUDAPIView.as_view()),
    path('questions/<slug:slug>/answers/<int:pk>/like/',views.AnswerLikeAPIView.as_view()),
    path('questions/<slug:slug>/answers/<int:pk>/reply/',views.ReplyCreateAPIView.as_view()),

    #path('<slug:username>/',views.QuestionUser.as_view()),
    
    
]