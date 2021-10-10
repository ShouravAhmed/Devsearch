
from .models import Project, Tag
from django.db.models import Q
from user_app.models import Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_project(request):
    search_text = ''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
        
    projects = Project.objects.distinct().order_by('created_at').filter(
            owner__in = Profile.objects.filter(is_verified=True)
        ).filter(
            Q(title__icontains = search_text) |
            Q(owner__in = Profile.objects.filter(Q(name__icontains=search_text) | Q(username__icontains=search_text))) |
            Q(tags__in = Tag.objects.filter(name__icontains=search_text)) 
        )

    return projects, search_text

def paginate_project(request, project_list, project_per_page, pagination_preview):

    paginator = Paginator(project_list, project_per_page)
    page_no = request.GET.get('page')
    
    try:
        current_page_project_list = paginator.page(page_no)
    except PageNotAnInteger:
        page_no = 1
        current_page_project_list = paginator.page(1)
    except EmptyPage:
        page_no = paginator.num_pages
        current_page_project_list = paginator.page(paginator.num_pages)
    except:
        page_no = 1
        current_page_project_list = paginator.page(1)

    page_no = int(page_no)
    start_page = max(page_no - pagination_preview, 1)
    end_page = min(page_no + pagination_preview, paginator.num_pages) + 1

    if page_no <= pagination_preview:
        end_page = min(end_page + pagination_preview - page_no + 1, paginator.num_pages + 1)

    if page_no > paginator.num_pages - pagination_preview:
        start_page = max(start_page - (pagination_preview - (paginator.num_pages - page_no + 1) + 1), 1)

    custom_pagination_range = range(start_page, end_page)

    return current_page_project_list, custom_pagination_range

