import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response


from core.models import User
from ShopApp.models import Orders
from .serializers import UserSerializer

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from django.utils import timezone
from django.utils.timezone import timedelta
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    

class LoginView(APIView):
    def post(self, request):
        email = request.data['email'] 
        password = request.data['password']   

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found !')
        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password !')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=48),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.data = {
            'jwt': token
        }
        
        response['Authorization'] = f'Bearer {token}'
        
        return response

class UserView(APIView):
    def get(self, request):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated !')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated !')    

        user = User.objects.filter(id=payload['id'])
        serializer = UserSerializer(user, many=True)

        total_amount_for_month = Orders.objects.filter(user=user, created_at__gte=timezone.now()-timezone.timedelta(days=30)).aggregate(sum('total'))['total__sum'] or 0

        if total_amount_for_month >= 50000:
            serializer.instance.membership = User.MEMBERSHIP_GOLD
        elif total_amount_for_month >= 30000:
            serializer.instance.membership = User.MEMBERSHIP_SILVER
        elif total_amount_for_month >= 10000:
            serializer.instance.membership = User.MEMBERSHIP_BRONZE

        # Calculate total amount from orders
        total_amount = Orders.objects.filter(user=user).aggregate(sum('total'))['total__sum'] or 0

        # Calculate points based on total_amount
        points = total_amount // 100

        # Update user's points
        user.points += points
        user.save()    
    
        serializer.save()
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logged out.'
        }  
        return response  


