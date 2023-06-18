from django import forms

class LoginForms(forms.Form):
    nome_login=forms.CharField(
        label="Login",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg"
            }
        )
    )
    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg"
            }
        )
    )