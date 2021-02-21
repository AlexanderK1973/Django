from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, verbose_name='Выбери Автора', on_delete=models.CASCADE, unique=True)
    author_raiting = models.IntegerField(verbose_name='Рейтинг выбранного Автора', default=0)

    class Meta:
        verbose_name = 'Перечень авторов'
        verbose_name_plural = 'Авторы'

    def update_raiting(self):
        posts = Post.objects.filter(author=self.id)  # выбор поста по id автора
        post_raiting = sum([r.post_raiting * 3 for r in posts])  # суммируем рейтинг постов автора умноженный на 3
        comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(author=self.author)])  #считаем лайки к комментам автора
        all_to_post_comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(post__in = posts)]) # сумма лайков/дислайков постам
        self.author_raiting = post_raiting + comment_raiting + all_to_post_comment_raiting
        self.save()

    def __str__(self):
        return self.author.username


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория', unique=True)

    class Meta:
        verbose_name = 'Перечень категорий'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    NEWS = 'NW'
    ARTICLE = 'AR'
    SELECT = 'ST'

    POST_TYPES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
        (SELECT, 'Выбрать'),
    ]
    type = models.CharField(max_length=2, choices=POST_TYPES, default=SELECT, verbose_name='Тип')
    created_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory',)
    header = models.CharField(max_length=255, verbose_name='Заголовок')
    article_text = models.TextField(verbose_name='Текст')
    post_raiting = models.IntegerField(default=0, verbose_name='Рейтинг')

    def preview(self):
        preview = self.article_text[:129] + '...'
        return preview

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()

    def __str__(self):
        return self.header


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория Поста'
        verbose_name_plural = 'Категории Постов'

    def __str__(self):
        return self.category.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_time = models.DateTimeField(auto_now_add=True)
    comment_raiting = models.IntegerField(default=0, verbose_name='Рейтинг комментариев')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        info = str(self.author.username)
        return info

    def like(self):
        self.comment_raiting += 1
        self.save()

    def dislike(self):
        self.comment_raiting -= 1
        self.save()

