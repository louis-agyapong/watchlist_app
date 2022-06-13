from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirmation")
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data["password"]
        password_confirmation = self.validated_data["password_confirmation"]

        if password != password_confirmation:
            raise serializers.ValidationError({"error": "Passwords do not match"})

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        user = User(email=self.validated_data["email"], username=self.validated_data["username"])
        user.set_password(password)
        user.save()
        return user
