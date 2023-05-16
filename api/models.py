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
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


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
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    item_desc = models.CharField(max_length=500, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    protein = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    carbs = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    vegan = models.IntegerField(blank=True, null=True)
    vegetarian = models.IntegerField(blank=True, null=True)
    bread = models.IntegerField(blank=True, null=True)
    rice = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "items"


class MealItem(models.Model):
    id = models.IntegerField(primary_key=True)
    meal = models.ForeignKey("Meals", models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(Items, models.DO_NOTHING, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "meal_item"


class Meals(models.Model):
    meal_id = models.IntegerField(primary_key=True)
    meal_name = models.CharField(max_length=50, blank=True, null=True)
    meal_des = models.CharField(max_length=300, blank=True, null=True)
    snack = models.IntegerField(blank=True, null=True)
    breakfast = models.IntegerField(blank=True, null=True)
    lunch = models.IntegerField(blank=True, null=True)
    dinner = models.IntegerField(blank=True, null=True)
    warm = models.IntegerField(blank=True, null=True)
    hard = models.IntegerField(blank=True, null=True)
    salty = models.IntegerField(blank=True, null=True)
    sweety = models.IntegerField(blank=True, null=True)
    spicy = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "meals"


class Questions(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_desc = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "questions"


class UserQuestion(models.Model):
    user_question_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey(Questions, models.DO_NOTHING, blank=True, null=True)
    question_answer = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user_question"


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=20, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"
