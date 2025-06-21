from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import UserProfile

class SignupForm(UserCreationForm):

    ROLE_CHOICES = (
        ('student','Student'),
        ('instructor','Instructor')
    )

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("هذا البريد الإلكتروني مستخدم بالفعل.")
        return email
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )

            if profile.role == 'instructor':
                instructor_group = Group.objects.get(name='Instructors')
                user.groups.add(instructor_group)
            elif profile.role == 'student':
                student_group = Group.objects.get(name='Students')
                user.groups.add(student_group)
        return user

    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'photo', 'contact_email', 'header']