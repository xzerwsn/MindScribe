from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Переименовано с text на content
    excerpt = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)
    featured = models.BooleanField(default=False, verbose_name="Избранный пост")
    media_file = models.FileField(
        upload_to='post_media/',
        null=True,
        blank=True,
        verbose_name="Медиа-контент",
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'jpg', 'jpeg', 'png', 'gif', 'svg', 
                'mp4', 'webm', 'avi'
            ])
        ]
    )
    MEDIA_TYPE_CHOICES = [
        ('image', 'Фото'),
        ('video', 'Видео'),
        ('gif', 'GIF'),
    ]
    media_type = models.CharField(
        max_length=5,
        choices=MEDIA_TYPE_CHOICES,
        null=True,
        blank=True
    )

    def is_author(self, user):
        """Проверяет, является ли пользователь автором поста"""
        return self.author == user

    class Meta:
        ordering = ['-published_date']  # Сортировка по умолчанию

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.media_file:
            filename = self.media_file.name.lower()
            if filename.endswith(('.gif')):
                self.media_type = 'gif'
            elif filename.endswith(('.mp4', '.webm', '.avi')):
                self.media_type = 'video'
            elif filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.svg')):
                self.media_type = 'image'
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    github = models.URLField(max_length=100, blank=True)
    vk = models.URLField(max_length=100, blank=True)
    telegram = models.CharField(max_length=50, blank=True)
    discord = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Создает или обновляет профиль пользователя"""
    if created:
        Profile.objects.create(user=instance)
    else:
        # Для существующих пользователей, у которых нет профиля
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
        instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()