from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PlayerForm, ProspectFilterForm, ScoutingReportForm, SkillGradeForm, TeamForm
from .models import Player, ScoutingReport, SkillGrade, Team


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class HomeView(ListView):
    template_name = 'home.html'
    model = Player
    context_object_name = 'players'

    def get_queryset(self):
        return (
            Player.objects.select_related('team')
            .prefetch_related('reports__skill_grade')
            .order_by('projected_pick')[:6]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_count'] = Team.objects.count()
        context['player_count'] = Player.objects.count()
        context['report_count'] = ScoutingReport.objects.count()
        spotlight_players = []
        for player in context['players']:
            reports = list(player.reports.all())
            graded_reports = [r for r in reports if hasattr(r, 'skill_grade')]
            if graded_reports:
                avg_overall = round(
                    sum(r.skill_grade.overall_grade for r in graded_reports) / len(graded_reports),
                    1,
                )
            else:
                avg_overall = None
            spotlight_players.append(
                {
                    'player': player,
                    'report_count': len(reports),
                    'avg_overall': avg_overall,
                }
            )
        context['spotlight_players'] = spotlight_players
        return context


class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'
    context_object_name = 'teams'


class TeamDetailView(DetailView):
    model = Team
    template_name = 'team_detail.html'
    context_object_name = 'team'


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'team_form.html'


class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'team_form.html'


class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'team_confirm_delete.html'
    success_url = reverse_lazy('team-list')


class PlayerListView(ListView):
    model = Player
    template_name = 'player_list.html'
    context_object_name = 'players'

    def get_queryset(self):
        return Player.objects.select_related('team').prefetch_related('reports__skill_grade')


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'player_detail.html'
    context_object_name = 'player'


class PlayerCreateView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'player_form.html'
    login_url = reverse_lazy('login')


class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'player_form.html'


class ScoutingReportDetailView(DetailView):
    model = ScoutingReport
    template_name = 'report_detail.html'
    context_object_name = 'report'


class ScoutingReportCreateView(LoginRequiredMixin, CreateView):
    model = ScoutingReport
    form_class = ScoutingReportForm
    template_name = 'report_form.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_form'] = kwargs.get('skill_form') or SkillGradeForm()
        return context

    def get_initial(self):
        initial = super().get_initial()
        player_id = self.request.GET.get('player')
        if player_id:
            initial['player'] = player_id
        return initial

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        skill_form = SkillGradeForm(request.POST)
        if form.is_valid() and skill_form.is_valid():
            report = form.save(commit=False)
            report.contributor = request.user.username
            report.save()
            skill = skill_form.save(commit=False)
            skill.report = report
            skill.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form, skill_form=skill_form))


class ScoutingReportUpdateView(LoginRequiredMixin, UpdateView):
    model = ScoutingReport
    form_class = ScoutingReportForm
    template_name = 'report_form.html'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()
        if report.is_locked:
            raise PermissionDenied('This scouting report is locked and cannot be edited.')
        if report.contributor != request.user.username:
            raise PermissionDenied('You can only edit your own scouting reports.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'skill_grade'):
            context['skill_form'] = kwargs.get('skill_form') or SkillGradeForm(instance=self.object.skill_grade)
        else:
            context['skill_form'] = kwargs.get('skill_form') or SkillGradeForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        skill_instance = getattr(self.object, 'skill_grade', None)
        skill_form = SkillGradeForm(request.POST, instance=skill_instance)
        if form.is_valid() and skill_form.is_valid():
            report = form.save()
            skill = skill_form.save(commit=False)
            skill.report = report
            skill.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form, skill_form=skill_form))


