# Verificação Formal dos Critérios Obrigatórios

Este documento comprova tecnicamente que o projeto atende aos dois critérios fundamentais especificados no PDF da atividade.

---

## Arquitetura Ambiente – Agente – Programa de Agente explícita

### Evidências no código

#### 1. **Ambiente** (`env/fire_env.py`)

```python
from agents import Environment

class FireEnvironment(Environment):
    def __init__(self, grid, initial_state, max_water=None):
        super().__init__()
        self.grid = grid
        self.state = initial_state
        # ...
        self.fires = list(fires)

    def percept(self, agent):
        return self.state

    def execute_action(self, agent, action):
        # Atualiza estado conforme ação
        if action == "UP":
            self.state = ((x-1,y), tuple(self.fires), water, base)
        # ... outras ações
```

**Responsabilidades do Ambiente:**
- Mantém estado do mundo (`self.state`)
- Fornece percepção ao agente via `percept(agent)`
- Executa ações via `execute_action(agent, action)`
- Herda de `Environment` do aima-python

---

#### 2. **Agente** (`agents/fire_agents.py`)

```python
from agents import Agent

class FireAgent(Agent):
    def __init__(self, grid):
        self.grid = grid
        self.plan = []
        self.last_state = None

        def program(percept):
            # ... decisão baseada em percept
            return action

        super().__init__(program)
```

**Responsabilidades do Agente:**
- Herda de `Agent` (classe base do aima-python)
- Encapsula o programa de agente
- É inserido no ambiente via `env.add_thing(agent)`

---

#### 3. **Programa de Agente** (`agents/fire_agents.py`)

```python
def program(percept):
    # 🔥 Se o mundo mudou → joga plano fora
    if percept != self.last_state:
        self.plan = []

    self.last_state = percept

    # 🧠 Replaneja se não tem plano
    if not self.plan:
        problem = fireProblem(
            initial = percept,
            goal = None,
            grid = self.grid
        )
        solution = astar_search(problem)
        if solution:
            self.plan = solution.solution()

    if self.plan:
        return self.plan.pop(0)

    return "NoOp"
```

**Responsabilidades do Programa:**
- Recebe **percept** como entrada
- Decide quando formular problema
- Executa busca quando necessário
- Retorna **uma ação** por chamada
- Mantém estado interno (plano)

---

#### 4. **Ciclo Percepção-Ação** (integração via `Environment.step()`)

No arquivo `agents.py` (base do aima-python), linha ~323-336:

```python
def step(self):
    """Run the environment for one time step."""
    if not self.is_done():
        actions = []
        for agent in self.agents:
            if agent.alive:
                actions.append(agent.program(self.percept(agent)))  # ← CHAMADA
            else:
                actions.append("")
        for (agent, action) in zip(self.agents, actions):
            self.execute_action(agent, action)
        self.exogenous_change()
```

**Fluxo completo:**
1. `env.step()` chama `self.percept(agent)` → retorna estado
2. Passa percept para `agent.program(percept)` → retorna ação
3. Chama `self.execute_action(agent, action)` → atualiza mundo

---

#### 5. **Loop principal** (`main.py`)

```python
env = FireEnvironment(grid, initial)
agent = FireAgent(grid)
env.add_thing(agent)

while len(env.fires):
    env.step()    # ← Ciclo percept → program → action
    env.render()
```

---

### Conclusão Critério 1

✅ **A separação conceitual Ambiente–Agente–Programa está explícita:**

- `FireEnvironment` herda de `Environment`
- `FireAgent` herda de `Agent`
- `program(percept)` é função interna que recebe percept e retorna ação
- O ciclo é mediado por `env.step()` do framework aima-python

---

## Critério 2: Algoritmos de busca utilizados DENTRO do programa do agente

### ✅ ATENDIDO

### Evidências no código

#### 1. Busca é chamada DENTRO do `program(percept)`

Arquivo: `agents/fire_agents.py` (linhas 13-37)

```python
def program(percept):
    # ... lógica de verificação de mudança de estado

    # 🧠 Replaneja se não tem plano
    if not self.plan:
        
        problem = fireProblem(
            initial = percept,
            goal = None,
            grid = self.grid
        )

        solution = astar_search(problem)  # ← BUSCA DENTRO DO PROGRAMA

        if solution:
            self.plan = solution.solution()

    if self.plan:
        return self.plan.pop(0)  # ← Retorna UMA ação por vez

    return "NoOp"
```

