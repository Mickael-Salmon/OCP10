from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# Constants for the project model
# Choices for the project status

TYPES = [
    ("BACKEND", "BACKEND"),
    ("FRONTEND", "FRONTEND"),
    ("ANDROID", "ANDROID"),
    ("IOS", "IOS"),
]

ROLES = [
    ("AUTHOR", "AUTHOR"),
    ("CONTRIBUTOR", "CONTRIBUTOR"),
]

TAGS = [
    ("BUG", "BUG"),
    ("TASK", "TASK"),
    ("UPDATE", "UPDATE"),
]

PRIORITIES = [
    ("LOW", "LOW"),
    ("MEDIUM", "MEDIUM"),
    ("HIGH", "HIGH"),
]

STATUS = [
    ("OPEN", "OPEN"),
    ("IN PROGRESS", "IN PROGRESS"),
    ("COMPLETED", "COMPLETED"),
]


class Project(models.Model):
    """
    Model for a project, with title, description, type, author, contributors, tags, priority, status, created_at, and updated_at.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(
        max_length=2048
    )  # Increased max_length from the first class
    type = models.CharField(max_length=200, choices=TYPES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_projects",
    )  # Included related_name from the second class
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="contributor_projects"
    )
    tags = models.CharField(max_length=200, choices=TAGS)
    priority = models.CharField(max_length=200, choices=PRIORITIES)
    status = models.CharField(max_length=200, choices=STATUS)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            """
            Returns a string representation of the project object.

            The string contains the title, description, type, author, contributors, tags, priority, status, created_at, and updated_at attributes of the project.

            Returns:
                str: A string representation of the project object.
            """
            return f"{self.title} - {self.description} - {self.type} - {self.author} - {self.contributors} - {self.tags} - {self.priority} - {self.status} - {self.created_at} - {self.updated_at}"


class Contributor(models.Model):
    """
    Represents a contributor to a project.

    Attributes:
        user (ForeignKey): The user associated with the contributor.
        project (ForeignKey): The project associated with the contributor.
        role (CharField): The role of the contributor in the project.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributor_set"
    )
    role = models.CharField(max_length=11, choices=ROLES, default="CONTRIBUTOR")
    #Empêcher la création de doublons de contributors pour un même projet - Un contributor ne devrait pas être présent plus d'une fois dans un projet
    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    """
    Represents an issue with title, description, tag, priority, status, project, author, assignee, and creation time.
    """

    title = models.CharField(max_length=200)
    desc = models.TextField(
        max_length=2048
    )  # Increased max_length from the first class
    tag = models.CharField(max_length=200, choices=TAGS)
    priority = models.CharField(
        max_length=200, choices=PRIORITIES, default="LOW"
    )  # Included default from the second class
    status = models.CharField(
        max_length=200, choices=STATUS, default="TODO"
    )  # Included default from the second class
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        Contributor, on_delete=models.CASCADE
    )  # Changed from User to Contributor based on the second class
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Represents a comment with issue, description, author, and creation time."""

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    """
    Represents an attachment with issue, file, and creation time.

    Attributes:
        issue (Issue): The issue to which the attachment belongs.
        file (FileField): The file uploaded as an attachment.
        created_time (DateTimeField): The timestamp of when the attachment was created.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments")
    created_time = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    """
    Represents a notification with issue, description, and creation time.

    Attributes:
        issue (Issue): The related issue for the notification.
        desc (str): The description of the notification.
        created_time (datetime): The creation time of the notification.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    """
    Represents an activity with issue, description, and creation time.

    Attributes:
        issue (Issue): The related issue for the activity.
        desc (str): The description of the activity.
        created_time (datetime): The timestamp when the activity was created.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)


class ProjectActivity(models.Model):
    """
    Represents an activity with project, description, and creation time.

    Attributes:
        project (Project): The project associated with the activity.
        desc (str): The description of the activity.
        created_time (datetime): The creation time of the activity.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)


class IssueActivity(models.Model):
    """
    Represents an activity with issue, description, and creation time.

    Attributes:
        issue (Issue): The issue associated with the activity.
        desc (str): The description of the activity.
        created_time (datetime): The creation time of the activity.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)


class IssueNotification(models.Model):
    """
    Represents a notification with issue, description, and creation time.

    Attributes:
        issue (Issue): The related issue for the notification.
        desc (str): The description of the notification.
        created_time (datetime): The creation time of the notification.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)


class ProjectNotification(models.Model):
    """
    Represents a notification with project, description, and creation time.

    Attributes:
        project (Project): The project associated with the notification.
        desc (str): The description of the notification.
        created_time (datetime): The creation time of the notification.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)


class IssueAttachment(models.Model):
    """
    Represents an attachment with issue, file, and creation time.

    Attributes:
        issue (Issue): The issue to which the attachment belongs.
        file (FileField): The file attached to the issue.
        created_time (DateTimeField): The timestamp of when the attachment was created.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments")
    created_time = models.DateTimeField(auto_now_add=True)


class ProjectAttachment(models.Model):
    """
    Represents an attachment with project, file, and creation time.

    Attributes:
        project (Project): The project to which the attachment belongs.
        file (FileField): The file associated with the attachment.
        created_time (DateTimeField): The timestamp when the attachment was created.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments")
    created_time = models.DateTimeField(auto_now_add=True)


class ProjectComment(models.Model):
    """
    Represents a comment with project, description, author, and creation time.

    Attributes:
        project (Project): The project associated with the comment.
        desc (str): The description of the comment.
        author (User): The author of the comment.
        created_time (datetime): The creation time of the comment.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class IssueComment(models.Model):
    """
    Represents a comment with issue, description, author, and creation time.

    Attributes:
        issue (Issue): The issue associated with the comment.
        desc (str): The description of the comment.
        author (User): The author of the comment.
        created_time (datetime): The creation time of the comment.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class ProjectContributor(models.Model):
    """
    Represents a contributor with project, user, and creation time.

    Attributes:
        project (Project): The project to which the contributor is associated.
        user (User): The user who is a contributor.
        created_time (datetime): The time when the contributor was created.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class IssueContributor(models.Model):
    """Represents a contributor with issue, user, and creation time."""

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class ProjectIssue(models.Model):
    """
    Represents an issue with project, title, description, tag, priority, status, author, assignee, and creation time.

    Attributes:
        project (Project): The project associated with the issue.
        title (str): The title of the issue.
        desc (str): The description of the issue.
        tag (str): The tag of the issue.
        priority (str): The priority of the issue.
        status (str): The status of the issue.
        author (User): The author of the issue.
        assignee (User): The assignee of the issue.
        created_time (datetime): The creation time of the issue.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=1000)
    tag = models.CharField(max_length=200, choices=TAGS)
    priority = models.CharField(max_length=200, choices=PRIORITIES)
    status = models.CharField(max_length=200, choices=STATUS)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="project_issue_assignees"
    )
    created_time = models.DateTimeField(auto_now_add=True)
