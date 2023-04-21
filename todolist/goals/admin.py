from django.contrib import admin

from todolist.goals.models import GoalCategory, GoalComment, Goal, Board, BoardParticipant


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created', 'updated', 'goal',)
    search_fields = ('text',)
    list_filter = ('goal',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created', 'updated', 'status', )
    search_fields = ('title', 'description',)
    list_filter = ('status', 'priority',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'updated', )
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'created', 'updated', 'user',)
    search_fields = ('board',)
    list_filter = ('board',)