---

#### 2. Busca NÃO é chamada isoladamente fora do ciclo

**❌ Padrão incorreto (não usado):**
```python
# ERRADO: busca fora do programa do agente
problem = fireProblem(...)
solution = astar_search(problem)
plan = solution.solution()

for action in plan:
    env.execute_action(agent, action)  # executa tudo de uma vez
```

**✅ Padrão correto (implementado):**
```python
# CORRETO: busca dentro do programa, ação por ação no ciclo
def program(percept):
    if not self.plan:
        problem = fireProblem(initial=percept, ...)
        solution = astar_search(problem)
        self.plan = solution.solution()
    
    return self.plan.pop(0)  # uma ação por step
```

---

#### 3. Fluxo real de execução

**Passo a passo de `main.py`:**

```python
while len(env.fires):
    env.step()    # ← Chama program(percept) internamente
    env.render()
```

**O que acontece em cada `env.step()`:**

1. `env.percept(agent)` → retorna estado atual
2. `agent.program(percept)` é executado:
   - Se não tem plano: formula problema e chama `astar_search`
   - Se tem plano: consome próxima ação
3. `env.execute_action(agent, action)` → atualiza mundo
4. Repete no próximo `step()`

---

#### 4. Prova adicional: Comparador de algoritmos

Arquivo: `agents/compare_agent.py`

```python
class CompareAgent(Agent):
    def __init__(self, grid, search_alg):
        self.search_alg = search_alg  # ← algoritmo parametrizado
        
        def program(percept):
            if not self.plan:
                problem = fireProblem(initial=percept, ...)
                solution = self.search_alg(problem)  # ← busca DENTRO
                if solution:
                    self.plan = solution.solution()
            
            if self.plan:
                return self.plan.pop(0)
            return "NoOp"
        
        super().__init__(program)
```

Usado em `compare.py` para testar BFS, DFS, UCS, Greedy e A* **dentro do mesmo padrão de programa de agente**.

---

### Conclusão Critério 2

✅ **A busca é utilizada DENTRO do programa do agente:**

- `astar_search` é chamada dentro da função `program(percept)`
- Não há chamada isolada de busca fora do ciclo percepção-ação
- O agente decide **quando** buscar (quando não tem plano)
- O agente retorna **uma ação por vez** ao ambiente
- Padrão segue `SimpleProblemSolvingAgentProgram` do AIMA

---

## Conformidade com o PDF da Atividade

### Trecho literal do PDF:

> "O programa de agente não é o algoritmo de busca em si (embora ele seja necessário).  
> Ele deve:
> - receber percepções do ambiente;
> - decidir quando formular um problema;
> - executar um algoritmo de busca para gerar um plano (sequência de ações);
> - retornar uma ação por passo ao ambiente."

### ✅ Implementação atende item por item:

| Requisito do PDF | Implementação | Localização |
|------------------|---------------|-------------|
| Receber percepções | `def program(percept)` | `agents/fire_agents.py:13` |
| Decidir quando formular problema | `if not self.plan:` | `agents/fire_agents.py:21` |
| Executar busca para gerar plano | `solution = astar_search(problem)` | `agents/fire_agents.py:30` |
| Retornar uma ação por passo | `return self.plan.pop(0)` | `agents/fire_agents.py:35` |

---

## Resumo Final

### ✅ Critério 1: Arquitetura explícita
- **Ambiente**: `FireEnvironment` (herda `Environment`)
- **Agente**: `FireAgent` (herda `Agent`)
- **Programa**: função `program(percept)` interna ao agente

### ✅ Critério 2: Busca dentro do programa
- Busca é chamada **dentro** de `program(percept)`
- Não há chamada isolada de busca
- Retorna uma ação por vez ao ambiente
- Segue ciclo percept → decide → action

---

## Validação Prática

Execute para comprovar funcionamento:

```bash
# Execução padrão (A* dentro do programa)
python main.py

# Comparação de algoritmos (todos dentro do programa)
python compare.py --no-visualize

# Testes automatizados
.venv/bin/pytest -q
```

---

**Conclusão:** O projeto atende integralmente aos dois critérios obrigatórios especificados no documento da atividade.
