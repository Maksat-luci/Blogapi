from django.db import models

from main.models import Post


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-value']

class Rating(models.Model):
    email = models.EmailField()
    star = models.ForeignKey(RatingStar,on_delete=models.CASCADE, verbose_name='звезда')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,verbose_name='пост',related_name="ratings")

    def __str__(self):
        return f'{self.star} - {self.post}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = "Рейтинги"
