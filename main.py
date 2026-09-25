from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Dict, Tuple

class ItemEstoque(ABC):
    @abstractmethod
    def quantidade_total(self) -> int:
        pass

    @abstractmethod
    def dar_baixa(self, quantidade: int) -> bool:
        pass

class Lote:
    def __init__(self, numero_lote: str, data_validade: date, quantidade: int):
        self._numero_lote = numero_lote
        self._data_validade = data_validade
        self.quantidade = quantidade 

    @property
    def numero_lote(self) -> str:
        return self._numero_lote

    @property
    def data_validade(self) -> date:
        return self._data_validade

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("Encapsulamento: A quantidade do lote não pode ser negativa.")
        self._quantidade = valor

    def dias_para_vencer(self, data_ref: date = None) -> int:
        hoje = data_ref or date.today()
        return (self._data_validade - hoje).days

    @property
    def esta_vencido(self) -> bool:
        return self.dias_para_vencer() < 0

class Produto(ItemEstoque):
    def __init__(self, codigo: str, nome: str):
        self._codigo = codigo
        self._nome = nome
        self._lotes: List[Lote] = []

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def lotes(self) -> List[Lote]:
        return list(self._lotes)

    def adicionar_lote(self, lote: Lote) -> None:
        if not isinstance(lote, Lote):
            raise TypeError("Apenas objetos da classe Lote podem ser adicionados.")
        self._lotes.append(lote)

    def quantidade_total(self) -> int:
        return sum(l.quantidade for l in self._lotes if not l.esta_vencido)

    def dar_baixa(self, quantidade: int) -> bool:
        if quantidade <= 0:
            raise ValueError("A quantidade de baixa deve ser maior que zero.")

        if self.quantidade_total() < quantidade:
            raise ValueError(f"Estoque insuficiente no produto '{self._nome}'.")

        quantidade_restante = quantidade

        lotes_validos = sorted(
            [l for l in self._lotes if not l.esta_vencido and l.quantidade > 0],
            key=lambda l: l.data_validade
        )

        for lote in lotes_validos:
            if quantidade_restante <= 0:
                break
            
            baixa = min(lote.quantidade, quantidade_restante)
            lote.quantidade -= baixa
            quantidade_restante -= baixa

        return True

class GestorEstoque:
    def __init__(self):
        self._produtos: Dict[str, Produto] = {}

    def cadastrar_produto(self, produto: Produto) -> None:
        if produto.codigo in self._produtos:
            raise ValueError(f"Produto '{produto.codigo}' já cadastrado.")
        self._produtos[produto.codigo] = produto

    def realizar_baixa(self, codigo_produto: str, quantidade: int) -> bool:
        if codigo_produto not in self._produtos:
            raise ValueError("Produto não encontrado no sistema.")
        return self._produtos[codigo_produto].dar_baixa(quantidade)

    def gerar_alerta_vencimento(self, dias_limite: int = 30) -> List[Tuple[str, str, int]]:
        alertas = []
        for produto in self._produtos.values():
            for lote in produto.lotes:
                dias = lote.dias_para_vencer()
                if 0 <= dias <= dias_limite and lote.quantidade > 0:
                    alertas.append((produto.nome, lote.numero_lote, dias))
        return alertas

if __name__ == "__main__":
    print("==================================================")
    print("     MEDCONTROL - SISTEMA DE GESTÃO DE ESTOQUE    ")
    print("==================================================\n")

    gestor = GestorEstoque()

    remedio = Produto(codigo="MED100", nome="Amoxicilina 500mg")

    lote_a = Lote(numero_lote="LOTE_A", data_validade=date.today() + timedelta(days=10), quantidade=15)
    lote_b = Lote(numero_lote="LOTE_B", data_validade=date.today() + timedelta(days=60), quantidade=40)

    remedio.adicionar_lote(lote_a)
    remedio.adicionar_lote(lote_b)
    gestor.cadastrar_produto(remedio)

    print(f" Produto cadastrado: {remedio.nome}")
    print(f" Quantidade total válida: {remedio.quantidade_total()} unidades")

    print("\n--- Testando Encapsulamento (Validação do Setter) ---")
    try:
        lote_a.quantidade = -10
    except ValueError as e:
        print(f" Bloqueado com sucesso: {e}")

    print("\n--- Alertas de Vencimento (Próximos 15 dias) ---")
    for prod, lote, dias in gestor.gerar_alerta_vencimento(dias_limite=15):
        print(f"  ATENÇÃO: '{prod}' (Lote: {lote}) vence em {dias} dia(s)!")

    print("\n--- Executando Baixa de 20 Unidades (Algoritmo FEFO) ---")
    gestor.realizar_baixa("MED100", 20)

    print(f"• Quantidade restante no Lote A (que vencia primeiro): {lote_a.quantidade} un")
    print(f"• Quantidade restante no Lote B (que vence depois): {lote_b.quantidade} un")
    print(f"• Total atualizado em estoque: {remedio.quantidade_total()} un")
    print("\n")
