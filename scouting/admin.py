from django.contrib import admin

from .models import Player, ScoutingReport, SkillGrade, Team


class SkillGradeInline(admin.StackedInline):
    model = SkillGrade
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'conference', 'country')
    search_fields = ('name', 'country')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'team', 'projected_pick', 'age')
    list_filter = ('position', 'team')
    search_fields = ('first_name', 'last_name', 'team__name')


@admin.register(ScoutingReport)
class ScoutingReportAdmin(admin.ModelAdmin):
    list_display = ('player', 'contributor', 'projected_nba_level', 'updated_at')
    list_filter = ('projected_nba_level',)
    search_fields = ('player__first_name', 'player__last_name', 'contributor', 'nba_comparison')
    inlines = [SkillGradeInline]


@admin.register(SkillGrade)
class SkillGradeAdmin(admin.ModelAdmin):
    list_display = ('report', 'overall_grade', 'shooting', 'defense', 'athleticism')
    search_fields = ('report__player__first_name', 'report__player__last_name')
