from django import forms
from apps.login.models import Usuario, Filial, Nivelvendedor

class UsuarioForm(forms.ModelForm):

    # Campo DropDown com dados de outra tabela (Nesse caso, tabela de filiais)
    filial = forms.ModelChoiceField(
        label='Filial',                                 # Que descrição estara ao lado do campo no front-end
        queryset=Filial.objects.all(),                  # Dados que vai constar no campo utilizando a ORM do Django
        widget=forms.Select(
            attrs={                                     # Aqui podemos colocar um dicionário de dados contento atributos para mandar para o front-end
                "class": "form-control"                 # Atributo "class" contendo a classe "form-control"
            }
        ),
        required=False                                  # Preenchimento não obrigatório
    )

    # Campo DropDown com dados de outra tabela (Nesse caso, tabela de nivel de vendedor)
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
        model = Usuario                 # Nesse caso, Usuario é a instancia do modelo que vem do arquivo models.py que foi configurado em Prog1/apps/login
        exclude = ['codusuario']        # Campos que não irão constar no formulário

        labels = {                      # Dicionário de dados contento: "NomeDoCampo":"Descrição do campo que vai aparecer no front-end"
            'nome':'Nome',
            'cpf':'CPF',
            'login':'Login no Sistema',
            'senha':'Senha no Sistema',
            'tipo':'Cargo',
            'dtinclusao': 'Data de Inclusão',
            'dtencerramento': 'Data de Encerramento',
            'status': 'Status'
        }

        # Configurando cada campo do formulário, Atenção: o nome do campo deve ser idêntico ao models.py
        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control'}),                                        # Campo de Texto nome
            'cpf': forms.TextInput(attrs={'class':'form-control'}),                                         # Campo de Texto CPF
            'login': forms.TextInput(attrs={'class':'form-control'}),                                       # Campo de Texto Login
            'senha': forms.PasswordInput(attrs={'class':'form-control'}),                                   # Campo de Senha
            'tipo': forms.Select(attrs={'class':'form-control'}),                                           # Campo DropDown de Tipo (As opções nesse caso são criadas dentro do models.py)
            'dtinclusao': forms.TextInput(attrs={'class':'form-control', 'readonly':True}),                 # Campo de Texto somente para visualização
            'dtencerramento': forms.TextInput(attrs={'class':'form-control', 'readonly':True}),             # Campo de Texto somente para visualização
            'status': forms.Select(attrs={'class':'form-control'})                                          # Campo DropDown de Tipo (As opções nesse caso são criadas dentro do models.py)
        }
