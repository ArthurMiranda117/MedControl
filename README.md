# MedControl – Sistema de Gestão de Validade e Estoque Medicamentoso

O **MedControl** é um sistema em Python desenvolvido para resolver o problema real do desperdício de medicamentos e insumos médicos em farmácias, postos de saúde e hospitais. A aplicação automatiza a regra **FEFO** (*First Expired, First Out* — Primeiro que Vence, Primeiro que Sai) e emite alertas preventivos de vencimento.

---

##  Sumário
- [Justificativa e Problema Real](#-justificativa-e-problema-real)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Conceitos de POO Aplicados](#-conceitos-de-poo-aplicados)
- [Diagrama de Classes](#-diagrama-de-classes)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Executar](#-como-executar)
- [Tecnologias e Bibliotecas](#-tecnologias-e-bibliotecas)
- [Distribuição das Tarefas](#-distribuição-das-tarefas)

---

## Justificativa e Problema Real

O descarte de medicamentos por perda de validade gera grandes prejuízos financeiros e risco de desabastecimento de itens essenciais na saúde pública e privada. O **MedControl** atua diretamente na prevenção desse problema, ordenando a saída dos lotes com expiração mais próxima e fornecendo alertas configuráveis para a gestão tomar decisões antes do vencimento.

---

## Funcionalidades Principais

- **Gestão Multilote:** Vinculação de múltiplos lotes com validades distintas a um mesmo medicamento.
- **Baixa Automática por FEFO:** Consumo prioritário dos lotes mais próximos do vencimento.
- **Alertas de Vencimento:** Filtro configurável de itens que vencerão em uma janela determinada de dias.
- **Integridade do Estoque:** Bloqueio automático de tentativas de atribuição de saldo negativo ou saídas sem estoque suficiente.

---

## 🧬 Conceitos de POO Aplicados

- **Abstração (`ItemEstoque`):** Uso de classe abstrata com o módulo `abc` para definir o contrato obrigatório (`quantidade_total` e `dar_baixa`) de qualquer item armazenado.
- **Encapsulamento (`Lote` e `Produto`):** Atributos protegidos/privados (`_codigo`, `_nome`, `_quantidade`) expostos apenas via `@property`. Uso de `@property.setter` para validar regras de negócio e evitar estado inconsistente.
- **Herança e Polimorfismo:** A classe `Produto` herda de `ItemEstoque` e implementa seus métodos abstratos. O `GestorEstoque` interage com objetos através da interface abstrata, sem necessidade de conhecer a estrutura interna de lotes.

---

## Diagrama de Classes

```mermaid
classDiagram
    class ItemEstoque {
        <<abstract>>
        +quantidade_total()* int
        +dar_baixa(quantidade: int)* bool
    }

    class Lote {
        -str _numero_lote
        -date _data_validade
        -int _quantidade
        +numero_lote str
        +data_validade date
        +quantidade int
        +dias_para_vencer() int
        +esta_vencido bool
    }

    class Produto {
        -str _codigo
        -str _nome
        -list~Lote~ _lotes
        +codigo str
        +nome str
        +lotes list~Lote~
        +adicionar_lote(lote: Lote) void
        +quantidade_total() int
        +dar_baixa(quantidade: int) bool
    }

    class GestorEstoque {
        -dict~str, ItemEstoque~ _produtos
        +cadastrar_produto(produto: ItemEstoque) void
        +realizar_baixa(codigo: str, quantidade: int) bool
        +gerar_alerta_vencimento(dias_limite: int) list
    }

    ItemEstoque <|.. Produto : implementa
    Produto "1" *-- "many" Lote : possui
    GestorEstoque "1" o-- "many" ItemEstoque : gerencia
