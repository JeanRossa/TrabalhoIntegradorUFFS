from django import forms
from apps.login.models import Usuario, Filial, Nivelvendedor, Localidade, Filial, Nivelfilial


class FilialForm(forms.ModelForm):

    codlocal = forms.ModelChoiceField(label='Localidade', queryset=Localidade.objects.all(
    ), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    nivelfilial = forms.ModelChoiceField(label='Nivel da Filial', queryset=Nivelfilial.objects.all(
    ), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        # Nesse caso, Usuario é a instancia do modelo que vem do arquivo models.py que foi configurado em Prog1/apps/login
        model = Filial
        # Campos que não irão constar no formulário
        exclude = ['codfilial']

        # Dicionário de dados contento: "NomeDoCampo":"Descrição do campo que vai aparecer no front-end"

        labels = {
            'cnpj': 'CNPJ',
            'dtinclusao': 'Data de Inclusão',
            'dtencerramento': 'Data de Encerramento',
            'status': 'Status'
        }

        # Configurando cada campo do formulário, Atenção: o nome do campo deve ser idêntico ao models.py
        widgets = {
            # Campo de Texto CNPJ
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'dtinclusao': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'dtencerramento': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class NivelFilialForm(forms.ModelForm):

    class Meta:
        model = Nivelfilial

        fields = ['nivelfilial', 'descricao']

        labels = {
            'nivelfilial': 'Nível Filial',
            'descricao': 'Descrição',
        }

        widgets = {
            'nivelfilial': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LocalidadeForm(forms.ModelForm):

    class Meta:
        # Nesse caso, Usuario é a instancia do modelo que vem do arquivo models.py que foi configurado em Prog1/apps/login
        model = Localidade
        # Campos que não irão constar no formulário
        exclude = ['codlocal']

        # Dicionário de dados contento: "NomeDoCampo":"Descrição do campo que vai aparecer no front-end"

        labels = {
            'cidade': 'Cidade',
            'estado': 'Estado',
        }

        # Configurando cada campo do formulário, Atenção: o nome do campo deve ser idêntico ao models.py
        widgets = {
            # Campo de Texto nome
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            # Campo de Texto nome
            'estado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecione o estado'}),
        }


class UsuarioForm(forms.ModelForm):

    # Campo DropDown com dados de outra tabela (Nesse caso, tabela de filiais)
    filial = forms.ModelChoiceField(
        # Que descrição estara ao lado do campo no front-end
        label='Filial',
        # Dados que vai constar no campo utilizando a ORM do Django
        queryset=Filial.objects.all(),
        widget=forms.Select(
            attrs={
                # Aqui podemos colocar um dicionário de dados contento atributos para mandar para o front-end
                # Atributo "class" contendo a classe "form-control"
                "class": "form-control"
            }
        ),
        required=False                                  # Preenchimento não obrigatório
    )

    # Campo DropDown com dados de outra tabela (Nesse caso, tabela de nivel de vendedor)
    nivelvendedor = forms.ModelChoiceField(label='Nivel do Vendedor', queryset=Nivelvendedor.objects.all(
    ), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        # Nesse caso, Usuario é a instancia do modelo que vem do arquivo models.py que foi configurado em Prog1/apps/login
        model = Usuario
        # Campos que não irão constar no formulário
        exclude = ['codusuario']

        labels = {                      # Dicionário de dados contento: "NomeDoCampo":"Descrição do campo que vai aparecer no front-end"
            'nome': 'Nome',
            'cpf': 'CPF',
            'login': 'Login no Sistema',
            'senha': 'Senha no Sistema',
            'tipo': 'Cargo',
            'dtinclusao': 'Data de Inclusão',
            'dtencerramento': 'Data de Encerramento',
            'status': 'Status'
        }

        # Configurando cada campo do formulário, Atenção: o nome do campo deve ser idêntico ao models.py
        widgets = {
            # Campo de Texto nome
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            # Campo de Texto CPF
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            # Campo de Texto Login
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            # Campo de Senha
            'senha': forms.PasswordInput(attrs={'class': 'form-control'}),
            # Campo DropDown de Tipo (As opções nesse caso são criadas dentro do models.py)
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            # Campo de Texto somente para visualização
            'dtinclusao': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            # Campo de Texto somente para visualização
            'dtencerramento': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            # Campo DropDown de Tipo (As opções nesse caso são criadas dentro do models.py)
            'status': forms.Select(attrs={'class': 'form-control'})
        }
