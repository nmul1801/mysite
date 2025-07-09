from django.shortcuts import render
from django.http import HttpResponse
from .league.league import League


def index(request):
    return render(request, 'analysis/index.html')


def analysis(request):
    return render(request, 'analysis/analysis.html')


def progress_demo(request):
    """Serve the progress demo page"""
    return render(request, 'analysis/progress_demo.html')

