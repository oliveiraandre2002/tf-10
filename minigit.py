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
        # Custo: 2 passos (criar commit + mover ponteiro).

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

git = MiniGit()

print(git.commitar("primeiro commit"))
print(git.passos)

print(git.commitar("segundo commit"))
print(git.passos)

print(git.mensagem("c1"))
print(git.passos)

print(git.pais("c2"))
print(git.passos)

print(git.pais("c1"))
