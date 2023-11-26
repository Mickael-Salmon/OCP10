from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from projects.models import Project, Issue, Comment


# class ProjectPermissions(permissions.BasePermission):
#     """
#     Custom permissions for accessing and modifying projects.

#     - For safe methods (e.g., GET), the user must be a contributor of the project.
#     - For other methods (e.g., POST, PUT, DELETE), the user must be the author of the project.
#     """

#     def has_permission(self, request, view):
#         """
#         Check if the user has permission to perform the requested action on the project.

#         Args:
#             request (HttpRequest): The request object.
#             view (View): The view object.

#         Returns:
#             bool: True if the user has permission, False otherwise.
#         """
#         project_pk = view.kwargs.get("pk")
#         if project_pk is None:
#             return False  # Prevent access if project_pk is not provided

#         try:
#             project = Project.objects.get(id=project_pk)
#         except Project.DoesNotExist:
#             return False

#         try:
#             # project = get_object_or_404(Project, id=view.kwargs["project_pk"])
#             # project = get_object_or_404(Project, id=view.kwargs["pk"])
#             project = Project.objects.get(id=project_pk)
#             if request.method in permissions.SAFE_METHODS:
#                 return project in Project.objects.filter(
#                     contributors__user=request.user
#                 )
#             return request.user == project.author
#         except KeyError:
#             return True

class ProjectPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs.get("pk")
        if project_pk is None:
            return False

        project = get_object_or_404(Project, id=project_pk)
        is_contributor = project.contributors.filter(id=request.user.id).exists()
        is_author = project.author == request.user

        if request.method in permissions.SAFE_METHODS:
            return is_contributor or is_author

        return is_author  # Pour les méthodes non-sûres (PUT, DELETE), l'utilisateur doit être l'auteur

class ContributorPermissions(permissions.BasePermission):
    """
    Custom permissions for accessing and modifying contributors of a project.

    - For safe methods (e.g., GET), the user must be a contributor of the project.
    - For other methods, the user must be the author of the project.
    """

    # def has_permission(self, request, view):
    #     """
    #     Check if the user has permission to perform the requested action on the project.

    #     Args:
    #         request (HttpRequest): The request object.
    #         view (APIView): The view object.

    #     Returns:
    #         bool: True if the user has permission, False otherwise.
    #     """
    #     project = get_object_or_404(Project, id=view.kwargs["pk"])
    #     if request.method in permissions.SAFE_METHODS:
    #         return project in Project.objects.filter(contributors=request.user)
    #     return request.user == project.author
    def has_permission(self, request, view):
        project_pk = view.kwargs.get("project_pk") or view.kwargs.get("pk")
        user_pk = view.kwargs.get("user_pk")

        project = get_object_or_404(Project, id=project_pk)
        is_contributor = project.contributors.filter(id=request.user.id).exists()
        is_author = project.author == request.user

        if request.method in permissions.SAFE_METHODS:
            return is_contributor or is_author

        if request.method == 'DELETE' and user_pk:
            # Pour la suppression, vérifie si l'utilisateur est l'auteur du projet
            return is_author

        return is_author  # Pour les méthodes non-sûres autres que DELETE

class IssuePermissions(permissions.BasePermission):
    """
    Custom permissions for accessing and modifying issues of a project.

    - For safe methods (e.g., GET), the user must be a contributor or the author of the project.
    - For POST, the user must be a contributor or the author of the project.
    - For PUT and DELETE, the user must be the author of the issue.
    """

    def has_permission(self, request, view):
        # Récupérer l'identifiant du projet depuis l'URL
        project_pk = view.kwargs.get("project_pk")

        # Récupérer le projet ou renvoyer une erreur 404 si non trouvé
        project = get_object_or_404(Project, id=project_pk)

        # Vérifier si l'utilisateur est un contributeur ou l'auteur du projet
        is_contributor_or_author = project.contributors.filter(id=request.user.id).exists() or project.author == request.user

        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return is_contributor_or_author

        if request.method in ['PUT', 'DELETE']:
            issue_pk = view.kwargs.get("issue_pk")
            if issue_pk:
                issue = get_object_or_404(Issue, id=issue_pk)
                return request.user == issue.author

        return False



class CommentPermissions(permissions.BasePermission):
    """
    Custom permissions for accessing and modifying comments of an issue.

    - If the comment ID is provided:
        - For safe methods, the user must be a contributor of the project.
        - For other methods, the user must be the author of the comment.
    - Otherwise, the user must be a contributor of the project.
    """

    # def has_permission(self, request, view):
    #     """
    #     Check if the user has permission to perform the requested action.

    #     Args:
    #         request (HttpRequest): The request object.
    #         view (APIView): The view object.

    #     Returns:
    #         bool: True if the user has permission, False otherwise.
    #     """
    #     project = get_object_or_404(Project, id=view.kwargs["pk"])

    #     try:
    #         comment = get_object_or_404(Comment, id=view.kwargs["comment_pk"])
    #         if request.method in permissions.SAFE_METHODS:
    #             return project in Project.objects.filter(
    #                 contributors__user=request.user
    #             )
    #         return request.user == comment.author
    #     except KeyError:
    #         return project in Project.objects.filter(contributors__user=request.user)
    # def has_permission(self, request, view):
    #     # Gérer la requête POST différemment car il n'y a pas d'ID de commentaire
    #     if request.method == 'POST':
    #         project_pk = view.kwargs.get("project_pk")
    #         project = get_object_or_404(Project, id=project_pk)
    #         return project.contributors.filter(id=request.user.id).exists() or project.author == request.user

    #     # Logique pour les autres méthodes (GET, PUT, DELETE)
    #     comment_pk = view.kwargs.get("comment_pk")
    #     if comment_pk:
    #         comment = get_object_or_404(Comment, id=comment_pk)
    #         return request.user == comment.author or request.user == comment.issue.project.author

    #     return False
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        issue_pk = view.kwargs.get('issue_pk')

        if not project_pk or not issue_pk:
            return False

        try:
            project = Project.objects.get(pk=project_pk)
            Issue.objects.get(pk=issue_pk, project=project)  # Vérifier que l'issue appartient bien au projet
        except (Project.DoesNotExist, Issue.DoesNotExist):
            return False

        is_contributor = project.contributors.filter(id=request.user.id).exists()
        is_author = project.author == request.user

        return is_contributor or is_author