# Generated by Django 3.2.9 on 2021-12-11 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0008_alter_user_auth_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlike',
            name='user_ip',
        ),
        migrations.AddField(
            model_name='userlike',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notice.user'),
        ),
    ]