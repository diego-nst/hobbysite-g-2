# Generated by Django 5.1.6 on 2025-03-07 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0006_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='commissions.commission'),
        ),
    ]
