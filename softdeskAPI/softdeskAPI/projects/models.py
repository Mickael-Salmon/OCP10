from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# Constants for the project model
# Choices for the project status

TYPES = [
    ('BACKEND', 'BACKEND'),
    ('FRONTEND', 'FRONTEND'),
    ('ANDROID', 'ANDROID'),
    ('IOS', 'IOS'),

]

ROLES = [
    ('AUTHOR', 'AUTHOR'),
    ('CONTRIBUTOR', 'CONTRIBUTOR'),
]

TAGS = [
    ('BUG', 'BUG'),
    ('TASK', 'TASK'),
    ('UPDATE', 'UPDATE'),
]

PRIORITIES = [
    ('LOW', 'LOW'),
    ('MEDIUM', 'MEDIUM'),
    ('HIGH', 'HIGH'),
]

STATUS = [
    ('OPEN', 'OPEN'),
    ('IN PROGRESS', 'IN PROGRESS'),
    ('COMPLETED', 'COMPLETED'),
]

class Project(models.Model):
    """Model for a project, with title, description, type, author, contributors, tags, priority, status, created_at, and updated_at."""

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)  # Increased max_length from the first class
    type = models.CharField(max_length=200, choices=TYPES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_projects')  # Included related_name from the second class
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contributor_projects')
    tags = models.CharField(max_length=200, choices=TAGS)
    priority = models.CharField(max_length=200, choices=PRIORITIES)
    status = models.CharField(max_length=200, choices=STATUS)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.description} - {self.type} - {self.author} - {self.contributors} - {self.tags} - {self.priority} - {self.status} - {self.created_at} - {self.updated_at}"

class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributor_set')
    role = models.CharField(max_length=11, choices=ROLES, default='CONTRIBUTOR')



class Issue(models.Model):
    """Represents an issue with title, description, tag, priority, status, project, author, assignee, and creation time."""

    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=2048)  # Increased max_length from the first class
    tag = models.CharField(max_length=200, choices=TAGS)
    priority = models.CharField(max_length=200, choices=PRIORITIES, default='LOW')  # Included default from the second class
    status = models.CharField(max_length=200, choices=STATUS, default='TODO')  # Included default from the second class
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(Contributor, on_delete=models.CASCADE)  # Changed from User to Contributor based on the second class
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Represents a comment with issue, description, author, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    """Represents an attachment with issue, file, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments')
    created_time = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    """Represents a notification with issue, description, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    """Represents an activity with issue, description, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)

class ProjectActivity(models.Model):
    """Represents an activity with project, description, and creation time."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)

class IssueActivity(models.Model):
    """Represents an activity with issue, description, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)

class IssueNotification(models.Model):
    """Represents a notification with issue, description, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)

class ProjectNotification(models.Model):
    """Represents a notification with project, description, and creation time."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)

class IssueAttachment(models.Model):
    """Represents an attachment with issue, file, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments')
    created_time = models.DateTimeField(auto_now_add=True)

class ProjectAttachment(models.Model):
    """Represents an attachment with project, file, and creation time."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments')
    created_time = models.DateTimeField(auto_now_add=True)

class ProjectComment(models.Model):
    """Represents a comment with project, description, author, and creation time."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class IssueComment(models.Model):
    """Represents a comment with issue, description, author, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class ProjectContributor(models.Model):
    """Represents a contributor with project, user, and creation time."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class IssueContributor(models.Model):
    """Represents a contributor with issue, user, and creation time."""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class ProjectIssue(models.Model):
    """Represents an issue with project, title, description, tag, priority, status, author, assignee, and creation time."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=1000)
    tag = models.CharField(max_length=200, choices=TAGS)
    priority = models.CharField(max_length=200, choices=PRIORITIES)
    status = models.CharField(max_length=200, choices=STATUS)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_issue_assignees')
    #assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)

