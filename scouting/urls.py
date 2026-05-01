from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('prospects/', views.PlayerListView.as_view(), name='player-list'),
    path('prospects/filter/', views.prospects_filter_view, name='prospect-filter'),
    path('prospects/create/', views.PlayerCreateView.as_view(), name='player-create'),
    path('prospects/<int:pk>/', views.PlayerDetailView.as_view(), name='player-detail'),
    path('prospects/<int:pk>/edit/', views.PlayerUpdateView.as_view(), name='player-update'),

    path('reports/<int:pk>/', views.ScoutingReportDetailView.as_view(), name='report-detail'),
    path('reports/create/', views.ScoutingReportCreateView.as_view(), name='report-create'),
    path('reports/<int:pk>/edit/', views.ScoutingReportUpdateView.as_view(), name='report-update'),
    path('reports/<int:pk>/delete/', views.ScoutingReportDeleteView.as_view(), name='report-delete'),

    path('leaderboards/', views.leaderboard_view, name='leaderboards'),
]
