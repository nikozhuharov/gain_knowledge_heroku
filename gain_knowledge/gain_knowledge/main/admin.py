from django.contrib import admin

# Register your models here.
from gain_knowledge.main.models import Category, Course, Test, Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Test)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class CategoryAdmin(admin.ModelAdmin):
    pass