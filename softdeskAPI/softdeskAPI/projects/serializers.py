from rest_framework import serializers
from projects.models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Project model.

    Serializes the Project model fields into JSON format.
    """

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            "contributors",
            "created_time",
        ]
        read_only_fields = ["author", "id"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Fields:
    - id: The unique identifier of the comment.
    - issue: The issue associated with the comment.
    - description: The description of the comment.
    - author: The author of the comment.
    - created_time: The timestamp when the comment was created.

    Read-only fields:
    - id: The unique identifier of the comment.
    - author: The author of the comment.
    - created_time: The timestamp when the comment was created.
    - issue: The issue associated with the comment.
    """
    class Meta:
        """
        Meta class for Comment serializer.
        """
        model = Comment
        fields = ["id", "issue", "desc", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time", "issue"]


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.

    Serializes the Contributor model fields: id, user, project, and role.
    The id and role fields are read-only.

    Usage:
    serializer = ContributorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    """

    class Meta:
        """
        Meta class for the Contributor serializer.

        Defines the metadata options for the serializer, including the model, fields, and read-only fields.
        """
        model = Contributor
        fields = ["id", "user", "project", "role"]
        read_only_fields = ["id", "role", "project"]


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.

    Serializes the Issue model fields into JSON format.
    """
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=Contributor.objects.all(),
        allow_null=True,
        required=False
    )
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "desc",
            "tag",
            "priority",
            "status",
            "project",
            "author",
            "assignee",
            "created_time",
        ]
        read_only_fields = ["id", "author", "created_time", "project"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ProjectDetailSerializer.

    This serializer is used to serialize and deserialize the Project model
    for detailed project information.

    Attributes:
        contributors (ContributorSerializer): Serializer for the contributors field.
    """

    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for defining metadata options for the Project serializer.
        """
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            "contributors",
            "created_time",
        ]
        read_only_fields = ["author", "id"]


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the CommentDetailSerializer class.

    This serializer is used to serialize and deserialize Comment objects
    for detailed representation, including the issue, description, author,
    and created time fields.

    Attributes:
        model (Comment): The Comment model class.
        fields (list): The list of fields to include in the serialized representation.
        read_only_fields (list): The list of fields that are read-only and cannot be modified.
    """
    class Meta:
        """
        Meta class for Comment serializer.
        """
        model = Comment
        fields = ["id", "issue", "description", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time", "issue"]
