from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Author
        fields = ['id', 'username', 'password', 'full_name', 'description', 'active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'active']

    def validate(self, data):
        # Only require password for POST (create)
        if not self.instance and 'password' not in data:
            raise serializers.ValidationError({"password": "This field is required for registration / Это поле обязательно для регистрации"})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        author = Author(**validated_data)
        if password:
            author.set_password(password)
        author.save()
        return author

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class AuthorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
