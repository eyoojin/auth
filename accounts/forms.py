from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        # fields = '__all__'
        fields = ('username', )
        # password는 필수