from django.conf import UserSettingsHolder
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Course, Enrollment, Assignment, Sponsorship, Notification
from django.contrib.auth import authenticate

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import RegexValidator

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class SponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsorship
        fields = '__all__'

# base/serializers.py
from rest_framework import serializers
from base.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    




'''class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
            )
        ],
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
   
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Required.'
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        email = attrs.get('email')

        if username and password and email:
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "username": ["Invalid username or email."],
                    "email": ["Invalid username or email."],
                    "password": ["Invalid password."]
                })
            
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError({
                    "username": ["Invalid username or email."],
                    "email": ["Invalid username or email."],
                    "password": ["Invalid password."]
                })
            attrs['user'] = user
        return attrs'''


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import RegexValidator

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
            )
        ],
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
   
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Required.'
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({
                "username": ["Invalid username."],
                "password": ["Invalid password."]
            })

        # Add the user object to validated_data for the view
        attrs['user'] = user
        return attrs






# serializers.py
from rest_framework import serializers

class AdminDashboardSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_enrollments = serializers.IntegerField()

class StudentDashboardSerializer(serializers.Serializer):
    enrolled_courses = serializers.IntegerField()
    completed_assignments = serializers.IntegerField()
    message = serializers.CharField()




# base/serializers.py
from rest_framework import serializers

class EmailSendSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        help_text="List of recipient emails"
    )
