# Projeto Agente Bombeiro - Busca IA

Descrição
---------
Projeto que implementa um agente inteligente baseado em busca para extinguir incêndios em um grid, utilizando a biblioteca `aima-python`.

Objetivo
--------
Extinguir todos os focos de incêndio no grid minimizando o custo de caminho, considerando que o agente tem capacidade limitada de água e precisa retornar à base para recarregar.

Especificação formal
--------------------
- Estado: ((x, y), fires, water, base)  
  - (x, y): posição do agente  
  - fires: tupla com coordenadas dos incêndios  
  - water: nível atual de água (inteiro)  
  - base: coordenada da base para recarga
- Estado inicial: definido em `main.py`
- Ações: UP, DOWN, LEFT, RIGHT, EXTINGUISH, REFILL
- Teste de objetivo: `len(fires) == 0`
- Custo: cada ação tem custo 1
- Modelo de transição: implementado em `problems/fire_problem.py`

Classificação do ambiente
-------------------------
- Observabilidade: Totalmente observável (posições dos fogos e da base conhecidas)
- Determinismo: Determinístico
- Temporalidade: Estático
- Natureza: Discreto
- Agentes: Único

Estrutura do projeto
--------------------
projectGrupo1/
├── env/            # FireEnvironment: lógica do mundo e percepções  
├── agent/          # FireAgent: agente e lógica de replanejamento  
├── problems/       # fireProblem: modelagem formal (AIMA)  
├── tests/          # Testes automatizados (pytest)  
├── main.py         # Ponto de entrada  
└── README.md       # Documentação

Requisitos
----------
- Python 3.8+  
- aima-python (instalar com `pip install aima-python`)  

Como executar
-------------
1. Criar e ativar um ambiente virtual (opcional):
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Instalar dependências:
   pip install aima-python
   ```
3. Rodar a simulação:
   ```bash
   python main.py
   ```
4. Rodar testes:
   ```bash
   pytest tests/
   ```

Observações
----------
- Verifique `main.py`, `problems/fire_problem.py` e `agent/` para detalhes da implementação e parâmetros (capacidade de água, tamanhos de grid, posições iniciais).