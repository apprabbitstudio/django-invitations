# Generated by Django 2.2.6 on 2019-10-19 16:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0003_auto_20151126_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='created',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='sent',
        ),
        migrations.AddField(
            model_name='invitation',
            name='accepted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='accepted at'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='approved at'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='invitation',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='invitation',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='invitation',
            name='sent_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='sent at'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='e-mail address'),
        ),
    ]
