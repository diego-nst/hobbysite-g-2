# Generated by Django 5.1.6 on 2025-03-03 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise_store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Product'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'ordering': ['name'], 'verbose_name': 'Product Type'},
        ),
        migrations.AlterField(
            model_name='product',
            name='productType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='merchandise_store.producttype'),
        ),
    ]
