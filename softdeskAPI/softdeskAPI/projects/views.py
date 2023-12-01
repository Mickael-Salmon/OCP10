from django.shortcuts import render
from rest_framework import serializers
from django.db.models import Q
# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.models import Project, Contributor, Issue, Comment
from django.shortcuts import get_object_or_404
from django.http import Http404
from projects.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
    ProjectDetailSerializer,
    CommentDetailSerializer,
)
from projects.permissions import (
    ProjectPermissions,
    ContributorPermissions,
    IssuePermissions,
    CommentPermissions,
)
from django.contrib.auth.models import User

class ProjectList(generics.ListCreateAPIView):
    """
    API endpoint to list all projects or create a new project.

    Attributes:
        serializer_class (class): The serializer class for the project model.
        permission_classes (list): The list of permission classes for the view.
    """

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all().order_by('id')
        """
        Returns:
            QuerySet: A queryset containing projects where the current user is either a contributor or the author.
        """
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) |
            Q(contributors=user)
        )

    def perform_create(self, serializer):
        """
        Automatically sets the author of the project to the current user.

        Args:
            serializer: The serializer instance used for creating the project.

        Returns:
            None
        """
        serializer.save(author=self.request.user)



class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific project.

    Attributes:
        serializer_class (Serializer): The serializer class for the project model.
        permission_classes (list): The list of permission classes for the view.
    """

    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]

    def get_queryset(self):
        # Récupère l'ID du projet à partir de l'URL
        # project_id = self.kwargs.get('project_pk')
        # project_pk = self.kwargs.get('project_pk')
        # # Assure-toi que la requête retourne un seul projet correspondant à l'ID
        # return Project.objects.filter(id=project_id)
        project_pk = self.kwargs.get('pk')
        return Project.objects.filter(id=project_pk)


class ContributorList(generics.ListCreateAPIView):
    """
    API endpoint to list all contributors of a project or add a new contributor to a project.

    Attributes:
        serializer_class (Serializer): The serializer class for the Contributor model.
        permission_classes (list): The list of permission classes for the view.

    Methods:
        get_queryset(): Return a queryset that includes only the contributors of the specific project.
    """

    serializer_class = ContributorSerializer
    permission_classes = [ContributorPermissions]

    def get_queryset(self):
        """
        Return a queryset that includes only the contributors of the specific project.

        Returns:
            QuerySet: A queryset containing the contributors of the specific project.
        """
        return Contributor.objects.filter(project__id=self.kwargs["project_pk"]).order_by('id')

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])


class ContributorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a contributor of a specific project.

    Attributes:
        serializer_class (ContributorSerializer): The serializer class for the contributor model.
        permission_classes (list): The list of permission classes for the view.

    Methods:
        get_queryset(): Return a queryset that includes only the contributors of the specific project.
    """
    serializer_class = ContributorSerializer
    permission_classes = [ContributorPermissions]

    def get_object(self):
        # Utilise 'user_pk' et 'project_pk' pour obtenir l'objet Contributor spécifique
        project_pk = self.kwargs.get('project_pk')
        user_pk = self.kwargs.get('user_pk')
        return get_object_or_404(Contributor, project__id=project_pk, user__id=user_pk)

    def get_queryset(self):
        project_pk = self.kwargs.get("project_pk") or self.kwargs.get("pk")
        user_pk = self.kwargs.get("user_pk")

        if user_pk:
            # Gérer la suppression d'un contributeur spécifique
            return Contributor.objects.filter(project__id=project_pk, user__id=user_pk)
        else:
            # Gérer la liste / l'ajout de contributeurs
            return Contributor.objects.filter(project__id=project_pk)

    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()
        if contributor.role == "AUTHOR":
            return Response({"detail": "Project author cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        # Si l'utilisateur n'est pas l'auteur, procéder à la suppression
        return super().destroy(request, *args, **kwargs)


class IssueList(generics.ListCreateAPIView):
    """
    API endpoint to list all issues of a project or create a new issue for a project.

    Attributes:
        serializer_class (class): The serializer class for the Issue model.
        permission_classes (list): The list of permission classes for the view.

    Methods:
        get_queryset(): Return a queryset that includes only the issues of the specific project.
    """

    serializer_class = IssueSerializer
    permission_classes = [IssuePermissions]

    def get_queryset(self):
        """
        Return a queryset that includes only the issues of the specific project.

        Returns:
            QuerySet: A queryset containing the issues of the specific project.
        """
        return Issue.objects.filter(project__id=self.kwargs["project_pk"]).order_by('id')

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific issue of a specific project.

    Attributes:
        serializer_class (IssueSerializer): The serializer class for the issue model.
        permission_classes (list): The list of permission classes for the view.

    Methods:
        get_object(): Return the specific issue of the specific project.
    """
    serializer_class = IssueSerializer
    permission_classes = [IssuePermissions]

    def get_object(self):
        # Utilise 'project_pk' et 'issue_pk' pour obtenir l'objet Issue spécifique
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        return get_object_or_404(Issue, project__id=project_pk, id=issue_pk).order_by('id')

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = self.get_serializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        issue_pk = self.kwargs.get("issue_pk")
        project_pk = self.kwargs.get("project_pk")
        return Comment.objects.filter(issue__id=issue_pk, issue__project__id=project_pk).order_by('id')

    def perform_create(self, serializer):
        issue_pk = self.kwargs.get("issue_pk")
        issue = get_object_or_404(Issue, pk=issue_pk)
        serializer.save(author=self.request.user, issue=issue)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a comment of a specific issue.

    Attributes:
        serializer_class (CommentSerializer): The serializer class for comment objects.
        permission_classes (list): The list of permission classes for comment operations.

    Methods:
        get_queryset(): Return a queryset that includes only the comments of the specific issue.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        """
        Return a queryset that includes only the comments of the specific issue.

        Returns:
            QuerySet: A queryset containing comments related to the specific issue.
        """
        return Comment.objects.filter(issue__id=self.kwargs["issue_pk"]).order_by('id')

    def get_object(self):
        comment_id = self.kwargs.get('comment_pk')
        try:
            return Comment.objects.get(pk=comment_id, issue__id=self.kwargs.get('issue_pk'))
        except Comment.DoesNotExist:
            raise Http404
