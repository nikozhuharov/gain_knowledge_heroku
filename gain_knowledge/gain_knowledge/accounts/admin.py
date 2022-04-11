from django.contrib import admin

from gain_knowledge.accounts.models import GainKnowledgeUser


@admin.register(GainKnowledgeUser)
class GainKnowledgeUserAdmin(admin.ModelAdmin):
    pass
