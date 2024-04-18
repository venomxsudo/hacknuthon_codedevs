from tkinter import Image
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, VerifyAccountSerializer,ForgotPasswordSerializer, ResetPasswordSerializer,QuerySerializer
from rest_framework.response import Response
from .models import User,PendingUser
import jwt,datetime
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from rest_framework import status
import traceback
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from urllib.parse import unquote
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model 

User = get_user_model()

def error_404_view(request, exception):
    return render(request, 'users/404.html', status=404)


class RegisterView(APIView):
    def post(self, request):
        try:
            User = get_user_model()
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # user = serializer.save()
            user_data = serializer.validated_data
            pending_user = PendingUser.objects.create(name=user_data['name'], email=user_data['email'], phone=user_data['phonenumber'],password=user_data['password'])

            # Generate OTP and send email
            otp = get_random_string(length=6, allowed_chars='0123456789')
            pending_user.otp = otp
            pending_user.save()

            # Send OTP email
            subject = 'OTP Verification'
            message = render_to_string('registration/otp_email.html', {'otp': otp})
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [pending_user.email]
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = 'html' 
            email.send()

            if User.objects.filter(email=email).exists():
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Email already exists', 'data': None})
            redirect_url = 'http://127.0.0.1:8000/verify?email=' + pending_user.email
            return JsonResponse({'redirect_url': redirect_url})
            # return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            # return Response(serializer.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'An error occurred', 'data': None})
        


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        if user.is_active == False:
            raise AuthenticationFailed('Account disabled')
        if not user.is_verified:
            otp = get_random_string(length=6, allowed_chars='0123456789')
            user.otp = otp
            user.save()
            # Send OTP email
            subject = 'OTP Verification'
            message = render_to_string('registration/otp_email.html', {'otp': otp})
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = 'html' 
            email.send()
            redirect_url = 'http://127.0.0.1:8000/verify'  # Replace with your desired redirect URL
            return JsonResponse({'redirect_url': redirect_url})
            # raise AuthenticationFailed('Account not verified')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60000),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = HttpResponse()
        response.set_cookie('jwt', token, httponly=True)  # Set the 'jwt' cookie

        # Return a success response
        return response
        # Render the login.html template with the user's email and token
        # return render(request, 'login.html', {'email': email, 'token': token})


class DeleteUserView(APIView):
    def delete(self, request):
        user_id = request.data.get('id')
        try:
            user = PendingUser.objects.get(id=user_id)
            user.delete()
            return Response("User record deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        token = request.COOKIES.get('jwt')
        # return Response(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response


class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            pending_user = PendingUser.objects.filter(email=email, otp=otp).first()

            if not pending_user:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email',
                    'data': {}
                })

            # Check if more than 2 minutes have passed since the creation of the pending user
            if pending_user.created_at + timedelta(minutes=2) < timezone.now():
                pending_user.delete()
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Account verification expired. Please sign up again.',
                    'data': {}
                })

            user = User.objects.create_user(
                name=pending_user.name,
                email=pending_user.email,
                password=pending_user.password,
                first_name=pending_user.name,
                is_active=True,
                is_verified=True,
                otp='verified',
                is_staff=False,
                is_superuser=False,
                last_name='',
                phonenumber=pending_user.phone
            )
            user.save()
            pending_user.delete()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Account verified successfully',
                'data': {}
            })
            # ... Rest of the code
            # Update user's verification status, return response, etc.

        except Exception as e:
            print(e)
            traceback.print_exc()  # Print the exception traceback for debugging
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Something went wrong',
                'data': {}
            })
    
        

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = token_generator.make_token(user)
        reset_link = f'http://{get_current_site(request).domain}/reset' + f'?uidb64={uidb64}&token={token}'
        # reset_link = f"http://{get_current_site(request).domain}/reset-password/{user.id}/{token}"
        user.forgot_token = token
        user.save()
        subject = 'Forgot Password - Reset Link'
        message = render_to_string('registration/forgot_password_email.html', {
            'user': user,
            'reset_link': reset_link,
            'domain': get_current_site(request).domain,
        })
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.content_subtype = 'html' 
        email.send()
        response = HttpResponse()
        # return response
        return Response({'success':True,'message': 'Reset link sent successfully'})

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.query_params.get('token') # Extract token from query parameters
        print(token)
        new_password = serializer.validated_data['new_password']

        try:
            uidb64 = request.query_params.get('uidb64')  # Extract uidb64 from query parameters
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            print(user)
            print(user, user_id, uidb64, user)
            if user.forgot_token != token:
                raise AuthenticationFailed('Invalid reset token')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid reset token')

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise AuthenticationFailed('Invalid reset token')

        user.password = make_password(new_password)
        user.forgot_token = None
        user.save()

        return Response({'message': 'Password reset successful'})
    
# class QuerySubmission(APIView):
#     def post(self, request):
#         serializer = QuerySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'status': status.HTTP_201_CREATED,
#                 'message': 'Query submitted successfully',
#                 'data': serializer.data
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'Invalid data',
#                 'errors': serializer.errors
#             })

from rest_framework.parsers import MultiPartParser, FormParser

class QuerySubmission(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Query submitted successfully',
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data',
                'errors': serializer.errors
            })
            
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings
from sendfile import sendfile

@staff_member_required
def admin_images(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this directory.")

    # Construct the full file path
    file_path = settings.MEDIA_ROOT + '/query_photos/'

    # Use the sendfile package to serve the file
    return sendfile(request, file_path, attachment=True)

from django.views.generic import TemplateView
from .decorators import jwt_token_required

@jwt_token_required
def home_view(request):
    # Your view logic goes here
    return render(request, 'home.html')

'''
class VisitorListCreateView(generics.ListCreateAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

class QueryListCreateView(generics.ListCreateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    
class RegistrationCreateView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
'''

    
# class LoginView(APIView):
#     def post(self,request):
#         email = request.data['email']
#         password = request.data['password']
#         user = User.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed('User not found')
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password')
#         if user.is_active == False:
#             raise AuthenticationFailed('Account disabled')
#         if user.is_verified == False:
#             raise AuthenticationFailed('Account not verified')
        
#         payload = {
#             'id':user.id,
#             'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat':datetime.datetime.utcnow()
#         }
#         token = jwt.encode(payload,'secret',algorithm='HS256')
#         response = Response()
#         response.set_cookie(key='jwt',value=token,httponly=True)
#         response.data = {
#             'jwt':token
#         }
#         return response
