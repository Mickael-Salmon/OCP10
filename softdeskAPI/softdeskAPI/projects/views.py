from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.models import Project, Contributor, Issue, Comment
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


# class ProjectList(generics.ListCreateAPIView):
#     """API endpoint to list all projects or create a new project."""
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated]


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
                QuerySet: A queryset containing projects where the current user is a contributor.
            """
            return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically sets the author of the project to the current user.

        Args:
            serializer: The serializer instance used for creating the project.

        Returns:
            None
        """
        serializer.save(author=self.request.user)


# class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
#     """API endpoint to retrieve, update, or delete a specific project."""
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [ProjectPermissions]


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
        """
        Return a queryset that includes only the projects where the current user is a contributor.

        Returns:
            QuerySet: The queryset of projects where the current user is a contributor.
        """
        # Fixed error : django.core.exceptions.FieldError: Unsupported lookup 'user' for ForeignKey or join on the field not permitted.
        # return Project.objects.filter(contributors__user=self.request.user)
        return Project.objects.filter(contributors=self.request.user)


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
        return Contributor.objects.filter(project__id=self.kwargs["pk"])


# class ContributorDetail(generics.RetrieveUpdateDestroyAPIView):
#     """API endpoint to retrieve, update, or delete a contributor of a specific project."""
#     queryset = Contributor.objects.all()
#     serializer_class = ContributorSerializer
#     permission_classes = [ContributorPermissions]
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

    def get_queryset(self):
        """
        Return a queryset that includes only the contributors of the specific project.

        Returns:
            QuerySet: A queryset containing the contributors of the specific project.
        """
        return Contributor.objects.filter(project__id=self.kwargs["pk"])


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
        return Issue.objects.filter(project__id=self.kwargs["pk"])


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete an issue of a specific project.

    Attributes:
        serializer_class (class): The serializer class for the issue.
        permission_classes (list): The permission classes for the issue.

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
        return Issue.objects.filter(project__id=self.kwargs["pk"])


class CommentList(generics.ListCreateAPIView):
    """
    API endpoint to list all comments of an issue or add a new comment to an issue.
    """

    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
            """
            Return a queryset that includes only the comments of the specific issue.

            Returns:
                QuerySet: A queryset containing the comments of the specific issue.
            """
            return Comment.objects.filter(issue__id=self.kwargs["issue_pk"])


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a comment of a specific issue.

    Attributes:
        serializer_class (CommentSerializer): The serializer class for comment objects.
        permission_classes (list): The list of permission classes for comment operations.

    Methods:
        get_queryset(): Return a queryset that includes only the comments of the specific issue.
    """
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        """
        Return a queryset that includes only the comments of the specific issue.

        Returns:
            QuerySet: A queryset containing comments related to the specific issue.
        """
        return Comment.objects.filter(issue__id=self.kwargs["issue_pk"])
