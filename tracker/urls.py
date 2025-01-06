from tracker.apps import TrackerConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from tracker.views import (
    EmployeeViewSet,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskDeleteAPIView,
    TaskCreateAPIView,

)

app_name = TrackerConfig.name

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employees")

urlpatterns = [
                  path("task/task_list/", TaskListAPIView.as_view(), name="task_list"),
                  path("task/retrieve/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task_retrieve"),
                  path("task/create/", TaskCreateAPIView.as_view(), name="task_create"),
                  path("task/update/<int:pk>/", TaskUpdateAPIView.as_view(), name="task_update"),
                  path("task/delete/<int:pk>/", TaskDeleteAPIView.as_view(), name="task_delete"),

              ] + router.urls