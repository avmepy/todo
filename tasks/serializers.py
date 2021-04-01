#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from rest_framework import serializers
from tasks.models import Todo, Subtask


class SubtaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = ('id', 'todo', 'text', 'color')


class TodoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Todo
        fields = ('id', 'text', 'color', 'subtasks')

