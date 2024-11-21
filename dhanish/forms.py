from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
   class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class': 'p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none'})
            self.fields['email'].widget.attrs.update({'class': 'p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none'})
            self.fields['password1'].widget.attrs.update({'class': 'p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none'})
            self.fields['password2'].widget.attrs.update({'class': 'p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none'})
        
        def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            
            # Add custom password validation rules here if needed
            if len(password1) < 8:
                raise forms.ValidationError("Your password must be at least 8 characters long.")
            
            # Optionally, you can add more checks, or you can skip them entirely
            return password1

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            # Optional: Check if the passwords match
            if password1 != password2:
                raise forms.ValidationError("The two password fields must match.")
            
            return password2
