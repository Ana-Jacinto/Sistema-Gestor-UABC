from django.shortcuts import redirect

class ClearSessionOnNavigationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Clear session if the user navigates away from add_item
        if request.session.get('has_access') and request.path != '/contenido/agregar' and response.status_code == 200:
            request.session['has_access'] = False
        return response