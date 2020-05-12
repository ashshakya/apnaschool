# Generated by Django 3.0.6 on 2020-05-12 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('middle_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('email', models.EmailField(blank=True, db_column='email', db_index=True, max_length=256, null=True, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('unique_code', models.CharField(blank=True, db_index=True, editable=False, max_length=64, null=True, unique=True)),
                ('mobile', models.CharField(blank=True, db_index=True, max_length=13, null=True)),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Please select the gender.'), (1, 'Male'), (2, 'Female')], null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.StudentsCategory')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('primary_address', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_primary_address', to='data.Address')),
                ('secondary_address', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_secondary_address', to='data.Address')),
                ('standard', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='standard', to='data.Standard')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('middle_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('email', models.EmailField(blank=True, db_column='email', db_index=True, max_length=256, null=True, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('unique_code', models.CharField(blank=True, db_index=True, editable=False, max_length=64, null=True, unique=True)),
                ('mobile', models.CharField(blank=True, db_index=True, max_length=13, null=True)),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Please select the gender.'), (1, 'Male'), (2, 'Female')], null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('user_type', models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Please select a user type.'), (1, 'Staff'), (2, 'Employee')], null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('department', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='department', to='data.Department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='employee_set', related_query_name='employee', to='auth.Group', verbose_name='groups')),
                ('primary_address', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='employee_primary_address', to='data.Address')),
                ('secondary_address', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='employee_secondary_address', to='data.Address')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='employee_set', related_query_name='employee', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Employees',
            },
        ),
    ]
