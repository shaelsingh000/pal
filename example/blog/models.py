from django.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from account.models import Account


def upload_loaction(instance, filename, **kwargs):
    file_path = 'blog/{author_id}/{title}.{filename}'.format(
        author_id = str(instance.author.id), title = str(instance.title), filename=filename
    )
    return file_path

class BlogPost(models.Model):
    title               = models.CharField(max_length=50, null= False, blank= False)
    body                = models.TextField(max_length=50000)
    image               = models.ImageField(upload_to= upload_loaction, null = False, blank= True)
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated        = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                = models.SlugField(blank=True,unique = True)
    likes               = models.ManyToManyField(Account,related_name='blogpost_like')


    def number_of_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title
    @property
    def number_of_comments(self):
        return comment.objects.filter(post=self).count()

@receiver(post_delete,sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender,instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username+ "-" +instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender= BlogPost)

class comment(models.Model):
    post                = models.ForeignKey(BlogPost,related_name="comments", on_delete=models.CASCADE)
    body                = models.TextField(max_length=250)
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s' %(self.post.title,self.author)