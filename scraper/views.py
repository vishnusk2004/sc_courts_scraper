from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import json
import logging

from .models import ScrapingSession, CourtRecord
from .scraper_service import SCCourtsScraperService

logger = logging.getLogger(__name__)

def home(request):
    """Home page with scraping interface"""
    try:
        # Get recent sessions
        recent_sessions = ScrapingSession.objects.all()[:5]
        
        context = {
            'recent_sessions': recent_sessions,
            'total_sessions': ScrapingSession.objects.count(),
            'successful_sessions': ScrapingSession.objects.filter(status='success').count(),
        }
    except Exception as e:
        # Handle database not ready
        context = {
            'recent_sessions': [],
            'total_sessions': 0,
            'successful_sessions': 0,
        }
    
    return render(request, 'scraper/home.html', context)

def start_scraping(request):
    """Start a new scraping session"""
    if request.method == 'POST':
        try:
            scraper_service = SCCourtsScraperService()
            session, success = scraper_service.run_scraping()
            
            if success:
                messages.success(request, f'Scraping completed successfully! Session ID: {session.session_id}')
                return redirect('session_detail', session_id=session.session_id)
            else:
                messages.error(request, f'Scraping failed: {session.error_message}')
                return redirect('session_detail', session_id=session.session_id)
                
        except Exception as e:
            logger.error(f"Error starting scraping: {e}")
            messages.error(request, f'Error starting scraping: {str(e)}')
            return redirect('home')
    
    return redirect('home')

def session_detail(request, session_id):
    """View details of a specific scraping session"""
    try:
        session = ScrapingSession.objects.get(session_id=session_id)
        records = session.records.all()
        
        context = {
            'session': session,
            'records': records,
        }
        
        return render(request, 'scraper/session_detail.html', context)
        
    except ScrapingSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('home')

def sessions_list(request):
    """List all scraping sessions"""
    try:
        sessions = ScrapingSession.objects.all()
        
        # Search functionality
        search = request.GET.get('search', '')
        if search:
            sessions = sessions.filter(
                Q(session_id__icontains=search) |
                Q(status__icontains=search) |
                Q(error_message__icontains=search)
            )
        
        # Status filter
        status_filter = request.GET.get('status', '')
        if status_filter:
            sessions = sessions.filter(status=status_filter)
        
        # Pagination
        paginator = Paginator(sessions, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'search': search,
            'status_filter': status_filter,
            'status_choices': ScrapingSession.STATUS_CHOICES,
        }
    except Exception as e:
        # Handle database not ready
        context = {
            'page_obj': None,
            'search': '',
            'status_filter': '',
            'status_choices': ScrapingSession.STATUS_CHOICES,
        }
    
    return render(request, 'scraper/sessions_list.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def api_start_scraping(request):
    """API endpoint to start scraping"""
    try:
        scraper_service = SCCourtsScraperService()
        session, success = scraper_service.run_scraping()
        
        return JsonResponse({
            'success': success,
            'session_id': session.session_id,
            'status': session.status,
            'message': 'Scraping started' if success else session.error_message
        })
        
    except Exception as e:
        logger.error(f"API scraping error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def api_session_status(request, session_id):
    """API endpoint to get session status"""
    try:
        session = ScrapingSession.objects.get(session_id=session_id)
        
        return JsonResponse({
            'session_id': session.session_id,
            'status': session.status,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'ip_address': session.ip_address,
            'forms_count': session.forms_count,
            'inputs_count': session.inputs_count,
            'selects_count': session.selects_count,
            'links_count': session.links_count,
            'scripts_count': session.scripts_count,
            'error_message': session.error_message,
        })
        
    except ScrapingSession.DoesNotExist:
        return JsonResponse({
            'error': 'Session not found'
        }, status=404)

@csrf_exempt
@require_http_methods(["GET"])
def api_session_data(request, session_id):
    """API endpoint to get session data"""
    try:
        session = ScrapingSession.objects.get(session_id=session_id)
        
        if session.status != 'success':
            return JsonResponse({
                'error': 'Session not successful'
            }, status=400)
        
        return JsonResponse({
            'session_id': session.session_id,
            'status': session.status,
            'parsed_data': session.parsed_data,
            'forms_count': session.forms_count,
            'inputs_count': session.inputs_count,
            'selects_count': session.selects_count,
            'links_count': session.links_count,
            'scripts_count': session.scripts_count,
        })
        
    except ScrapingSession.DoesNotExist:
        return JsonResponse({
            'error': 'Session not found'
        }, status=404)

def dashboard(request):
    """Dashboard with statistics"""
    try:
        total_sessions = ScrapingSession.objects.count()
        successful_sessions = ScrapingSession.objects.filter(status='success').count()
        failed_sessions = ScrapingSession.objects.filter(status='failed').count()
        blocked_sessions = ScrapingSession.objects.filter(status='blocked').count()
        
        # Recent sessions
        recent_sessions = ScrapingSession.objects.all()[:10]
        
        context = {
            'total_sessions': total_sessions,
            'successful_sessions': successful_sessions,
            'failed_sessions': failed_sessions,
            'blocked_sessions': blocked_sessions,
            'recent_sessions': recent_sessions,
        }
    except Exception as e:
        # Handle database not ready
        context = {
            'total_sessions': 0,
            'successful_sessions': 0,
            'failed_sessions': 0,
            'blocked_sessions': 0,
            'recent_sessions': [],
        }
    
    return render(request, 'scraper/dashboard.html', context)