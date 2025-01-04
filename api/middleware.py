from .models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse

def auth_middleware(get_response):
    def middleware(request):
        unprotected_routes = ['/ping/', '/login/', '/signup/','/refresh/']
        owner_routes = ['/owner/create-user','/owner/set-flag']

        if request.path not in unprotected_routes:
            auth_header = request.headers.get('Authorization')

            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse(
                    {'error': 'Authentication required'}, 
                    status=401
                )
                
            try:
                token = auth_header.split(' ')[1]
                decoded_token = AccessToken(token)
                user = User.objects.filter(id=decoded_token['user_id']).first()
                
                if not user:
                    return JsonResponse(
                        {'error': 'User not found'}, 
                        status=404
                    )

                if request.path in owner_routes:
                    if user.role != "owner":
                        return JsonResponse({"error":"Not a owner trying to access owner routes"})

                request.info = user

            except Exception as e:
                return JsonResponse(
                    data={'error': 'Invalid token or token expired'}, 
                    status=401
                )

        response = get_response(request)
        return response

    return middleware