
from collections import deque


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
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    def commitar(self, mensagem):
        # Cria um commit e move a branch.
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
        # Consulta a mensagem pelo identificador.
        # Custo: 1 passo.

        if commit not in self.__mensagens:
            self.__passos = 0
            raise ValueError("Commit não encontrado.")

        self.__passos = 1

        return self.__mensagens[commit]

    def pais(self, commit):
        # Devolve os pais como tupla.
        # Custo: 1 passo.

        if commit not in self.__pais:
            self.__passos = 0
            raise ValueError("Commit não encontrado.")

        self.__passos = 1

        return tuple(self.__pais[commit])

    @property
    def passos(self):
        # Permite consultar a quantidade de passos.
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

    def log(self):
        # Percorre o histórico usando uma fila.
        # Cada commit aparece apenas uma vez.

        fila = deque()
        visitados = set()
        resultado = []

        commit_atual = self.__branches[self.__branch_atual]

        if commit_atual is not None:
            fila.append(commit_atual)

        while fila:
            commit = fila.popleft()

            if commit not in visitados:
                visitados.add(commit)
                resultado.append(commit)

                for pai in self.__pais[commit]:
                    fila.append(pai)

        self.__passos = len(resultado)

        return tuple(resultado)

    def buscar(self, texto):
        # Procura texto nas mensagens em ordem de criação.

        examinados = 0

        for commit in self.__mensagens:
            examinados += 1

            if texto in self.__mensagens[commit]:
                self.__passos = examinados
                return commit

        self.__passos = examinados

        return None

    def merges(self):
        # Retorna commits que possuem mais de um pai.

        resultado = []

        for commit in self.__pais:
            if len(self.__pais[commit]) > 1:
                resultado.append(commit)

        self.__passos = len(self.__pais)

        return tuple(resultado)


def tentar(acao):
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)

# Teste oficial do professor

git = MiniGit()

git.commitar("primeiro commit")
print(git.passos)

git.commitar("segundo commit")
git.criar_branch("feature")
print(git.passos)

git.commitar("terceiro commit")

git.trocar_branch("feature")
git.commitar("quarto commit")

git.trocar_branch("main")
git.mesclar("feature")

print(git.pais("c5"))
print(git.log(), git.passos)
print(git.mensagem("c3"), git.passos)
print(git.buscar("quarto"), git.passos)
print(git.merges())

git.trocar_branch("feature")
print(git.log(), git.passos)

git.trocar_branch("main")


# Testes que precisam apresentar erros

tentar(lambda: git.trocar_branch("inexistente"))
tentar(lambda: git.criar_branch("main"))
tentar(lambda: git.mesclar("main"))
tentar(lambda: git.pais("c99"))


def medir(quantidade):
    # Cria um repositório novo para realizar a medição.
    git_teste = MiniGit()

    # Cria a quantidade solicitada de commits.
    for numero in range(quantidade):
        git_teste.commitar("commit " + str(numero))

    # Guarda os passos gastos pelo último commitar.
    passos_commitar = git_teste.passos

    # Executa a leitura do histórico.
    git_teste.log()

    # Guarda os passos gastos pelo log.
    passos_log = git_teste.passos

    # Devolve os dois resultados.
    return passos_commitar, passos_log


# Tabela de comparação entre escrita e leitura.

print()
print("commits   passos do commitar   passos do log")

for quantidade in (10, 100, 1000):
    passos_commitar, passos_log = medir(quantidade)

    print(
        quantidade,
        "       ",
        passos_commitar,
        "                    ",
        passos_log
    )
