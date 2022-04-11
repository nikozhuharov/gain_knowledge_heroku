from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import models

from gain_knowledge.main.validators import validate_only_letters, MaxFileSizeInMbValidator

UserModel = get_user_model()


class Category(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 30
    IMAGE_MAX_SIZE_IN_MB = 5

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=(
            MinLengthValidator(TITLE_MIN_LENGTH),
        )
    )

    picture = models.ImageField(
        upload_to='images/category',
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        )
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 30
    IMAGE_MAX_SIZE_IN_MB = 5

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=(
            MinLengthValidator(TITLE_MIN_LENGTH),
        )
    )

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    picture = models.ImageField(
        upload_to='images/course',
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        )
    )

    video = models.FileField(
        upload_to='videos',
        validators=(
            FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv']),
        )
    )

    document = models.FileField(
        upload_to='documents',
        validators=(
            FileExtensionValidator(allowed_extensions=['pdf']),
        )
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}'


class Test(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 30

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=(
            MinLengthValidator(TITLE_MIN_LENGTH),
        )
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    FIRST_OPTION = 'A'
    SECOND_OPTION = 'B'
    THIRD_OPTION = 'C'
    FOURTH_OPTION = 'D'
    OPTIONS = [(x, x) for x in (FIRST_OPTION, SECOND_OPTION, THIRD_OPTION, FOURTH_OPTION)]

    title = models.TextField()

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )

    first_option = models.TextField()

    second_option = models.TextField()

    third_option = models.TextField()

    fourth_option = models.TextField()

    correct_answer = models.CharField(
        max_length=max(len(x) for x, _ in OPTIONS),
        choices=OPTIONS,
    )

    def __str__(self):
        return f'{self.title}'



