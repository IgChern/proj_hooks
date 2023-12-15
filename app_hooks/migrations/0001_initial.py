# Generated by Django 4.2.7 on 2023-12-07 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('data', models.JSONField(blank=True, default=list, null=True, verbose_name='Filter Data')),
            ],
            options={
                'verbose_name': 'Filter',
                'verbose_name_plural': 'Filters',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('endpoint', models.TextField(verbose_name='Endpoint')),
                ('template', models.TextField(blank=True, verbose_name='Template')),
                ('callback', models.URLField(verbose_name='Callback')),
                ('filters', models.ManyToManyField(related_name='events', to='app_hooks.filter')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]