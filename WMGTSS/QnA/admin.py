from django.contrib import admin

# Register your models here.

from .models import Question, Profile, Course, Student, Tutor, Answer, Board, Like

class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # automatically fill the slug slot with the board name

# register the models with the admin site
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Answer)
admin.site.register(Board)
admin.site.register(Like)