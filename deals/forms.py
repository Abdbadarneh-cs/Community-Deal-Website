from django import forms
from .models import User, Deal
from django.contrib.auth.hashers import make_password

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', 'phone', 'bio', 'interests']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields =['title', 'description', 'category', 'expiration_date', 'document', 'image']
        widgets ={ 'expiration_date': forms.DateInput(attrs={'type': 'date'}), }
    



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'phone', 'bio', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={'rows':3}),
            'interests': forms.TextInput(attrs={'placeholder': 'E.g. Programming, Technology, Marketing'}),
            'phone': forms.TextInput(attrs={'placeholder': '+972 '}),
        }


    





