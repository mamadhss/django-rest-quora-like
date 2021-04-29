from rest_framework import status,viewsets,permissions,generics
from rest_framework.views import APIView
from .serializers import QuestionSerializer,AnswerSerializer,QuestionLikeSerializer,AnswerLikeSerializer,ReplySerializer
from .models import Question,Answer,qlike,alike,Reply
from .permissions import IsOwnerOrReadonly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from .task import question_created,question_answered,question_liked
from decouple import config
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)


CACHE_TTL = int(config("CACHE_TTL"))

class QuestionsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadonly]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-created_at')
    lookup_field = 'slug'

    def perform_create(self,serializer):
        question = serializer.save(author=self.request.user)
        question_created.delay(question.id)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)    


class AnswerCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self,serializer):
        question = Question.objects.get(slug=self.kwargs['slug'])


        if question.answers.filter(author=self.request.user).exists():

            raise ValidationError('you already answered this question')
  
        answer = serializer.save(
            author=self.request.user,
            question = question
        ) 
        question_answered.delay(answer.id)

class AnswerListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


    def get_queryset(self):
        return self.queryset.filter(question__slug=self.kwargs['slug'])   
        
    #     '''question = Question.objects.get(slug = self.kwargs['slug'])
    #     return question.answers.all()'''
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadonly]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()   

    def get_queryset(self):
        return self.queryset.filter(question__slug=self.kwargs['slug'])

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request,*args,**kwargs)
           


class QuestionLikeAPIView(APIView):
    serializer_class = QuestionLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = qlike.objects.all()

    def post(self,request,slug):
        question = Question.objects.get(slug=slug)
        serializer = QuestionLikeSerializer(data=request.data)
        if self.queryset.filter(question=question,liker=self.request.user).exists():
            raise ValidationError('already voted')
        if serializer.is_valid():

            q_like = serializer.save(
                question=question,
                liker=self.request.user

            )
            question_liked.delay(q_like.id)
            

            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

    def delete(self,request,slug):
        question = Question.objects.get(slug=slug)
        qs = question.likes.filter(
            liker=self.request.user
        )

        qs.delete()
        return Response({'msg':'suucessfully unliked'},status=status.HTTP_204_NO_CONTENT)

        
class AnswerLikeAPIView(APIView):
    serializer_class = AnswerLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = alike.objects.all()

    def post(self,request,slug,pk):
        answer = Answer.objects.get(question__slug=slug,pk=pk)
        serializer = AnswerLikeSerializer(data=request.data)
        if answer.likers.filter(liker=self.request.user).exists():
            raise ValidationError('already liked')
        if serializer.is_valid():
            serializer.save(
                answer=answer,
                liker=self.request.user
            )

            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    def delete(self,request,slug,pk):
        answer = Answer.objects.get(question__slug=slug,pk=pk)
        qs = answer.likers.filter(
            liker = self.request.user
            
        )    

        qs.delete()

        return Response({'msg':'unliked!'},status=status.HTTP_204_NO_CONTENT)


# class QuestionUser(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = QuestionSerializer
#     queryset = Question.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(author__username=self.kwargs['username'])




class ReplyCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()

    def perform_create(self,serializer):
        answer = Answer.objects.get(question__slug=self.kwargs['slug'],pk=self.kwargs['pk'])

        qs = self.queryset.filter(answer=answer,author=self.request.user.is_staff)
        if not qs:
            raise ValidationError('just question owners can reply a question !')

        
        serializer.save(
            author = self.request.user,
            answer = answer
        )








