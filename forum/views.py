from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import GroupJoinForm, PostCreateForm, PostEditForm, PostCommentForm
from .models import Event, Group, Post, Comment, GroupMembership


CustomUser = get_user_model()


def group_list(request):
    groups = Group.objects.filter(active=True, status='ACTIVE').order_by('-title')
    
    context = {
        'cnav': 'groups',
        'gnav': 'all',
        'object_list': groups,
    }
    return render(request, 'forum/groups/group_list.html', context)


@require_POST
@login_required
def group_join(request):
    group_id = request.POST.get('id')
    action = request.POST.get('action')

    if group_id and action:
        try:
            joined_group = Group.objects.get(id=group_id)
            if action == 'join':
                GroupMembership.objects.get_or_create(member=request.user, group=joined_group)
            else:
                GroupMembership.objects.filter(member=request.user, group=joined_group).delete()
            return JsonResponse({'status':'ok'})
        except Group.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})


def group_detail(request, group):
    group = get_object_or_404(Group, slug=group)
    posts = group.posts.filter(active=True)
    members = group.members.all()
    moderators = members.filter(groupmembership__role='MODERATOR')
    join_form = GroupJoinForm(initial={'group': group})
    
    context = {
        'gnav': 'posts',
        'pnav': 'recent',
        'group': group,
        'object_list': posts,
        'members': members,
        'moderators': moderators,
        'join_form': join_form,
    }
    return render(request, 'forum/groups/group_detail.html', context)


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    # Handle comment via POST request
    if request.method == 'POST':
        # A comment was posted
        comment_form = PostCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current thread to the comment
            new_comment.post = post
            # Assign the current user to the comment
            new_comment.author = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = PostCommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'forum/posts/post_detail.html', context)


@login_required
def post_create(request, group):
    # Get the viewed Group
    group = get_object_or_404(Group, slug=group)
    # Check the user is a member of the group, if not raise a 404
    membership = get_object_or_404(GroupMembership, member=request.user, group=group)

    new_post = None
    if request.method == 'POST':
        # A post was posted
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            # Create a post object but don't save to database yet
            new_post = form.save(commit=False)
            # Assign the current user to the post
            new_post.author = request.user
            # Save the post to the database
            new_post.save()
            # Redirect to the newly created post's detail page
            return redirect('forum:post_detail', post=new_post.slug)
    else:
        form = PostCreateForm()

    context = {
        'new_post': new_post,
        'form': form,
        'group': group,
    }
    return render(request, 'forum/posts/post_create.html', context)


@login_required
def post_update(request, post):
    post = get_object_or_404(Post, slug=post)
    # Check user is author of post and raise 404 if not
    if post.author != request.user:
        raise Http404("You are not allowed to edit this Post")
    # Handle POST request
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('forum:post_detail', post=post.slug)
    else:
        form = PostEditForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'forum/posts/post_update.html', context)


@login_required
def post_delete(request, post):
    post = get_object_or_404(Post, slug=post)
    # Check user is author of post and raise 404 if not
    if post.author != request.user:
        raise Http404("You are not allowed to edit this Post")
    # Handle POST request
    if request.method =="POST":
        # Delete object
        post.delete()
        # After deleting redirect to community page
        return redirect('forum:group_list')

    context = {
        'post': post,
    }
    return render(request, 'forum/posts/post_delete.html', context)


# EVENTS

def event_list(request):
    today = timezone.now().date()
    events = Event.objects.filter(start__gte=today).order_by('-start')
    
    context = {
        'cnav': 'events',
        'object_list': events,
        'today': today,
    }
    return render(request, 'forum/events/event_list.html', context)