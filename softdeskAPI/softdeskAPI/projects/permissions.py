from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from projects.models import Project, Issue, Comment

class ProjectPermissions(permissions.BasePermission):
    """Custom permissions for accessing and modifying projects.

    - For safe methods (e.g., GET), the user must be a contributor of the project.
    - For other methods (e.g., POST, PUT, DELETE), the user must be the author of the project.
    """
    def has_permission(self, request, view):
        try:
            project = get_object_or_404(Project, id=view.kwargs['project_pk'])
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(contributors__user=request.user)
            return request.user == project.author
        except KeyError:
            return True

class ContributorPermissions(permissions.BasePermission):
    """Custom permissions for accessing and modifying contributors of a project.

    - For safe methods (e.g., GET), the user must be a contributor of the project.
    - For other methods, the user must be the author of the project.
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        if request.method in permissions.SAFE_METHODS:
            return project in Project.objects.filter(contributors__user=request.user)
        return request.user == project.author

class IssuePermissions(permissions.BasePermission):
    """Custom permissions for accessing and modifying issues of a project.

    - If the issue ID is provided, the user must be the author of the issue.
    - Otherwise, the user must be a contributor of the project.
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        try:
            issue = get_object_or_404(Issue, id=view.kwargs['issue_pk'])
            return request.user == issue.author
        except KeyError:
            return project in Project.objects.filter(contributors__user=request.user)


class CommentPermissions(permissions.BasePermission):
    """Custom permissions for accessing and modifying comments of an issue.

    - If the comment ID is provided:
    - For safe methods, the user must be a contributor of the project.
    - For other methods, the user must be the author of the comment.
    - Otherwise, the user must be a contributor of the project.
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        try:
            comment = get_object_or_404(Comment, id=view.kwargs['comment_pk'])
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(contributors__user=request.user)
            return request.user == comment.author
        except KeyError:
            return project in Project.objects.filter(contributors__user=request.user)




