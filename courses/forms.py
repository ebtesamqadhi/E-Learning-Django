from django import forms
from .models import Courses, Text, Video, File, Image , Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['subject', 'title', 'overview', 'status', 'photo']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['text']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']