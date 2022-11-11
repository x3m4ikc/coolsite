"""Modules for captcha, forms"""
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import CharField, EmailField
from django.forms.models import ModelForm
from django.forms.widgets import EmailInput, PasswordInput, Textarea, TextInput

from .models import Women


class AddPostForm(ModelForm):
    """Creates form for posts"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta-options to add post"""

        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat"]
        widgets = {
            "title": TextInput(attrs={"class": "form-input"}),
            "slug": TextInput(attrs={"class": "form-input"}),
            "content": Textarea(attrs={"cols": 60, "rows": 10}),
        }

    def validate_title(self):
        """Validator password"""
        if self.cleaned_data["title"] and len(self.cleaned_data["title"]) <= 200:
            return True
        return False

    def clean_title(self) -> dict:
        """Checks string for lenght"""
        if not self.validate_title():
            raise ValidationError("Длина превышает 200 символом")
        return self.cleaned_data["title"]


class RegisterUserForm(UserCreationForm):
    """Registration form"""

    username = CharField(label="Логин", widget=TextInput(attrs={"class": "form-input"}))
    email = EmailField(label="Email", widget=EmailInput(attrs={"class": "form-input"}))
    password1 = CharField(
        label="Пароль", widget=PasswordInput(attrs={"class": "form-input"})
    )
    password2 = CharField(
        label="Повтор пароля", widget=PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta-options for registration"""

        model = User
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    """Login form"""

    username = CharField(label="Логин", widget=TextInput(attrs={"class": "form-input"}))
    password = CharField(
        label="Пароль", widget=PasswordInput(attrs={"class": "form-input"})
    )


class ContactForm(Form):
    """Feed-back form"""

    name = CharField(label="Имя", max_length=255)
    email = EmailField(label="Email")
    content = CharField(widget=Textarea(attrs={"cpls": 60, "rows": 10}))
    captcha = CaptchaField()
