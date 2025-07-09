from django.urls import path
from . import api_views

urlpatterns = [
    # Assembly endpoints
    path('leagues/assemble-scoring/', api_views.assemble_scoring_league, name='assemble_scoring_league'),
    path('leagues/assemble-scoring-stream/', api_views.assemble_scoring_league_stream, name='assemble_scoring_league_stream'),
    path('leagues/assemble-draft/', api_views.assemble_draft_league, name='assemble_draft_league'),
    
    # Progress tracking
    path('progress/<str:assembly_id>/', api_views.get_progress, name='get_progress'),
    
    # Scoring analysis endpoints
    path('leagues/<str:league_id>/scoring/expected-wins/', api_views.expected_wins_analysis, name='expected_wins_analysis'),
    path('leagues/<str:league_id>/scoring/ew-difference/', api_views.ew_difference_analysis, name='ew_difference_analysis'),
    path('leagues/<str:league_id>/scoring/luck/', api_views.luck_analysis, name='luck_analysis'),
    path('leagues/<str:league_id>/scoring/bonage/', api_views.bonage_analysis, name='bonage_analysis'),
    path('leagues/<str:league_id>/scoring/consistency/', api_views.consistency_analysis, name='consistency_analysis'),
    path('leagues/<str:league_id>/scoring/probability-curve/', api_views.probability_curve_analysis, name='probability_curve_analysis'),
    
    # Draft analysis endpoints
    path('leagues/<str:league_id>/draft/sleepers/', api_views.sleepers_analysis, name='sleepers_analysis'),
    path('leagues/<str:league_id>/draft/positional-ranks/', api_views.positional_ranks_analysis, name='positional_ranks_analysis'),
    path('leagues/<str:league_id>/draft/injury-table/', api_views.draft_injury_analysis, name='draft_injury_analysis'),
    
    # Debug endpoint
    path('leagues/<str:league_id>/debug/', api_views.debug_league_info, name='debug_league_info'),
] 