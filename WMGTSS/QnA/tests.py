from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, Profile, Tutor, Student, Board, Question, Answer, Like
# Create your tests here.

class BasicTest(TestCase):
    def test_course_model(self):
        course = Course()
        course.name = "WM393"
        course.save()

        record = Course.objects.get(pk=1)
        self.assertEqual(record, course)