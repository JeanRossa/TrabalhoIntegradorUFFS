from django import forms
from apps.login.models import Usuario, Filial, Nivelvendedor

class UsuarioForm(forms.ModelForm):

    filial = forms.ModelChoiceField(
        label='Filial',
        queryset=Filial.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ),
        required=False
    )

    nivelvendedor = forms.ModelChoiceField(
        label='Nivel do Vendedor',
        queryset=Nivelvendedor.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ),
        required=False
    )

    class Meta:
        model = Usuario
        exclude = ['codusuario','dtinclusao','dtencerramento','status']
        
        labels = {
            'nome':'Nome',
            'cpf':'CPF',
            'login':'Login no Sistema',
            'senha':'Senha no Sistema',
            'tipo':'Cargo',
        }

        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'cpf': forms.TextInput(attrs={'class':'form-control'}),
            'login': forms.TextInput(attrs={'class':'form-control'}),
            'senha': forms.PasswordInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
        }
