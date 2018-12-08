# Generated by Django 2.1.3 on 2018-12-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_desc'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, to='organization.CourseOrg', verbose_name='课程机构'),
        ),
    ]