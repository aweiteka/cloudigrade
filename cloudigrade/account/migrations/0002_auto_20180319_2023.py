# Generated by Django 2.0.2 on 2018-03-19 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_account.account_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='instance',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_account.instance_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='instanceevent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_account.instanceevent_set+', to='contenttypes.ContentType'),
        ),
    ]
