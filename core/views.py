import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from verify_email.email_handler import send_verification_email


from core.models import User
from ShopApp.models import Orders
from .serializers import UserSerializer

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from django.utils import timezone
from django.utils.timezone import timedelta

""" def validate(request, form):
    inactive_user = send_verification_email(request, form)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) """

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect

from django.views import View
from django.http import HttpResponse

class VerificationErrorView(View):
    def get(self, request):
        return HttpResponse("Email verification failed. Please try again or contact support.")


class EmailVerificationView(APIView):
    def get(self, request):
        User = get_user_model()
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Verify the user's email
            user.is_active = True
            user.save()

            # You can customize the redirect URL after successful verification
            return redirect('verification-success')  # Replace with your desired URL name or path
        else:
            # Handle the case of invalid or expired token
            return redirect('verification-error')  # Replace with your desired URL name or path


from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Generate token for email verification
        token = default_token_generator.make_token(user)

        # Encode user ID and token for email verification URL
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token_encoded = urlsafe_base64_encode(force_bytes(token))

        # Build email verification URL
        current_site = get_current_site(request)
        verify_url = reverse('verify-email')
        email_verification_url = f"{current_site}{verify_url}?uid={uid}&token={token_encoded}"

        # Construct email verification email content
        email_subject = 'Verify Your Email'
        email_body = f"Click the link below to verify your email:\n\n{email_verification_url}"

        # Send email verification email
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email='ys.maachou@gmail.com',
            recipient_list=[user.email],
            fail_silently=False
        )

        return Response({'message': 'Registration successful. Please check your email to verify your account.'})


    

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


