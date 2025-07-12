from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.http import StreamingHttpResponse
import uuid
import json
import threading
import queue
from analysis.league.league import League


@api_view(['POST'])
def assemble_scoring_league(request):
    """
    Assemble league data for scoring analysis.
    Returns a unique league_id for subsequent analysis calls.
    """
    try:
        # Extract parameters
        platform = request.data.get('platform', 'espn')
        league_id = request.data.get('league_id')
        s2 = request.data.get('s2', None)
        swid = request.data.get('swid', None)
        
        if not league_id:
            return Response(
                {'error': 'league_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create unique identifier for this assembly
        assembly_id = f"scoring_{league_id}_{platform}_{uuid.uuid4().hex[:8]}"
        
        # Create league object (this is the heavy processing)
        league = League(platform, league_id, s2=s2, swid=swid)
        
        if league is None:
            return Response(
                {'error': 'Failed to create league object'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cache the league object
        cache_key = f"league_scoring_{assembly_id}"
        cache.set(cache_key, league, timeout=3600)  # Cache for 1 hour
        
        # Return minimal response with league_id
        response_data = {
            'league_id': assembly_id,
            'status': 'ready'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Assembly failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def progress_stream(assembly_id, platform, league_id, s2=None, swid=None):
    yield f"data: {json.dumps({'type': 'progress', 'message': 'Starting assembly...', 'percent': 0})}\n\n"
    q = queue.Queue()

    def progress_callback(message, percent):
        q.put((message, percent))

    def build_league():
        league = League(platform, league_id, s2=s2, swid=swid, progress_id=assembly_id, progress_callback=progress_callback)
        # Remove callback before caching
        league.progress_callback = None
        cache_key = f"league_scoring_{assembly_id}"
        cache.set(cache_key, league, timeout=3600)
        cache.set(f"progress_{assembly_id}", {
            'status': 'complete',
            'message': 'Assembly complete!',
            'percent': 100
        }, timeout=3600)
        q.put('COMPLETE')

    thread = threading.Thread(target=build_league)
    thread.start()

    while True:
        update = q.get()
        if update == 'COMPLETE':
            yield f"data: {json.dumps({'type': 'complete', 'result': {'league_id': assembly_id, 'status': 'ready'}})}\n\n"
            break
        message, percent = update
        yield f"data: {json.dumps({'type': 'progress', 'message': message, 'percent': percent})}\n\n"

@api_view(['POST'])
def assemble_scoring_league_stream(request):
    """
    Assemble league data with real-time progress updates via Server-Sent Events.
    """
    try:
        # Extract parameters
        platform = request.data.get('platform', 'espn')
        league_id = request.data.get('league_id')
        s2 = request.data.get('s2', None)
        swid = request.data.get('swid', None)
        
        if not league_id:
            return Response(
                {'error': 'league_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create unique identifier for this assembly
        assembly_id = f"scoring_{league_id}_{platform}_{uuid.uuid4().hex[:8]}"
        
        # Return streaming response
        response = StreamingHttpResponse(
            progress_stream(assembly_id, platform, league_id, s2, swid),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Assembly failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_progress(request, assembly_id):
    """
    Get progress status for an assembly operation.
    """
    try:
        progress_data = cache.get(f"progress_{assembly_id}")
        if progress_data is None:
            return Response(
                {'error': 'Progress not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(progress_data)
        
    except Exception as e:
        return Response(
            {'error': f'Progress check failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def assemble_draft_league(request):
    """
    Assemble league data for draft analysis.
    Returns a unique league_id for subsequent analysis calls.
    """
    try:
        # Extract parameters
        platform = request.data.get('platform', 'espn')
        league_id = request.data.get('league_id')
        s2 = request.data.get('s2', None)
        swid = request.data.get('swid', None)
        
        if not league_id:
            return Response(
                {'error': 'league_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create unique identifier for this assembly
        assembly_id = f"draft_{league_id}_{platform}_{uuid.uuid4().hex[:8]}"
        
        # Create league object (this is the heavy processing)
        league = League(platform, league_id, s2=s2, swid=swid)
        
        if league is None:
            return Response(
                {'error': 'Failed to create league object'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cache the league object
        cache_key = f"league_draft_{assembly_id}"
        cache.set(cache_key, league, timeout=86400)  # Cache for 24 hours
        
        # Return minimal response with league_id
        response_data = {
            'league_id': assembly_id,
            'status': 'ready'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Assembly failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _get_cached_league(league_id, assembly_type):
    """Helper function to retrieve cached league object"""
    # Try both assembly types since leagues can be cached under either key
    for cache_type in [assembly_type, 'scoring', 'draft']:
        cache_key = f"league_{cache_type}_{league_id}"
        league = cache.get(cache_key)
        if league is not None:
            return league, None
    
    return None, {'error': f'League {league_id} not found or expired'}


@api_view(['GET'])
def expected_wins_analysis(request, league_id):
    """Get expected wins analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        chart_html = league.get_expected_wins_graph()
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'expected_wins',
                'chart_type': 'bar',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def ew_difference_analysis(request, league_id):
    """Get expected wins difference analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        ew_team_dic, chart_html = league.get_ew_difference_graph()
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'ew_difference',
                'chart_type': 'bar',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks,
                'summary': ew_team_dic
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def luck_analysis(request, league_id):
    """Get luck analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        luck_dic, chart_html = league.get_luck_graph()
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'luck',
                'chart_type': 'bar',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks,
                'summary': luck_dic
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def bonage_analysis(request, league_id):
    """Get bonage analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        chart_html = league.get_bonage_graph()
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'bonage',
                'chart_type': 'bar',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def consistency_analysis(request, league_id):
    """Get consistency analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        chart_html = league.get_consistency_graph()
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'consistency',
                'chart_type': 'scatter',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def probability_curve_analysis(request, league_id):
    """Get probability curve analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        chart_html = league.get_probdcurve()
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'probability_curve',
                'chart_type': 'line',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def sleepers_analysis(request, league_id):
    """Get sleepers analysis data"""
    try:
        league, error = _get_cached_league(league_id, 'draft')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        try:
            sleepers_dict = league.get_sleepers()
        except ValueError as e:
            return Response(
                {'error': str(e), 'solution': 'Call /process-draft/ endpoint first'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert Player objects to serializable data
        sleepers_data = []
        for position, player in sleepers_dict.items():
            sleepers_data.append([
                position,
                player.name if hasattr(player, 'name') else str(player)
            ])
        
        response_data = {
            'data': sleepers_data,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'sleepers',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def positional_ranks_analysis(request, league_id):
    """Get positional ranks analysis chart"""
    try:
        league, error = _get_cached_league(league_id, 'draft')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        try:
            chart_html = league.get_pos_rank_through_draft_graph()
        except ValueError as e:
            return Response(
                {'error': str(e), 'solution': 'Call /process-draft/ endpoint first'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_data = {
            'chart_html': chart_html,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'positional_ranks',
                'chart_type': 'line',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def draft_injury_analysis(request, league_id):
    """Get draft injury analysis data"""
    try:
        league, error = _get_cached_league(league_id, 'draft')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        try:
            draft_table_dict = league.get_draft_injury_table()
        except ValueError as e:
            return Response(
                {'error': str(e), 'solution': 'Call /process-draft/ endpoint first'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_data = {
            'data': draft_table_dict,
            'metadata': {
                'league_id': league_id,
                'analysis_type': 'draft_injury',
                'num_teams': len(league.teams),
                'num_weeks': league.num_weeks
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 
@api_view(['GET'])
def debug_league_info(request, league_id):
    """
    Debug endpoint to inspect cached league data.
    """
    try:
        # Try both scoring and draft cache keys
        for assembly_type in ['scoring', 'draft']:
            league, error = _get_cached_league(league_id, assembly_type)
            if league is not None:
                teams_info = {}
                for team_id, team in league.teams.items():
                    teams_info[str(team_id)] = {
                        "name": team.get_name(),
                        "has_scores": hasattr(team, "score_list") and team.score_list is not None,
                        "has_wins": hasattr(team, "win_list") and team.win_list is not None,
                        "has_ranks": hasattr(team, "rank_list") and team.rank_list is not None,
                        "score_count": len(getattr(team, "score_list", [])),
                        "win_count": len(getattr(team, "win_list", [])),
                        "rank_count": len(getattr(team, "rank_list", [])),
                    }
                
                return Response({
                    "num_teams": len(league.teams),
                    "num_weeks": league.num_weeks,
                    "assembly_type": assembly_type,
                    "teams": teams_info,
                })
        
        return Response(
            {"error": f"League {league_id} not found in cache."}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
    except Exception as e:
        return Response(
            {'error': f'Debug failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def process_draft_data(request, league_id):
    """
    Process draft data for an existing league.
    Requires the league to be already assembled.
    """
    try:
        # Try to get the league from cache using the helper function
        league, error = _get_cached_league(league_id, 'scoring')
        if error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        # Process draft data based on platform
        if league.platform == 'espn':
            league.process_draft_espn()
        elif league.platform == 'sleeper':
            league.process_draft_sleeper()
        else:
            return Response(
                {'error': f'Unsupported platform: {league.platform}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cache the updated league object with draft data
        cache_key = f"league_draft_{league_id}"
        cache.set(cache_key, league, timeout=86400)  # Cache for 24 hours
        
        return Response({
            'league_id': league_id,
            'status': 'draft_processed',
            'platform': league.platform
        })
        
    except Exception as e:
        return Response(
            {'error': f'Draft processing failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )