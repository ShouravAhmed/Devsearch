from django.shortcuts import render, redirect
from django.http import HttpResponse

from projects.models import Project, Review, Tag
from projects.forms import ProjectForm, ReviewForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import search_project, paginate_project



def projects(request):
    project_list, search_text = search_project(request)

    project_per_page = 6
    pagination_preview = 3
    current_page_project_list, custom_pagination_range = paginate_project(request, project_list, project_per_page, pagination_preview)

    context = {
        'project_list': current_page_project_list, 
        'custom_pagination_range': custom_pagination_range, 
        'search_text':search_text
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    
    review_list = Review.objects.filter(project=project)

    if request.user.is_authenticated:
        already_reviewed = Review.objects.filter(project=project, owner=request.user.profile).exists()
    else :
        already_reviewed = False
    
    form = ReviewForm()
        
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            review = form.instance
            review.project = project
            review.owner = request.user.profile
            review.save()

            if review.value == 'up':
                project.up_vote += 1
            else:
                project.down_vote += 1
            project.save()

            try:
                project.positive_review = int((project.up_vote * 100) / (project.up_vote + project.down_vote))
                project.save()
            except :
                pass

            messages.success(request, "Your Review Added Successfully")
            return redirect('project', project.id)

    context = {
        'project':project, 
        'form':form,
        'review_list':review_list,
        'total_review': project.up_vote + project.down_vote,
        'positive_review': project.positive_review,
    }

    if already_reviewed:
        context['already_reviewed'] = True

    return render(request, 'projects/single_project.html', context)


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        project_tags = [x.strip() for x in request.POST.get('users_tag').split(',')]

        if form.is_valid():
            form.save()

            project = form.instance
            project.owner = request.user.profile
            project.save()

            for tag in project_tags:
                if not Tag.objects.filter(name=tag).exists():
                    tag_instance = Tag.objects.create(name=tag)
                    tag_instance.save()
                    project.tags.add(tag_instance)
                    project.save()

            messages.success(request, "Congratulations, Your Project Created Successfully 🎉🎉")
            return redirect('project', project.id)

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(id=pk)

    if project.owner.id != request.user.profile.id:
        messages.error(request, "This Is Not Your Project 😜")
        return redirect('project', pk)

    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)

        project_tags = [x.strip() for x in request.POST.get('users_tag').split(',')]


        if form.is_valid():
            form.save()

            for tag in project_tags:
                if not Tag.objects.filter(name=tag).exists():
                    tag_instance = Tag.objects.create(name=tag)
                    tag_instance.save()
                    project.tags.add(tag_instance)
                    project.save()

            return redirect('project', project.id)


    context = {'form': form, 'project':project, 'update':True}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    project = Project.objects.get(id=pk)

    if project.owner.id != request.user.profile.id:
        messages.error(request, "This Is Not Your Project 😜")
        return redirect('project', pk)

    if request.method == 'POST':
        project.delete()
        return redirect('user_profile', request.user.profile.id)

    context = {'project':project}
    return render(request, 'projects/project_delete.html', context)
