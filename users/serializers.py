from rest_framework import serializers
from .models import UserAccount,Profile
from questions.serializers import QuestionSerializer




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('email','username','password','id')
        extra_kwargs = {
            'username':{'min_length':3},
            'password':{'write_only':True,'min_length':5,'style':{'input_type':'password'}}
        }



    def create(self,validate_data):
        return UserAccount.objects.create_user(**validate_data)   




