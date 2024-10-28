import random
import copy

class EstadoCoup:
    def __init__(self, jogadores):
        self.cartas = {jogador: ["Duque", "Capitão"] for jogador in jogadores}
        self.moedas = {jogador: 2 for jogador in jogadores}
        self.jogadores_ativos = jogadores.copy()
        self.acoes_recentes = {jogador: None for jogador in jogadores}
    
    def remover_carta(self, jogador):
        if jogador in self.jogadores_ativos and self.cartas[jogador]:
            carta_removida = self.cartas[jogador].pop()
            print(f"{jogador} perdeu a carta {carta_removida}!")
            if not self.cartas[jogador]:  # Jogador eliminado
                print(f"{jogador} foi eliminado!")
                self.jogadores_ativos.remove(jogador)
    
    def exibir_estado(self):
        print("\nEstado do jogo:")
        for jogador in self.jogadores_ativos:
            print(f"{jogador}: Cartas: {len(self.cartas[jogador])}, Moedas: {self.moedas[jogador]}")

def gerar_movimentos(estado, jogador):
    movimentos = ["Renda", "Ajuda Estrangeira"]
    if estado.moedas[jogador] >= 3:
        movimentos.append("Assassinato")
    if estado.moedas[jogador] >= 7:
        movimentos.append("Golpe")
    return movimentos

def funcao_utilidade(estado, jogador):
    valor_cartas = len(estado.cartas[jogador]) * 10
    valor_moedas = estado.moedas[jogador] * 2
    risco = -5 if estado.moedas[jogador] >= 7 else 0
    valor_acao = 3 if estado.acoes_recentes.get(jogador) in ["Assassinato", "Golpe"] else 0
    return valor_cartas + valor_moedas + risco + valor_acao

def funcao_avaliacao(estado, jogador):
    valor_cartas = len(estado.cartas[jogador]) * 10
    valor_moedas = estado.moedas[jogador] * 2
    risco = -5 if estado.moedas[jogador] >= 7 else 0
    valor_acao = 3 if estado.acoes_recentes.get(jogador) in ["Assassinato", "Golpe"] else 0
    return valor_cartas + valor_moedas + risco + valor_acao

def simular_jogada(estado, jogador, movimento):
    novo_estado = copy.deepcopy(estado)
    
    if movimento == "Renda":
        novo_estado.moedas[jogador] += 1
    elif movimento == "Ajuda Estrangeira":
        novo_estado.moedas[jogador] += 2
    elif movimento == "Assassinato" and novo_estado.moedas[jogador] >= 3:
        novo_estado.moedas[jogador] -= 3
    elif movimento == "Golpe" and novo_estado.moedas[jogador] >= 7:
        novo_estado.moedas[jogador] -= 7

    return novo_estado

def escolher_oponente(estado, jogador):
    oponentes = [j for j in estado.jogadores_ativos if j != jogador]
    return random.choice(oponentes)

def teste_terminal(estado):
    return len(estado.jogadores_ativos) == 1

def minimax(estado, jogador, profundidade, maximizando, alfa, beta):
    if profundidade == 0 or teste_terminal(estado):
        return funcao_avaliacao(estado, jogador)

    if maximizando:
        max_valor = float('-inf')
        for movimento in gerar_movimentos(estado, jogador):
            novo_estado = simular_jogada(estado, jogador, movimento)
            valor = minimax(novo_estado, jogador, profundidade - 1, False, alfa, beta)
            max_valor = max(max_valor, valor)
            alfa = max(alfa, valor)
            if beta <= alfa:
                break
        return max_valor
    else:
        min_valor = float('inf')
        oponente = escolher_oponente(estado, jogador)
        for movimento in gerar_movimentos(estado, oponente):
            novo_estado = simular_jogada(estado, oponente, movimento)
            valor = minimax(novo_estado, jogador, profundidade - 1, True, alfa, beta)
            min_valor = min(min_valor, valor)
            beta = min(beta, valor)
            if beta <= alfa:
                break
        return min_valor

def melhor_movimento(estado, jogador, profundidade=3):
    melhor_valor = float('-inf')
    melhor_movimento = None
    alfa, beta = float('-inf'), float('inf')
    
    for movimento in gerar_movimentos(estado, jogador):
        novo_estado = simular_jogada(estado, jogador, movimento)
        valor = minimax(novo_estado, jogador, profundidade - 1, False, alfa, beta)
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_movimento = movimento
    return melhor_movimento

def realizar_jogada(estado, jogador, movimento, alvo=None):
    if estado.moedas[jogador] >= 10:
        print(f"{jogador} possui 10 ou mais moedas e é obrigado a realizar um Golpe!")
        movimento = "Golpe"
        alvo = escolher_oponente(estado, jogador)

    print(f"\n{jogador} escolheu {movimento}.")
    estado.acoes_recentes[jogador] = movimento
    
    if movimento == "Renda":
        estado.moedas[jogador] += 1
    elif movimento == "Ajuda Estrangeira":
        estado.moedas[jogador] += 2
    elif movimento == "Assassinato" and alvo:
        if estado.moedas[jogador] >= 3:
            estado.moedas[jogador] -= 3
            estado.remover_carta(alvo)
    elif movimento == "Golpe" and alvo:
        if estado.moedas[jogador] >= 7:
            estado.moedas[jogador] -= 7
            estado.remover_carta(alvo)
    
    print(f"Utilidade de {jogador}: {funcao_utilidade(estado, jogador)}")
    print(f"Avaliação de {jogador}: {funcao_avaliacao(estado, jogador)}")

def main():
    jogadores = ["Jogador1", "IA"]
    estado = EstadoCoup(jogadores)
    turno = 0
    
    while len(estado.jogadores_ativos) > 1:
        estado.exibir_estado()
        jogador_atual = estado.jogadores_ativos[turno % len(estado.jogadores_ativos)]
        
        if jogador_atual == "IA":
            movimento = melhor_movimento(estado, "IA")
            alvo = escolher_oponente(estado, "IA") if movimento in ["Assassinato", "Golpe"] else None
        else:
            if estado.moedas[jogador_atual] >= 10:
                movimento = "Golpe"
                alvo = escolher_oponente(estado, jogador_atual)
                print(f"{jogador_atual} possui 10 ou mais moedas e é obrigado a realizar um Golpe!")
            else:
                movimentos = gerar_movimentos(estado, jogador_atual)
                print(f"\nAções disponíveis para {jogador_atual}: {', '.join(movimentos)}")
                movimento = input(f"{jogador_atual}, escolha sua ação: ")
                while movimento not in movimentos:
                    movimento = input("Ação inválida. Escolha novamente: ")
                alvo = None
                if movimento in ["Assassinato", "Golpe"]:
                    alvo = input("Escolha o alvo: ")
                    while alvo not in estado.jogadores_ativos or alvo == jogador_atual:
                        alvo = input("Alvo inválido. Escolha novamente: ")
        
        realizar_jogada(estado, jogador_atual, movimento, alvo)
        turno += 1
    
    print(f"\n{estado.jogadores_ativos[0]} é o vencedor!")

if __name__ == "__main__":
    main()
