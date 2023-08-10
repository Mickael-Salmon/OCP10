from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from projects.models import Project

class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "password": "testpass"}
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        response = self.client.post('/signup/', self.user_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_valid_login(self):
        response = self.client.post('/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_invalid_login(self):
        response = self.client.post('/login/', {"username": "testuser", "password": "wrongpass"}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_protected_route_without_auth(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 401)


class ProjectTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "password": "testpass"}
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
        self.project_data = {
            "name": "Test Project",
            "description": "Description for test project",
            "type": "BACKEND"
        }

    def test_create_project(self):
        response = self.client.post('/projects/', self.project_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_projects(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)

    def test_update_project(self):
        project = Project.objects.create(**self.project_data, author=self.user)
        response = self.client.put(f'/projects/{project.id}/', {"name": "Updated Project"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Project")

    def test_delete_project(self):
        project = Project.objects.create(**self.project_data, author=self.user)
        response = self.client.delete(f'/projects/{project.id}/')
        self.assertEqual(response.status_code, 204)


class ContributorTest(TestCase):

    def setUp(self):
        # ... [Préparation similaire à la précédente]
        self.project = Project.objects.create(**self.project_data, author=self.user)
        self.contributor_data = {
            "user": self.user.id,
            "role": "DEVELOPER"
        }

    def test_add_contributor(self):
        response = self.client.post(f'/projects/{self.project.id}/contributors/', self.contributor_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_contributors(self):
        response = self.client.get(f'/projects/{self.project.id}/contributors/')
        self.assertEqual(response.status_code, 200)

    def test_delete_contributor(self):
        # Ajoutez un contributeur, puis essayez de le supprimer
        contributor = Contributor.objects.create(project=self.project, **self.contributor_data)
        response = self.client.delete(f'/projects/{self.project.id}/contributors/{contributor.id}/')
        self.assertEqual(response.status_code, 204)

class IssueTest(TestCase):

    def setUp(self):
        # ... [Préparation similaire à la précédente]
        self.project = Project.objects.create(**self.project_data, author=self.user)
        self.issue_data = {
            "title": "Test Issue",
            "description": "Description for test issue",
            "type": "BUG",
            "status": "NEW",
            "priority": "LOW"
        }

    # ... [Des tests similaires à ceux de la classe ProjectTest]

class CommentTest(TestCase):

    def setUp(self):
        # ... [Préparation similaire à la précédente]
        self.project = Project.objects.create(**self.project_data, author=self.user)
        self.issue = Issue.objects.create(project=self.project, **self.issue_data)
        self.comment_data = {
            "description": "Test comment"
        }


class ProjectAuthorizationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "password": "testpass"}
        self.user = User.objects.create_user(**self.user_data)
        self.other_user_data = {"username": "otheruser", "password": "otherpass"}
        self.other_user = User.objects.create_user(**self.other_user_data)
        self.project_data = {
            "name": "Test Project",
            "description": "Description for test project",
            "type": "BACKEND"
        }
        self.project = Project.objects.create(**self.project_data, author=self.user)

    def test_non_authenticated_user_create_project(self):
        response = self.client.post('/projects/', self.project_data, format='json')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_non_contributor_update_project(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(f'/projects/{self.project.id}/', {"name": "Updated Project"}, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_non_contributor_delete_project(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/projects/{self.project.id}/')
        self.assertEqual(response.status_code, 403)  # Forbidden

class ContributorAuthorizationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "password": "testpass"}
        self.user = User.objects.create_user(**self.user_data)
        self.other_user_data = {"username": "otheruser", "password": "otherpass"}
        self.other_user = User.objects.create_user(**self.other_user_data)
        self.project_data = {
            "name": "Test Project",
            "description": "Description for test project",
            "type": "BACKEND"
        }
        self.project = Project.objects.create(**self.project_data, author=self.user)

    def test_non_authenticated_user_add_contributor(self):
        response = self.client.post(f'/projects/{self.project.id}/contributors/', {"user": self.other_user.id, "role": "DEVELOPER"}, format='json')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_non_contributor_add_contributor(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(f'/projects/{self.project.id}/contributors/', {"user": self.other_user.id, "role": "DEVELOPER"}, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_non_contributor_delete_contributor(self):
        contributor = Contributor.objects.create(user=self.user, project=self.project, role="DEVELOPER")
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/projects/{self.project.id}/contributors/{contributor.id}/')
        self.assertEqual(response.status_code, 403)  # Forbidden


class IssueAuthorizationTest(TestCase):

    def setUp(self):
        # ... [Préparation similaire à la précédente]
        self.issue_data = {
            "title": "Test Issue",
            "description": "Description for test issue",
            "type": "BUG",
            "status": "NEW",
            "priority": "LOW"
        }

    def test_non_authenticated_user_create_issue(self):
        response = self.client.post(f'/projects/{self.project.id}/issues/', self.issue_data, format='json')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_non_contributor_create_issue(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(f'/projects/{self.project.id}/issues/', self.issue_data, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_non_contributor_update_issue(self):
        issue = Issue.objects.create(project=self.project, **self.issue_data)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(f'/projects/{self.project.id}/issues/{issue.id}/', {"title": "Updated Issue"}, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_non_contributor_delete_issue(self):
        issue = Issue.objects.create(project=self.project, **self.issue_data)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/projects/{self.project.id}/issues/{issue.id}/')
        self.assertEqual(response.status_code, 403)  # Forbidden

class CommentAuthorizationTest(TestCase):

    def setUp(self):
        # ... [Préparation similaire à la précédente]
        self.issue = Issue.objects.create(project=self.project, **self.issue_data)
        self.comment_data = {
            "description": "Test comment"
        }

    def test_non_authenticated_user_create_comment(self):
        response = self.client.post(f'/projects/{self.project.id}/issues/{self.issue.id}/comments/', self.comment_data, format='json')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_non_contributor_create_comment(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(f'/projects/{self.project.id}/issues/{self.issue.id}/comments/', self.comment_data, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_non_contributor_update_comment(self):
        comment = Comment.objects.create(issue=self.issue, **self.comment_data)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(f'/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment.id}/', {"description": "Updated comment"}, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_non_contributor_delete_comment(self):
        comment = Comment.objects.create(issue=self.issue, **self.comment_data)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment.id}/')
        self.assertEqual(response.status_code, 403)  # Forbidden


