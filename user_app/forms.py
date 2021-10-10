from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from user_app import models
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name', 
            'email':'Email Address', 
            'username':'Username', 
            'password1':'Password', 
            'password2':'Password confirmation'
        }
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
            })
            
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Registered")
        elif email == "":
            raise forms.ValidationError("Email Address is Required")
        
        return email


class ProfileForm(ModelForm):
    
    class Meta:
        model = models.Profile
        fields = ['name', 'email', 'short_intro', 'bio', 'location', 'profile_picture', 'social_codeforces', 'social_github', 'social_linkedin', 'social_facebook']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
            })

class SkillForm(ModelForm):
    
    class Meta:
        model = models.Skill
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
            })




###################################################################
# login registration form template
###################################################################
# <form action="{% if register %}{% url 'register' %}{% else %}{% url 'login' %}{% endif %}" method="POST" class="form auth__form">
#     {% csrf_token %}
#     <!-- Input:Text -->
#     {% if register %}
#     <div class="form__field">
#         <label for="formInput#text">Name</label>
#         <input class="input input--text" id="formInput#text" type="text" name="name" placeholder="e.g. Dennis Ivanov" />
#     </div>
#     {% endif %}

#     <!-- Input:Email -->
#     {% if register %}
#     <div class="form__field">
#         <label for="formInput#email">Email Address</label>
#         <input class="input input--email" id="formInput#email" type="email" name="email" placeholder="e.g. user@domain.com" />
#     </div>
#     {% endif %}

#     <!-- Input:Username -->
#     <div class="form__field">
#         <label for="formInput#text">Username</label>
#         <input class="input input--text" id="formInput#text" type="text" name="username" placeholder="Enter your username..." />
#     </div>

#     <!-- Input:Password -->
#     <div class="form__field">
#         <label for="formInput#password">Password: </label>
#         <input class="input input--password" id="formInput#passowrd" type="password" name="password" placeholder="••••••••" />
#     </div>

#     {% if register %}
#     <!-- Input:Password -->
#     <div class="form__field">
#         <label for="formInput#confirm-password">Password confirmation</label>
#         <input class="input input--password" id="formInput#confirm-passowrd" type="password" name="confirm-password" placeholder="••••••••" />
#     </div>
#     {% endif %}

#     <div class="auth__actions">
#         <input class="btn btn--sub btn--lg" type="submit" value="{% if register %}Sign Up{% else %}Log In{% endif %}" />
#         {% if not register %}
#         <a href="#">Forget Password?</a>
#         {% endif %}
#     </div>
# </form>
###################################################################



