from django.http import JsonResponse

def handler404(request, exception=None):
    return JsonResponse({'error': 'Not Found', 'status_code': 404}, status=404)

def handler500(request):
    return JsonResponse({'error': 'Internal Server Error', 'status_code': 500}, status=500)

def handler403(request, exception=None):
    return JsonResponse({'error': 'Permission Denied', 'status_code': 403}, status=403)

def handler400(request, exception=None):
    return JsonResponse({'error': 'Bad Request', 'status_code': 400}, status=400)
