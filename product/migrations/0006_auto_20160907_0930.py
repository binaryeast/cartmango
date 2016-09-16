# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-07 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20160907_0917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personalproduct',
            options={'verbose_name': '개인별 상품', 'verbose_name_plural': '개인별 상품'},
        ),
        migrations.AddField(
            model_name='personalproduct',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성일'),
        ),
        migrations.AddField(
            model_name='personalproduct',
            name='modified',
            field=models.DateTimeField(blank=True, null=True, verbose_name='수정일'),
        ),
        migrations.AddField(
            model_name='personalproduct',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]