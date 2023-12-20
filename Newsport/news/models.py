from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAutor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commendRat = self.autorUser.comment_set.aggregate(commendRating=Sum('rating'))
        cRat = 0
        cRat += commendRat.get('commendRating')

        self.ratingAutor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'Nw'
    ARTICLE = "Ar"
    CATEGORY_CHOICES = [
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья')
    ]
    categoryType = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title1 = models.TextField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def preview(self):
        return self.text[0:128] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('global', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commendPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commendUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


