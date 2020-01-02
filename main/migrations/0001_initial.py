# Generated by Django 2.2.1 on 2019-05-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountToTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=155, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionETH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.BigIntegerField()),
                ('transaction_hash', models.CharField(max_length=500, unique=True)),
                ('fromAddress', models.CharField(max_length=125)),
                ('toAddress', models.CharField(max_length=125)),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=1000)),
                ('input', models.CharField(max_length=10000000)),
                ('timestamp', models.BigIntegerField()),
            ],
        ),
    ]