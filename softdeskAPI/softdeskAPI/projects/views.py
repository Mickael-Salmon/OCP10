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
    # lookup_field = 'project_pk'

    # def get_queryset(self):
    #     """
    #     Return a queryset that includes only the projects where the current user is a contributor.

    #     Returns:
    #         QuerySet: The queryset of projects where the current user is a contributor.
    #     """
    #     # Fixed error : django.core.exceptions.FieldError: Unsupported lookup 'user' for ForeignKey or join on the field not permitted.
    #     # return Project.objects.filter(contributors__user=self.request.user)
    #     # return Project.objects.filter(contributors=self.request.user)
    #     # return Project.objects.filter(id=self.kwargs['pk'], contributors=self.request.user)
    #     user = self.request.user
    #     return Project.objects.filter(
    #         Q(author=user) |
    #         Q(contributors=user)
    #     )
    # def get_queryset(self):
    #     """
    #     Return a queryset that includes only the project specified in the URL if the current user is a contributor or the author.
    #     """
    #     user = self.request.user
    #     project_pk = self.kwargs.get('pk')
    #     return Project.objects.filter(
    #         Q(id=project_pk) &
    #         (Q(author=user) | Q(contributors=user))
    #     )
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
        return Contributor.objects.filter(project__id=self.kwargs["project_pk"])

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

    # def get_queryset(self):
    #     """
    #     Return a queryset that includes only the contributors of the specific project.

    #     Returns:
    #         QuerySet: A queryset containing the contributors of the specific project.
    #     """
    #     return Contributor.objects.filter(project__id=self.kwargs["pk"])

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
        return Issue.objects.filter(project__id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IssuePermissions]

    def get_queryset(self):
        return Issue.objects.filter(project__id=self.kwargs["pk"])

    def perform_update(self, serializer):
        issue = self.get_object()
        project = issue.project

        assignee_id = serializer.validated_data.get('assignee')
        if assignee_id and not project.contributors.filter(id=assignee_id.id).exists():
            raise serializers.ValidationError("This user is not contributing to this project.")

        super().perform_update(serializer)

# class CommentList(generics.ListCreateAPIView):
#     """
#     API endpoint to list all comments of an issue or add a new comment to an issue.
#     """

#     serializer_class = CommentSerializer
#     permission_classes = [CommentPermissions]

#     def get_queryset(self):
#             """
#             Return a queryset that includes only the comments of the specific issue.

#             Returns:
#                 QuerySet: A queryset containing the comments of the specific issue.
#             """
#             return Comment.objects.filter(issue__id=self.kwargs["issue_pk"])
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        issue_pk = self.kwargs.get("issue_pk")
        project_pk = self.kwargs.get("project_pk")
        return Comment.objects.filter(issue__id=issue_pk, issue__project__id=project_pk)

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
        return Comment.objects.filter(issue__id=self.kwargs["issue_pk"])

    def get_object(self):
        comment_id = self.kwargs.get('comment_pk')
        try:
            return Comment.objects.get(pk=comment_id, issue__id=self.kwargs.get('issue_pk'))
        except Comment.DoesNotExist:
            raise Http404
