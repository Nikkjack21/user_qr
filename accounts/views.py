from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.serializer import AccountSerializer, LoginSerializer, shortenUrlSerialzier
from accounts.models import Accounts, ShortenURL
from accounts.utils import generate_short_url, generate_qr_code


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = Accounts.objects.get(email=serializer.data["email"])
                if user:
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {"access": str(refresh.access_token), "refresh": str(refresh)}
                    )
            except Accounts.DoesNotExist:
                return Response("User doesn't exist")


class LogoutView(TokenBlacklistView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serialzier = AccountSerializer(data=data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateURLView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        original_url = request.data.get("url", None)
        if not original_url:
            return Response({"url": "Please provide an URL to be shortened"})
        token, short_url = generate_short_url()
        qr_code_img = generate_qr_code(url=short_url)
        instance = ShortenURL.objects.create(
            user=request.user,
            original_url=original_url,
            shorten_url=short_url,
            token=token,
            qr_image=qr_code_img,
        )

        serializer = shortenUrlSerialzier(instance)
        if serializer:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ListURLView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        urls = ShortenURL.objects.filter(user=request.user)
        serialzier = shortenUrlSerialzier(urls, many=True, context={"request": request})
        return Response(serialzier.data)


class DeleteURLView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = shortenUrlSerialzier
    queryset = ShortenURL.objects.all()


class UpdateURLView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = request.data
        url_instance = ShortenURL.objects.get(id=pk, user=request.user)
        serializer = shortenUrlSerialzier(url_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLView(APIView):
    def get(self, request, short_url):
        print(short_url)
        url_instance = ShortenURL.objects.get(token=short_url)
        if url_instance:
            count = url_instance.visited_count
            count += 1
            url_instance.visited_count = count
            url_instance.save()
            return redirect(url_instance.original_url)
        return Response({"error": "soemthing went wrong"}, status=400)