class ScoutingReportDeleteView(LoginRequiredMixin, DeleteView):
    model = ScoutingReport
    template_name = 'report_confirm_delete.html'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()
        if report.is_locked:
            raise PermissionDenied('This scouting report is locked and cannot be deleted.')
        if report.contributor != request.user.username:
            raise PermissionDenied('You can only delete your own scouting reports.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('player-detail', kwargs={'pk': self.object.player_id})


def prospects_filter_view(request):
    queryset = Player.objects.select_related('team').prefetch_related('reports__skill_grade')
    form = ProspectFilterForm(request.GET or None)

    if form.is_valid():
        position = form.cleaned_data.get('position')
        team = form.cleaned_data.get('team')
        pick_min = form.cleaned_data.get('pick_min')
        pick_max = form.cleaned_data.get('pick_max')
        min_overall_grade = form.cleaned_data.get('min_overall_grade')
        strongest_skill = form.cleaned_data.get('strongest_skill')
        sort_by = form.cleaned_data.get('sort_by')

        if position:
            queryset = queryset.filter(position=position)
        if team:
            queryset = queryset.filter(team=team)
        if pick_min is not None:
            queryset = queryset.filter(projected_pick__gte=pick_min)
        if pick_max is not None:
            queryset = queryset.filter(projected_pick__lte=pick_max)
        if min_overall_grade is not None:
            queryset = queryset.filter(reports__skill_grade__overall_grade__gte=min_overall_grade)

        queryset = queryset.distinct()
        players = list(queryset)

        if strongest_skill:
            filtered_players = []
            for player in players:
                report = player.reports.first()
                if not report or not hasattr(report, 'skill_grade'):
                    continue
                grade = report.skill_grade
                scores = {
                    'shooting': grade.shooting,
                    'finishing': grade.finishing,
                    'playmaking': grade.playmaking,
                    'defense': grade.defense,
                    'athleticism': grade.athleticism,
                    'rebounding': grade.rebounding,
                    'iq': grade.iq,
                }
                max_score = max(scores.values())
                if scores.get(strongest_skill) == max_score:
                    filtered_players.append(player)
            players = filtered_players

        if sort_by == 'overall_grade_desc':
            players.sort(
                key=lambda p: getattr(getattr(p.reports.first(), 'skill_grade', None), 'overall_grade', 0),
                reverse=True,
            )
        elif sort_by == 'overall_grade_asc':
            players.sort(
                key=lambda p: getattr(getattr(p.reports.first(), 'skill_grade', None), 'overall_grade', 0)
            )
        elif sort_by == 'projected_pick_asc':
            players.sort(key=lambda p: p.projected_pick)
        elif sort_by == 'projected_pick_desc':
            players.sort(key=lambda p: p.projected_pick, reverse=True)
        elif sort_by == 'age_asc':
            players.sort(key=lambda p: p.age)
        elif sort_by == 'age_desc':
            players.sort(key=lambda p: p.age, reverse=True)
    else:
        players = list(queryset.order_by('projected_pick'))

    return render(
        request,
        'prospect_filter.html',
        {
            'form': form,
            'players': players,
        },
    )


def leaderboard_view(request):
    players = Player.objects.select_related('team').prefetch_related('reports__skill_grade').distinct()

    aggregate_rows = []
    for player in players:
        graded_reports = [r for r in player.reports.all() if hasattr(r, 'skill_grade')]
        if not graded_reports:
            continue

        n = len(graded_reports)
        row = {
            'player': player,
            'avg_overall': round(sum(r.skill_grade.overall_grade for r in graded_reports) / n, 1),
            'avg_shooting': round(sum(r.skill_grade.shooting for r in graded_reports) / n, 1),
            'avg_defense': round(sum(r.skill_grade.defense for r in graded_reports) / n, 1),
            'avg_athleticism': round(sum(r.skill_grade.athleticism for r in graded_reports) / n, 1),
        }
        aggregate_rows.append(row)

    context = {
        'top_overall': sorted(aggregate_rows, key=lambda r: r['avg_overall'], reverse=True)[:10],
        'best_shooters': sorted(aggregate_rows, key=lambda r: r['avg_shooting'], reverse=True)[:10],
        'best_defenders': sorted(aggregate_rows, key=lambda r: r['avg_defense'], reverse=True)[:10],
        'best_athletes': sorted(aggregate_rows, key=lambda r: r['avg_athleticism'], reverse=True)[:10],
    }
    return render(request, 'leaderboards.html', context)
