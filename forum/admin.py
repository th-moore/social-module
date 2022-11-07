from django.contrib import admin

from .models import Group, Post, Comment, Event


# Inlines

class PostCommentInline(admin.TabularInline):
    model = Comment
    fields = ['title',]
    extra = 0


class GroupMembersInline(admin.TabularInline):
    model = Group.members.through


# Group admin

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'active']
    list_filter = ['status', 'active']
    search_fields = ['title']
    inlines = [GroupMembersInline]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'pinned', 'restricted', 'active']
    list_filter = ['pinned', 'restricted', 'active']
    search_fields = ['title']
    readonly_fields = ('slug',)
    inlines = [PostCommentInline]


@admin.register(Comment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'active']
    list_filter = ['active']
    search_fields = ['title']


# Event admin

@admin.register(Event)
class ForumEventAdmin(admin.ModelAdmin):
    fields = ['title', 'location', 'url', 'start', 'end']
    list_display = ['title', 'location', 'start', 'end']
    search_fields = ['title', 'location']