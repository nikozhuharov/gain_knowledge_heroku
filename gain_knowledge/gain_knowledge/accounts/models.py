from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models

from gain_knowledge.accounts.manager import GainKnowledgeUserManager
from gain_knowledge.main.validators import validate_only_letters, MaxFileSizeInMbValidator


class GainKnowledgeUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 25

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = GainKnowledgeUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    IMAGE_MAX_SIZE_IN_MB = 5

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    picture = models.ImageField(
        upload_to='images/profile',
        validators=(
             MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
         )
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    email = models.EmailField()

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW
    )

    user = models.OneToOneField(
        GainKnowledgeUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CurrentResult(models.Model):
    user = models.OneToOneField(
        GainKnowledgeUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    correct_answers = models.IntegerField()

    incorrect_answers = models.IntegerField()