from django.urls import path

from todolist.goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView, GoalCreateView, \
    GoalListView, GoalView, GoalCommentCreateView, GoalCommentListView, GoalCommentView, BoardCreateView, BoardListView, \
    BoardView

urlpatterns = [
    # Board API
    path('board/create', BoardCreateView.as_view(), name='create-board'),
    path('board/list', BoardListView.as_view(), name='board-list'),
    path('board/<int:pk>', BoardView.as_view(), name='board'),
    # Goal Category API
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category-list'),
    path('goal_category/<int:pk>', GoalCategoryView.as_view(), name='goal-category'),
    # Goals API
    path('goal/create', GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='goal-list'),
    path('goal/<int:pk>', GoalView.as_view(), name='goal'),
    # Goals Comments API
    path('goal_comment/create', GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', GoalCommentView.as_view(), name='comment'),
]
