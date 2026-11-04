# MiniGit — Estrutura de Dados

## Medição: leitura x escrita

| Quantidade de commits | Passos do commitar | Passos do log |
|---:|---:|---:|
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## Respostas

**1. Por que o commitar gasta sempre 2 passos, e o log gasta mais conforme o histórico cresce?**

O método `commitar()` sempre realiza duas ações: cria o commit e atualiza o ponteiro da branch. Já o `log()` precisa percorrer os commits existentes, por isso utiliza mais passos quando o histórico aumenta.

**2. Por que mensagem(commit) gasta 1 passo e buscar(texto) pode gastar muitos?**

O método `mensagem()` encontra diretamente o commit usando seu identificador como chave no dicionário. Já `buscar()` precisa comparar o texto com as mensagens armazenadas, podendo verificar vários commits até encontrar o que procura.

**3. Por que o merge é um commit com dois pais, e por que isso faz do histórico um grafo, e não uma lista?**

O merge reúne o histórico de duas branches em um novo commit, que guarda os dois commits anteriores como pais. Assim, um commit pode estar ligado a mais de um caminho, formando uma estrutura de grafo em vez de uma sequência única.

**4. Por que o método pais devolve uma tupla, e não a lista que está guardada dentro do dicionário?**

A tupla impede que quem utiliza o método altere diretamente a lista de pais armazenada internamente. Dessa forma, o histórico fica mais protegido contra modificações feitas fora da classe.
