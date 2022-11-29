from django.db import models


class Tag(models.Model):
    """Теги для рецептов."""
    name = models.CharField('Название', max_length=200, unique=True)
    color_code = models.CharField('HEX-код цвета', max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta():
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:20]
