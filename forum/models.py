import secrets
import string
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def get_digits(length=12):
    allowed_chars = string.digits
    digits = ''.join(secrets.choice(allowed_chars) for i in range(length))
    return digits


# Groups

class Group(models.Model):
    """
    A forum group.
    """
    class GroupStatus(models.TextChoices):
        REVIEW = "IN REVIEW", "In Review"
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        SUSPENDED = "SUSPENDED", "Suspended"
    
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=480)
    # Related objects
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="GroupMembership", related_name='groups_joined', blank=True)
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Administration
    status = models.CharField(choices=GroupStatus.choices, max_length=20, default=GroupStatus.ACTIVE)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Group, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('forum:group_detail', kwargs={'group': self.slug})


class Post(models.Model):
    """
    A post for a group.
    """
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField(max_length=480)
    # Related objects
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_posts')
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Administration
    pinned = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            digits = get_digits(12)
            self.slug = slugify(f"{self.title}-{digits}")
        super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('forum:post_detail', kwargs={'post': self.slug})


class Comment(models.Model):
    """
    A comment on a post.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=480)
    # Related objects
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comments')
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Administration
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created']
    
    def __str__(self):
        return self.title


# Events

class Event(models.Model):
    """
    A community event.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=480)
    location = models.CharField(max_length=255)
    start = models.DateField(default=timezone.now, null=False)
    end = models.DateField(default=timezone.now, null=False)
    url = models.URLField(blank=True, null=True)
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Administration
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['title']
    
    def __str__(self):
        return self.title


# Group membership handler

class GroupMembership(models.Model):
    class MembershipRole(models.TextChoices):
        MEMBER = "MEMBER", "Member"
        MODERATOR = "MODERATOR", "Moderator"
    
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(choices=MembershipRole.choices, max_length=20, default=MembershipRole.MEMBER)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'{self.member} joined {self.group}'