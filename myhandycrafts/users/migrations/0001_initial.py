# Generated by Django 2.2.10 on 2020-05-27 23:14

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('active', models.BooleanField(default=True, help_text='show when the object is active.', verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the objects was created.', verbose_name='create_at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date time on which the objects was last updated.', verbose_name='updated_at')),
                ('deleted_at', models.DateTimeField(help_text='Date time on which the objects was deleted.', null=True, verbose_name='deleted_at')),
                ('created_by', models.PositiveIntegerField(help_text='created_by', null=True)),
                ('updated_by', models.PositiveIntegerField(help_text='updated_by', null=True)),
                ('deleted_by', models.PositiveIntegerField(help_text='deleted_by', null=True)),
                ('email', models.EmailField(error_messages={'unique': 'A user with  thise email already exists.'}, max_length=254, unique=True, verbose_name='email')),
                ('is_verified', models.BooleanField(default=True, help_text='Set to true when the user have verified its email address.', verbose_name='verified')),
                ('is_craftsman', models.BooleanField(default=True, help_text='User is craftsman. Clients are the main type of user.', verbose_name='craftsman')),
                ('type_user', models.CharField(choices=[('A', 'Admin'), ('B', 'Craftsman'), ('C', 'Client')], default='C', max_length=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TemporalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='show when the object is active.', verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the objects was created.', verbose_name='create_at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date time on which the objects was last updated.', verbose_name='updated_at')),
                ('deleted_at', models.DateTimeField(help_text='Date time on which the objects was deleted.', null=True, verbose_name='deleted_at')),
                ('created_by', models.PositiveIntegerField(help_text='created_by', null=True)),
                ('updated_by', models.PositiveIntegerField(help_text='updated_by', null=True)),
                ('deleted_by', models.PositiveIntegerField(help_text='deleted_by', null=True)),
                ('name', models.CharField(help_text='Temporal user name', max_length=256, verbose_name='name')),
                ('email', models.EmailField(error_messages={'unique': 'A user with  thise email already exists.'}, max_length=254, unique=True, verbose_name='email')),
                ('code_devide', models.CharField(blank=True, max_length=516)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.', regex='\\+?1?\\d{6,15}$')])),
                ('is_verified', models.BooleanField(default=False, help_text='Set to true when the user have verified its email address.', verbose_name='verified')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserTemporalPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='show when the object is active.', verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the objects was created.', verbose_name='create_at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date time on which the objects was last updated.', verbose_name='updated_at')),
                ('deleted_at', models.DateTimeField(help_text='Date time on which the objects was deleted.', null=True, verbose_name='deleted_at')),
                ('created_by', models.PositiveIntegerField(help_text='created_by', null=True)),
                ('updated_by', models.PositiveIntegerField(help_text='updated_by', null=True)),
                ('deleted_by', models.PositiveIntegerField(help_text='deleted_by', null=True)),
                ('password', models.CharField(max_length=200, verbose_name='Temporal Password')),
                ('canceled_date', models.DateTimeField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'User Temporal Password',
                'verbose_name_plural': 'User Temporal Passwords',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='show when the object is active.', verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the objects was created.', verbose_name='create_at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date time on which the objects was last updated.', verbose_name='updated_at')),
                ('deleted_at', models.DateTimeField(help_text='Date time on which the objects was deleted.', null=True, verbose_name='deleted_at')),
                ('created_by', models.PositiveIntegerField(help_text='created_by', null=True)),
                ('updated_by', models.PositiveIntegerField(help_text='updated_by', null=True)),
                ('deleted_by', models.PositiveIntegerField(help_text='deleted_by', null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='users/pictures/', verbose_name='profile picture')),
                ('biography', models.TextField(blank=True, max_length=500)),
                ('ci', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField()),
                ('address', models.TextField(blank=True, max_length=256)),
                ('nit', models.CharField(blank=True, max_length=30)),
                ('nit_bussiness_name', models.CharField(blank=True, max_length=512)),
                ('nit_is_active', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.', regex='\\+?1?\\d{6,15}$')])),
                ('website', models.CharField(blank=True, max_length=128)),
                ('has_wattsapp', models.BooleanField(default=False)),
                ('has_facebook', models.BooleanField(default=False)),
                ('addres_facebook', models.TextField(blank=True, max_length=512)),
                ('reputation', models.FloatField(default=5.0, help_text="User's reputation based on crafts.")),
                ('publications', models.PositiveIntegerField(default=0)),
                ('requests', models.PositiveIntegerField(default=0)),
                ('stores', models.PositiveIntegerField(default=0)),
                ('participation_in_fairs', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rubro', to='categories.Category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]
