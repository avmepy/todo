from rest_framework.response import Response
from tasks.serializers import TodoSerializer, SubtaskSerializer
from rest_framework import viewsets
from tasks.models import Todo, Subtask
from rest_framework import permissions


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        overriding create method
        picking user
        """
        todo_data = request.data
        new_todo = Todo.objects.create(user=self.request.user, text=todo_data['text'],
                                       color=todo_data['color'] if 'color' in todo_data.keys() else "#ffffff")
        new_todo.save()

        serializer = TodoSerializer(new_todo)
        return Response(serializer.data)


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Subtask.objects.filter(todo_id=self.request.data.get('todo_id'))

    def create(self, request, *args, **kwargs):
        """
        same as todo's
        """
        subtask_data = request.data
        print(subtask_data)
        new_subtask = Subtask.objects.create(todo_id=subtask_data['todo_id'],
                                             text=subtask_data['text'],
                                             color=subtask_data['color'] if 'color' in subtask_data.keys()
                                             else "#ffffff")
        new_subtask.save()

        serializer = SubtaskSerializer(new_subtask)
        return Response(serializer.data)

