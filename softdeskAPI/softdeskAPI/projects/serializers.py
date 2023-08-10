from rest_framework import serializers
from projects.models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors', 'created_time']
        read_only_fields = ['author', 'id']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'issue', 'description', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'created_time', 'issue']

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']
        read_only_fields = ['id', 'role', 'project']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'project', 'author', 'assignee', 'created_time']
        read_only_fields = ['id', 'author', 'created_time','project']

class ProjectDetailSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors', 'created_time']
        read_only_fields = ['author', 'id']

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'issue', 'description', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'created_time', 'issue']

