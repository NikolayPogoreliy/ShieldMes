from django.db import models
#from mptt.models import MPTTModel, TreeForeignKey
from tinymce import models as model_tinymce

# Create your models here.
class Posts(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=0, related_name='children')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Заголовок сообщения')
    text = models.TextField(blank=False, verbose_name='Текст сообщения')
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False, verbose_name='Дата публикации')
    master_id = models.IntegerField(null=True, default=0, editable=False, verbose_name='Номер корня ветки сообщений')
    level = models.IntegerField(null=True, default=0, editable=False, verbose_name='Уровень вложенности')
    coments_count = models.IntegerField(null=True, default=0, editable=False, verbose_name='количество комментариев' )
    author_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Автор')
    author_link = models.URLField(blank=True, null=True, verbose_name='Страничка автора в соцсетях')
    author_pic = models.URLField(blank=True, null=True, verbose_name='Страничка автора в соцсетях')
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.text

    class Meta():
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


"""class PostsMaxLevel(models.Model):
    master = models.ForeignKey(Posts, unique=True, verbose_name='Номер корня')
    maxlevel = models.IntegerField(null=True, default=0, editable=False, verbose_name='Максимальный уровень вложенности для ветки')"""