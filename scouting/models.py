from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Team(models.Model):
    CONFERENCE_CHOICES = [
        ('East', 'East'),
        ('West', 'West'),
        ('Intl', 'International'),
    ]

    name = models.CharField(max_length=120, unique=True)
    conference = models.CharField(max_length=20, choices=CONFERENCE_CHOICES)
    country = models.CharField(max_length=80)
    logo_url = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team-detail', kwargs={'pk': self.pk})


class Player(models.Model):
    POSITION_CHOICES = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
        ('G/F', 'Guard/Forward'),
        ('F/C', 'Forward/Center'),
    ]

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    height = models.CharField(max_length=20, help_text='Example: 6-8')
    weight = models.PositiveIntegerField(help_text='Weight in pounds')
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(40)])
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    projected_pick = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(60)])
    image_url = models.URLField(blank=True)
    bio = models.TextField()

    class Meta:
        ordering = ['projected_pick', 'last_name']
        unique_together = [('first_name', 'last_name', 'team')]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('player-detail', kwargs={'pk': self.pk})


class ScoutingReport(models.Model):
    PLAYER_LEVEL_CHOICES = [
        ('rotation', 'Rotational NBA Player'),
        ('starter', 'Starting Level Player'),
        ('all_star', 'All-Star Caliber Player'),
        ('superstar', 'Superstar Player'),
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reports')
    contributor = models.CharField(max_length=80, default='Anonymous Scout')
    summary = models.TextField()
    strengths = models.TextField()
    weaknesses = models.TextField()
    nba_comparison = models.CharField(max_length=120)
    projected_nba_level = models.CharField(max_length=20, choices=PLAYER_LEVEL_CHOICES, default='starter')
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Report: {self.player} ({self.updated_at.date()})'

    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.pk})


class SkillGrade(models.Model):
    report = models.OneToOneField(ScoutingReport, on_delete=models.CASCADE, related_name='skill_grade')
    shooting = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    finishing = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    playmaking = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    defense = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    athleticism = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    rebounding = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    iq = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    overall_grade = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        ordering = ['-overall_grade']

    def __str__(self):
        return f'{self.report.player} | Overall {self.overall_grade}'
