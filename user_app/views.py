from django.shortcuts import render, redirect

from . import models
from . import forms
from projects.models import Project
from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import UserRegistrationForm

from .utils import search_profile, paginate_profile

def profiles(request):
    profile_list, search_text = search_profile(request)

    profile_per_page = 6
    pagination_preview = 3
    current_page_profile_list, custom_pagination_range = paginate_profile(request, profile_list, profile_per_page, pagination_preview)

    context = {
        'profile_list': current_page_profile_list, 
        'custom_pagination_range': custom_pagination_range, 
        'search_text':search_text
    }

    return render(request, 'user_app/profiles.html', context)

def user_profile(request, pk):
    profile = models.Profile.objects.get(id=pk)
    projects = Project.objects.filter(owner=pk)
    
    allskills = models.Skill.objects.filter(owner=pk)
    dskills = [x for x in models.Skill.objects.filter(owner=pk) if x.description]
    skills = [x for x in models.Skill.objects.filter(owner=pk) if not x.description]
    
    context = {'profile':profile, 'projects': projects, 'skills':skills, 'dskills':dskills, 'allskills':allskills}
    return render(request, 'user_app/user_profile.html', context)

def login_user(request):

    if request.user.is_authenticated:
        messages.error(request, 'You Are Already Loged In')
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user_data = User.objects.get(username=username)
            if not user_data.profile.is_verified:
                messages.error(request, "Please check your email and Verify your account.")
                return redirect('login')
        except:
            messages.error(request, "Username Does Not Exist.")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "✨✨ 🔥Welcome Aboard : "+ username +"🔥 ✨✨")
            return redirect('profiles')
        else:
            messages.error(request, "Username or Password is Incorrect")

    context = {}
    return render(request, 'user_app/login_register.html', context)

@login_required(login_url='login')
def logout_user(request):
    username = str(request.user.profile.username)
    logout(request)
    messages.info(request, username + " : Loged Out Successfully." )
    return redirect('login')

# def register_user(request):
#     if request.user.is_authenticated:
#         messages.error(request, 'You Are Already Loged In')
#         return redirect('profiles')
    
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         username = request.POST['username'].lower()
#         password = request.POST['password']
#         confirm_password = request.POST['confirm-password']

#         # print(name, email, username, password, confirm_password)
#         try:
#             User.objects.get(username=username)
#             messages.error(request, "Username Already Exist.")
#             return redirect('register')
#         except:
#             pass
#         if password != confirm_password:
#             messages.error(request, "The two password fields didn’t match.")
#             return redirect('register')

#         user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
#         user.save()

#         messages.success(request, "🎉🎉 Registration Successful 🎉🎉")
#         return redirect('login')

#     context = {'register':True}
#     return render(request, 'user_app/login_register.html', context)


def register_user(request):
    if request.user.is_authenticated:
        messages.error(request, 'You Are Already Loged In')
        return redirect('profiles')
    
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            messages.success(request, "🎉🎉 Registration Successful 🎉🎉")
            return redirect('varify_account')

    context = {'register':True, 'form':form}
    return render(request, 'user_app/login_register.html', context)

def varify_account(request):
    context = {}
    return render(request, 'user_app/varify_account.html', context)

def varify_account_success(request, pk):
    context = {}
    try:
        profile = models.Profile.objects.get(id=pk)
        if profile:
            if profile.is_verified:
                context['verified'] = True
            else:
                profile.is_verified = True
                profile.save()
        else:
            context['not_valid'] = True
    except :
        context['not_valid'] = True
    
    return render(request, 'user_app/varify_account_success.html', context)


@login_required(login_url='login')
def update_profile(request, pk):
    profile = models.Profile.objects.get(id=pk)

    if profile.user.id != request.user.id:
        messages.error(request, "This Is Not Your Profile 😜")
        return redirect('user_profile', pk)

    form = forms.ProfileForm(instance=profile)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk)

    context = {'form': form, 'profile':profile, 'update':True}
    return render(request, 'user_app/profile_form.html', context)

@login_required(login_url='login')
def create_skill(request):
    form = forms.SkillForm()
    if request.method == 'POST':
        form = forms.SkillForm(request.POST)
        if form.is_valid():
            form.save()

            skill = form.instance
            skill.owner = request.user.profile
            skill.save()

            messages.success(request, "Skill is Created Successfully")
            return redirect('user_profile', request.user.profile.id)

    context = {'form': form}
    return render(request, 'user_app/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    skill = models.Skill.objects.get(id=pk)

    if skill.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', skill.owner.id)

    form = forms.SkillForm(instance=skill)
    if request.method == 'POST':
        form = forms.SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('user_profile', skill.owner.id)

    context = {'form': form, 'update':True}
    return render(request, 'user_app/skill_form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    skill = models.Skill.objects.get(id=pk)

    if skill.owner.user.id != request.user.id:
        messages.error(request, "This Is Not Your SKill 😜")
        return redirect('user_profile', skill.owner.id)

    if request.method == 'POST':
        skill.delete()
        return redirect('user_profile', skill.owner.id)

    context = {'skill':skill}
    return render(request, 'user_app/skill_delete.html', context)




