#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tasks.views import TodoViewSet, SubtaskViewSet
from rest_framework import routers

router = routers.SimpleRouter()

# registering djoser endpoints
router.register(r'todos', TodoViewSet)
router.register(r'subtasks', SubtaskViewSet)

urlpatterns = router.urls
