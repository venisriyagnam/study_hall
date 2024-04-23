# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Application(models.Model):
    application_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    resume = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'application'


class Career(models.Model):
    job_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    requirements = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'career'


class Complaints(models.Model):
    complaint_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'complaints'


class Donate(models.Model):
    donation_id = models.IntegerField(primary_key=True)
    item = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    availability = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'donate'


class Forum(models.Model):
    post_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    reply_to = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'forum'


class Library(models.Model):
    book_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'library'


class LibraryHistory(models.Model):
    book_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'library_history'


class Pc(models.Model):
    pc_id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    availability = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pc'


class PcAllocation(models.Model):
    allocation_id = models.IntegerField(primary_key=True)
    pc_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pc_allocation'


class Reserve(models.Model):
    reserve_id = models.BigAutoField(primary_key=True)
    room_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=False, null=False)
    reserve_date = models.CharField(max_length=255, null=True)
    reserve_timestamp = models.CharField(max_length = 255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'reserve'


class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'review'


class Room(models.Model):
    room_number = models.IntegerField(primary_key=True)
    capacity = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'room'


class Store(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    availability = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'store'


class User1(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=50)
    user_role = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'

class Points(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    points = models.IntegerField(default = 0)

    class Meta:
        managed = True
        db_table = 'points'

class UserRole(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    user_role = models.CharField(default = 'student', max_length=100)

    class Meta:
        managed = True
        db_table = 'user_role'

class Feedback(models.Model):
    username = models.CharField(max_length=100, blank = True, null = True)
    email = models.CharField(max_length=100, blank = True, null = True)
    message = models.CharField(max_length=10000, blank = True, null = True)

    class Meta:
        managed = True
        db_table = 'feedback'