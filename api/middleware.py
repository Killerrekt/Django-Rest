from .models import User
from rest_framework_simplejwt.tokens import AccessToken

def auth_middleware(get_response):
    def middleware(request):
        unprotected_routes = ['/ping/', '/login/','/signup/']
        
        if request.path not in unprotected_routes:
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return response(
                    {'error': 'Authentication required'}, 
                    status=401
                )
                
            try:
                token = auth_header.split(' ')[1]
                decoded_token = AccessToken(token)
                print(decoded_token['user_id'])
                user = User.objects.filter(id=decoded_token['user_id']).first()
                print(user.email)
                if not user:
                    return response(
                        {'error': 'User not found'}, 
                        status=404
                    )
                    
                request.info = user
                
            except Exception as e:
                return response(
                    {'error': 'Invalid token'}, 
                    status=401
                )
                
        response = get_response(request)
        return response
        
    return middleware