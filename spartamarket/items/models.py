from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_items"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ArticleLike(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )


class Item(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    click_count = models.IntegerField(default=0)
    price = models.IntegerField()
    deleted = models.BooleanField(default=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items")
    images = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='item_images', blank=True, null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    filepath = models.ImageField(upload_to='images/', blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_images', default=1)

    def __str__(self):
        return self.filepath
