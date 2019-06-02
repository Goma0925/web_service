import os
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from applications.users.models import User, UserProfile
import datetime
from PIL import Image
from applications.users import views_support_scripts
from django.conf import settings

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
    birthday = forms.DateField(widget=forms.HiddenInput())
    class Meta():
        model = UserProfile
        fields = ("first_name", "last_name", "middle_name", 'birthday', 'where_you_live', 'introduction',)
        widgets = {
            "introduction": forms.Textarea(),
        }

    # def save(self, commit=True):
    #     new_profile = super(ProfileForm, self).save(commit=False)
    #     old_profile = UserProfile.objects.filter(id=new_profile.id)
    #     # print("Saving profile of", user)
    #     # print("The user's profile =", user.profile)
    #     # print([f.name for f in user._meta.get_fields()])
    #     new_profile_fields = [f for f in new_profile._meta.get_fields()]
    #     print("FIELDS of user profile")
    #     for new_profile_field in new_profile_fields:
    #          = profile._meta.get_field(field_name)
    #         print(field_name + ": " + str(field_object.value_from_object(profile)))
    #     if commit == True:
    #         UserProfile.objects.filter(id=profile.id)
    #         print("Profile saved")
    #     return profile

class ProfileImageForm(forms.Form):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    image = forms.ImageField()
    def save_image_of(self, user):
        img_format = ".jpg"
        stored_time = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        print("time format:", stored_time)

        image_x = self.cleaned_data.get('x')
        image_y = self.cleaned_data.get('y')
        image_width = self.cleaned_data.get('width')
        image_height = self.cleaned_data.get('height')
        #print("Coordinates:", image_x, image_y, image_width, image_height)
        # Resize the image and store it in media dir.
        image = Image.open(self.cleaned_data.get('image')).convert('RGB')
        cropped_image = image.crop((image_x, image_y, image_width + image_x, image_height + image_y))
        resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)
        file_name = "profileImg_" + str(user.id) + "_" + stored_time + img_format
        image_storage_path = os.path.join(settings.MEDIA_ROOT, settings.PROFILE_IMAGE_DIR, file_name)
        print("image_storage_path", image_storage_path)
        image_storage_url = settings.MEDIA_URL + settings.PROFILE_IMAGE_URL.lstrip("/") + file_name + "/"
        print("Profile storage", settings.PROFILE_IMAGE_URL, "|", image_storage_url)
        try:
            resized_image.save(image_storage_path, format="JPEG")  # Image.save() saves the image in a file at the given path(event.image.path)
        except Exception as e:
            #print("Image failed to be saved:", e)
            raise forms.ValidationError("Error occured when saving the image")
        return str(image_storage_url)
