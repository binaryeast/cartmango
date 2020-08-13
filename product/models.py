from django.templatetags.static import static
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from taggit.managers import TaggableManager

from cart.db.time import TimeStampedModel


class Product(TimeStampedModel):
    class Meta:
        verbose_name = u'상품'
        verbose_name_plural = verbose_name
        ordering = ["-updated"]

    mall = models.ForeignKey('Mall', verbose_name=u'쇼핑몰',
                             related_name='mall_product',
                             on_delete=models.CASCADE)
    name = models.CharField(u'상품명', max_length=200)
    url = models.CharField(u'링크', max_length=300)
    price = models.PositiveIntegerField(u'가격', default=0, null=True, blank=True)
    thumbnail_src = models.CharField(u'썸네일 소스', max_length=1000, null=True, blank=True)
    thumbnail = ResizedImageField(
        u'썸네일',
        size=[900, 900], quality=80,
        crop=['middle', 'center'],
        null=True, blank=True,
        upload_to='product/%Y/%m/%d',
    )

    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        elif self.thumbnail_src:
            return self.thumbnail_src
        else:
            return static('img/no-product-image.png')

    def __str__(self):
        return '{} - {}'.format(self.name, self.mall.name)


class PersonalProduct(TimeStampedModel):
    class Meta:
        verbose_name = u'개인별 상품'
        verbose_name_plural = verbose_name
        ordering = ["-created"]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'사용자',
                             related_name='my_product',
                             on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name=u'제품',
                                related_name='personal_product',
                                on_delete=models.CASCADE)
    tags = TaggableManager()
    created = models.DateTimeField(u'생성일', default=timezone.now)
    modified = models.DateTimeField(u'수정일', blank=True, null=True)

    is_favorite = models.BooleanField(u'즐겨찾기', default=False)
    is_archived = models.BooleanField(u'보관하기', default=False)

    def __str__(self):
        return self.product.name + self.user.email

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user)
        super(PersonalProduct, self).save(*args, **kwargs)


class Mall(TimeStampedModel):
    name = models.CharField(u'쇼핑몰 이름', max_length=200)
    thumbnail = ResizedImageField(
        u'썸네일',
        size=[900, 900], quality=80,
        null=True, blank=True,
        crop=['middle', 'center'],
        upload_to='mall/%Y/%m/%d',
    )

    def __str__(self):
        return self.name

    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return static('img/no-product-image.png')


class List(TimeStampedModel):
    name = models.CharField(u'리스트 이름', unique=True, max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'사용자',
                             related_name='my_list',
                             on_delete=models.CASCADE)
    product = models.ManyToManyField(PersonalProduct, verbose_name=u'리스트 제품', blank=True)

    def __str__(self):
        return self.name

