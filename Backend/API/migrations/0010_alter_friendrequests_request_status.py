# Generated by Django 4.2.14 on 2024-08-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_alter_friendrequests_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequests',
            name='request_status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
    ]
