from rest_framework import serializers
from .models import Question,Answer,qlike,alike,Reply


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    answer_likes = serializers.SerializerMethodField()
    number_of_replies = serializers.SerializerMethodField()
    like_by_req_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Answer
        exclude = ('updated_at','question',)

    def get_answer_likes(self,instance):
        return instance.likers.count()    

    def get_number_of_replies(self,instance):
        return instance.replies.count()

    def get_like_by_req_user(self,instance):
        request = self.context['request']
        return instance.likers.filter(liker_id=request.user.id).exists() 



class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    number_of_likes = serializers.SerializerMethodField()
    number_of_answers = serializers.SerializerMethodField()
    like_by_req_user = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()
   
    class Meta:
        model = Question
        exclude = ('updated_at',)
        lookup_field = 'slug'
        
       

    
    def get_number_of_answers(self,instance):
        return instance.answers.count()  
        

    def get_number_of_likes(self,instance):
        '''return qlike.objects.filter(question=instance).count()'''
        return instance.likes.count()

    def get_like_by_req_user(self,instance):
        request = self.context['request']
        return instance.likes.filter(liker_id=request.user.id).exists()
        

    def get_user_has_answered(self,instance):
        request = self.context['request']

        return instance.answers.filter(
            author=request.user
        ).exists()

        # return Answer.objects.filter(
        #     question=instance,author=request.user
        # ).exists()
    
        


class QuestionLikeSerializer(serializers.ModelSerializer):
    liker = serializers.StringRelatedField(read_only=True)
    class Meta:
       model = qlike
       exclude = ('question',) 


class AnswerLikeSerializer(serializers.ModelSerializer):
    liker = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = alike
        exclude = ('answer',)

class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reply
        exclude = ('answer',)




