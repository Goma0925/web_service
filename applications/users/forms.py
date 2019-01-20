from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from applications.users.models import User, UserProfile
import datetime


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email has already been taken.")
        else:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("Please confirm your password.")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        return password2

    # def save(self, commit=True):
    #     self.cleaned_data["date_joined"] = datetime.datetime.now()
    #     self.cleaned_data["is_active"] = True
    #     self.cleaned_data["is_staff"] = False
    #     self.cleaned_data["is_superuser"] = False
    #     return super(CustomUserCreationForm, self).save(commit)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class ProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ("first_name", "last_name", "middle_name", 'birthday', 'where_you_live', 'introduction',
                  "profile_image_storage_url")