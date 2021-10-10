from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects/'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'}
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    profile = request.user.profile
    data = request.data

    if not Review.objects.filter(owner=profile, project=project).exists():
        review_created = Review.objects.create(
            owner=profile,
            project=project
        )
        if 'value' in data:
            review_created.value = data['value']
        if 'body' in data:
            review_created.body = data['body']
        review_created.save()

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
