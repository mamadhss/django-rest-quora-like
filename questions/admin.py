from django.contrib import admin

# Register your models here.
from .models import Question,qlike,alike,Answer,Reply


admin.site.register(Question)
admin.site.register(qlike)
admin.site.register(alike)
admin.site.register(Answer)
admin.site.register(Reply)