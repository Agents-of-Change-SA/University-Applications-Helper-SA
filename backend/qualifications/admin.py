from django.contrib import admin

from .models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SelectionRequirement,
    SubjectRequirement,
)


class APSRuleConditionInline(admin.TabularInline):
    model = APSRuleCondition
    extra = 1


class APSRuleInline(admin.TabularInline):
    model = APSRule
    extra = 0
    show_change_link = True


class SubjectRequirementInline(admin.TabularInline):
    model = SubjectRequirement
    extra = 1


class SelectionRequirementInline(admin.TabularInline):
    model = SelectionRequirement
    extra = 0


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'qualification_code', 'faculty', 'minimum_aps')
    list_filter = ('institution', 'faculty')
    search_fields = ('name', 'qualification_code', 'faculty')
    inlines = [APSRuleInline, SubjectRequirementInline, SelectionRequirementInline]


@admin.register(APSRule)
class APSRuleAdmin(admin.ModelAdmin):
    list_display = ('qualification', 'rule_type')
    inlines = [APSRuleConditionInline]
