from django import forms

from .models import Player, ScoutingReport, SkillGrade, Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'conference', 'country', 'logo_url']


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'first_name',
            'last_name',
            'position',
            'height',
            'weight',
            'age',
            'team',
            'projected_pick',
            'image_url',
            'bio',
        ]


class ScoutingReportForm(forms.ModelForm):
    class Meta:
        model = ScoutingReport
        fields = [
            'player',
            'summary',
            'strengths',
            'weaknesses',
            'nba_comparison',
            'projected_nba_level',
        ]


class SkillGradeForm(forms.ModelForm):
    class Meta:
        model = SkillGrade
        fields = [
            'shooting',
            'finishing',
            'playmaking',
            'defense',
            'athleticism',
            'rebounding',
            'iq',
            'overall_grade',
        ]


class ProspectFilterForm(forms.Form):
    SORT_CHOICES = [
        ('', 'Default'),
        ('overall_grade_desc', 'Overall Grade: High to Low'),
        ('overall_grade_asc', 'Overall Grade: Low to High'),
        ('projected_pick_asc', 'Projected Pick: 1 to 60'),
        ('projected_pick_desc', 'Projected Pick: 60 to 1'),
        ('age_asc', 'Age: Youngest First'),
        ('age_desc', 'Age: Oldest First'),
    ]

    SKILL_CHOICES = [
        ('', 'Any'),
        ('shooting', 'Shooting'),
        ('finishing', 'Finishing'),
        ('playmaking', 'Playmaking'),
        ('defense', 'Defense'),
        ('athleticism', 'Athleticism'),
        ('rebounding', 'Rebounding'),
        ('iq', 'Basketball IQ'),
    ]

    position = forms.ChoiceField(choices=[('', 'Any')] + Player.POSITION_CHOICES, required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.none(), required=False, empty_label='Any')
    pick_min = forms.IntegerField(required=False, min_value=1, max_value=60)
    pick_max = forms.IntegerField(required=False, min_value=1, max_value=60)
    min_overall_grade = forms.IntegerField(required=False, min_value=1, max_value=100)
    strongest_skill = forms.ChoiceField(choices=SKILL_CHOICES, required=False)
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.all().order_by('name')
