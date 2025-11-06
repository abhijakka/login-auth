from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

User = get_user_model()

# ✅ REGISTER (function based)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email    = request.data.get("email")
    password = request.data.get("password")

    if not (username and email and password):
        return Response({"detail": "username, email, password required"}, status=400)

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return Response({"detail": "User already exists"}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    refresh = RefreshToken.for_user(user)
    return Response({
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


# ✅ CUSTOM LOGIN (function based)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get("identifier")  # email or username
    password   = request.data.get("password")

    if not identifier or not password:
        return Response({"detail": "identifier & password required"}, status=400)

    # Try email → username
    try:
        user_obj = User.objects.get(email=identifier)
        username = user_obj.username
    except User.DoesNotExist:
        username = identifier

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })


