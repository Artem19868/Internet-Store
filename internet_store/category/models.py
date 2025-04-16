from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    objects = models.Manager()

    category_name = models.CharField(verbose_name='category name', max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('products_by_categories', args=[self.slug])

    def __str__(self):
        return self.category_name