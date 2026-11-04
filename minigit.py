
class MiniGit:

    # Simula um histórico Git utilizando dicionários.
    # Todo o estado interno é privado.

    __slots__ = (
        "__pais",
        "__mensagens",
        "__branches",
        "__branch_atual",
        "__contador",
        "__passos"
    )

    def __init__(self):
        # Inicializa o repositório vazio na branch main.
        # Custo: 0 passos de operação pública.
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    def commitar(self, mensagem):
        # Cria um commit, registra seu pai e move a branch.
        # Custo: 2 passos.

        if not mensagem or not mensagem.strip():
            self.__passos = 0
            raise ValueError("A mensagem não pode ser vazia.")

        self.__contador += 1
        identificador = "c" + str(self.__contador)

        commit_anterior = self.__branches[self.__branch_atual]

        pais_do_commit = []

        if commit_anterior is not None:
            pais_do_commit.append(commit_anterior)

        self.__pais[identificador] = pais_do_commit
        self.__mensagens[identificador] = mensagem

        self.__branches[self.__branch_atual] = identificador

        self.__passos = 2

        return identificador

    def mensagem(self, commit):
        # Consulta diretamente a mensagem pelo identificador.
        # Custo: 1 passo.

        if commit not in self.__mensagens:
            self.__passos = 0
            raise ValueError("Commit não encontrado.")

        self.__passos = 1

        return self.__mensagens[commit]

    def pais(self, commit):
        # Devolve os pais como tupla, protegendo a lista interna.
        # Custo: 1 passo.

        if commit not in self.__pais:
            self.__passos = 0
            raise ValueError("Commit não encontrado.")

        self.__passos = 1

        return tuple(self.__pais[commit])

    @property
    def passos(self):
        # Permite consultar os passos sem alterar o valor.
        return self.__passos

    def criar_branch(self, nome):
        # Cria uma branch apontando para o commit atual.
        # Custo: 1 passo.

        if nome in self.__branches:
            self.__passos = 0
            raise ValueError("Essa branch já existe.")

        if self.__branches[self.__branch_atual] is None:
            self.__passos = 0
            raise ValueError("Ainda não existem commits.")

        self.__branches[nome] = self.__branches[self.__branch_atual]
        self.__passos = 1

    def trocar_branch(self, nome):
        # Seleciona uma branch existente.
        # Custo: 1 passo.

        if nome not in self.__branches:
            self.__passos = 0
            raise ValueError("Essa branch não existe.")

        self.__branch_atual = nome
        self.__passos = 1

    def mesclar(self, nome):
        # Cria um commit com dois pais.
        # Custo: 2 passos.

        if nome not in self.__branches:
            self.__passos = 0
            raise ValueError("Essa branch não existe.")

        if nome == self.__branch_atual:
            self.__passos = 0
            raise ValueError("Não é possível mesclar a própria branch.")

        primeiro_pai = self.__branches[self.__branch_atual]
        segundo_pai = self.__branches[nome]

        if primeiro_pai is None or segundo_pai is None:
            self.__passos = 0
            raise ValueError("As branches precisam possuir commits.")

        self.__contador += 1
        identificador = "c" + str(self.__contador)

        self.__pais[identificador] = [
            primeiro_pai,
            segundo_pai
        ]

        self.__mensagens[identificador] = "merge de " + nome

        self.__branches[self.__branch_atual] = identificador

        self.__passos = 2

        return identificador

    @property
    def branch_atual(self):
        # Informa qual branch está selecionada.
        return self.__branch_atual


# Teste da Parte 2

git = MiniGit()

git.commitar("primeiro commit")
git.commitar("segundo commit")

git.criar_branch("feature")
print(git.passos)

git.commitar("terceiro commit")

git.trocar_branch("feature")
git.commitar("quarto commit")

git.trocar_branch("main")
git.mesclar("feature")

print(git.pais("c5"))
print(git.mensagem("c5"))
