# middleware.py - Create this file in your app directory

class NoCacheMiddleware:
    """
    Middleware to prevent caching of authenticated user pages
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only add no-cache headers for authenticated users and non-static files
        if (request.user.is_authenticated and 
            not request.path.startswith('/static/') and 
            not request.path.startswith('/media/')):
            
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
        return response