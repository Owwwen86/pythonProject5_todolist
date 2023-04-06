from django.urls import path

from todolist.goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category-goal'),
    path('goal_category/<int:pk>', GoalCategoryView.as_view(), name='goal-category'),
]
