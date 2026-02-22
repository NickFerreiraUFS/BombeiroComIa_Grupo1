# Verificação: Especificação Formal do Problema (AIMA)

Este documento comprova que **todos os 6 itens obrigatórios** da especificação formal estão implementados e **claramente mapeados** para o código correspondente.

---

## ✅ Critério 1: Representação dos Estados

### Definição Formal

**Formato:** `((x, y), fires, water, base)`

Onde:
- `(x, y)`: posição do agente no grid
- `fires`: tupla de coordenadas dos focos ativos
- `water`: quantidade de água disponível (inteiro)
- `base`: posição da base de reabastecimento

### Mapeamento para o Código

#### Localização: `problems/fire_problem.py` (linha 24-26, 56-58, 81-82)

**Evidência 1 - Uso no método `actions`:**
```python
def actions(self, state):
    (x,y), fires, water, base = state  # ← DESEMPACOTAMENTO DO ESTADO
    possible = []
    # ...
```

**Evidência 2 - Uso no método `result`:**
```python
def result(self, state, action):
    (x,y), fires, water, base = state  # ← DESEMPACOTAMENTO DO ESTADO
    fires = list(fires)
    
    if action == "UP":
        return ((x-1,y), tuple(fires), water, base)  # ← RETORNA NOVO ESTADO
```

**Evidência 3 - Uso no método `goal_test`:**
```python
def goal_test(self, state):
    pos, fires, water, base = state  # ← DESEMPACOTAMENTO DO ESTADO
    return len(fires) == 0
```

**Evidência 4 - Uso na heurística:**
```python
def h(self, node):
    pos, fires, water, base = node.state  # ← ACESSO AO ESTADO
```

### Definição Formal Matemática (README.md, linhas 21-37)

```
s = ((x, y), F, w, b)

onde:
- x ∈ {0, 1, ..., N-1}
- y ∈ {0, 1, ..., M-1}
- F ⊆ {(i,j) | 0 ≤ i < N, 0 ≤ j < M}
- w ∈ {0, 1, ..., max_water}
- b ∈ {(i,j) | 0 ≤ i < N, 0 ≤ j < M}

Espaço de estados:
S = Grid × P(Grid) × {0,...,max_water} × Grid
```

### ✅ Mapeamento claro: SIM
- **Onde está:** `problems/fire_problem.py` (usado em todos os métodos)
- **Como está:** Tupla de 4 elementos `((x,y), fires, water, base)`
- **Documentação:** `README.md` linhas 11-37

---

## ✅ Critério 2: Estado Inicial

### Definição

O estado inicial especifica a configuração de partida do problema:
- posição inicial do agente
- locais dos focos de incêndio
- água inicial disponível
- localização da base

### Mapeamento para o Código

#### Localização: `main.py` (linhas 13-18)

```python
initial = (
    (0,0),                                            # ← posição inicial (linha 0, coluna 0)
    ((1,1),(1,2),(0,2),(2,2),(2,3),(1,3),(3,3)),    # ← 7 focos de incêndio
    3,                                                # ← 3 unidades de água
    (0,0)                                             # ← base na posição (0,0)
)

env = FireEnvironment(grid, initial)  # ← PASSADO PARA O AMBIENTE
```

#### Localização: `agents/fire_agents.py` (linha 24-27)

Quando o agente planeja, o estado inicial do problema de busca é o **percept atual**:

```python
def program(percept):
    # ...
    if not self.plan:
        problem = fireProblem(
            initial = percept,  # ← PERCEPT É O ESTADO ATUAL
            goal = None,
            grid = self.grid
        )
```

#### Localização: `problems/fire_problem.py` (linha 5-6)

A classe herda de `Problem` e passa `initial` para a superclasse:

```python
class fireProblem(Problem):
    def __init__(self, initial, goal, grid, max_water=3):
        super().__init__(initial, goal)  # ← ARMAZENA initial
```

### ✅ Mapeamento claro: SIM
- **Onde está:** `main.py` linha 13-18 (definição concreta)
- **Como é usado:** Passado para `FireEnvironment` e `fireProblem`
- **Documentação:** `README.md` linha 40-41

---

## ✅ Critério 3: Conjunto de Ações

### Definição

Ações disponíveis: `UP`, `DOWN`, `LEFT`, `RIGHT`, `EXTINGUISH`, `REFILL`

### Mapeamento para o Código

#### Localização: `problems/fire_problem.py` (linhas 24-52)

```python
def actions(self, state):
    (x,y), fires, water, base = state
    possible = []

    # 1. AÇÕES DE MOVIMENTO
    moves = {
        "UP": (x-1,y),      # ← AÇÃO UP
        "DOWN": (x+1,y),    # ← AÇÃO DOWN
        "LEFT": (x,y-1),    # ← AÇÃO LEFT
        "RIGHT": (x,y+1)    # ← AÇÃO RIGHT
    }

    for action,(nx,ny) in moves.items():
        if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
            # Não pode entrar em fogo sem água
            if water == 0 and (nx,ny) in fires:
                continue
            possible.append(action)

    # 2. AÇÃO EXTINGUISH
    if (x,y) in fires and water > 0:
        possible.append("EXTINGUISH")  # ← AÇÃO EXTINGUISH

    # 3. AÇÃO REFILL
    if water == 0 and (x,y) == base:
        possible.append("REFILL")  # ← AÇÃO REFILL

    return possible
```

**Restrições implementadas:**
- Movimentos só são válidos dentro dos limites do grid
- Não pode entrar em célula com fogo sem água
- `EXTINGUISH` só é possível se estiver no fogo e tiver água
- `REFILL` só é possível se estiver na base e sem água

### ✅ Mapeamento claro: SIM
- **Onde está:** `problems/fire_problem.py` método `actions` (linhas 24-52)
- **Como está:** Retorna lista de strings com ações válidas
- **Documentação:** `README.md` linha 43-44

---

## ✅ Critério 4: Modelo de Transição - `result(s, a)`

### Definição

Função que retorna o estado resultante após aplicar ação `a` no estado `s`.

### Mapeamento para o Código

#### Localização: `problems/fire_problem.py` (linhas 55-77)

```python
def result(self, state, action):
    (x,y), fires, water, base = state
    fires = list(fires)

    # TRANSIÇÃO PARA UP
    if action == "UP":
        return ((x-1,y), tuple(fires), water, base)

    # TRANSIÇÃO PARA DOWN
    elif action == "DOWN":
        return ((x+1,y), tuple(fires), water, base)

    # TRANSIÇÃO PARA LEFT
    elif action == "LEFT":
        return ((x,y-1), tuple(fires), water, base)

    # TRANSIÇÃO PARA RIGHT
    elif action == "RIGHT":
        return ((x,y+1), tuple(fires), water, base)

    # TRANSIÇÃO PARA EXTINGUISH
    elif action == "EXTINGUISH":
        fires.remove((x,y))                          # ← Remove fogo
        return ((x,y), tuple(fires), water-1, base)  # ← Consome água

    # TRANSIÇÃO PARA REFILL
    elif action == "REFILL":
        return ((x,y), tuple(fires), self.max_water, base)  # ← Reabastece
```

**Semântica das transições:**
- `UP/DOWN/LEFT/RIGHT`: altera posição, mantém fires/water/base
- `EXTINGUISH`: remove fogo da célula atual, decrementa água
- `REFILL`: restaura água ao máximo, mantém posição

### Teste de Transição

#### Localização: `tests/test_result.py`

```python
def test_result_refill():
    problem = fireProblem(
        initial=((0,0), ((1,1),), 0, (0,0)),
        goal=None,
        grid=[[".","."],[".","."]],
        max_water=5
    )
    new_state = problem.result(((0,0), ((1,1),), 0, (0,0)), "REFILL")
    assert new_state[2] == 5  # água voltou ao máximo
```

### ✅ Mapeamento claro: SIM
- **Onde está:** `problems/fire_problem.py` método `result` (linhas 55-77)
- **Como funciona:** Match de ação → retorna novo estado
- **Validação:** `tests/test_result.py`, `tests/test_extinguish.py`, `tests/test_actions.py`
- **Documentação:** `README.md` linhas 46-50

---

## ✅ Critério 5: Teste de Objetivo - `goal_test`

### Definição

Verifica se um estado é objetivo (problema resolvido).

**Condição:** Todos os focos de incêndio foram extintos.

### Mapeamento para o Código

#### Localização: `problems/fire_problem.py` (linhas 80-82)

```python
def goal_test(self, state):
    pos, fires, water, base = state
    return len(fires) == 0  # ← OBJETIVO: sem fogos restantes
```

### Testes de Goal Test

#### Localização: `tests/test_goal_true.py`

```python
def test_goal_test_true():
    problem = fireProblem(
        initial=((0,0), (), 3, (0,0)),  # ← SEM FOGOS
        goal=None,
        grid=[[".","."],[".","."]],
        max_water=3
    )
    assert problem.goal_test(((0,0), (), 3, (0,0))) == True  # ← DEVE SER OBJETIVO
```

#### Localização: `tests/test_goal_false.py`

```python
def test_goal_test_false():
    problem = fireProblem(
        initial=((0,0), ((1,1),), 3, (0,0)),  # ← COM FOGO
        goal=None,
        grid=[[".","."],[".","."]],
        max_water=3
    )
    assert problem.goal_test(((0,0), ((1,1),), 3, (0,0))) == False  # ← NÃO É OBJETIVO
```

### ✅ Mapeamento claro: SIM
- **Onde está:** `problems/fire_problem.py` método `goal_test` (linhas 80-82)
- **Condição:** `len(fires) == 0`
- **Validação:** `tests/test_goal_true.py` e `tests/test_goal_false.py`
- **Documentação:** `README.md` linhas 52-54

---

## ✅ Critério 6: Custo de Caminho - `path_cost`

### Definição

Função que calcula o custo acumulado de um caminho após aplicar ação `a` no estado `s1`, chegando a `s2`.

**Custos definidos:**
- Movimentos: `1`
- `EXTINGUISH`: `2`
- `REFILL`: `15`

### Mapeamento para o Código

#### Localização: `problems/fire_problem.py` (linhas 10-20)

```python
def path_cost(self, c, state1, action, state2):
    
    if action == "EXTINGUISH":
        return c + 2      # ← CUSTO DE EXTINGUIR: 2

    elif action == "REFILL":
        return c + 15     # ← CUSTO DE REABASTECER: 15

    else:
        return c + 1      # ← CUSTO DE MOVIMENTO: 1
```

**Justificativa dos custos:**
- Movimentos têm custo base (1)
- Extinguir é mais custoso que mover (2)
- Reabastecer é muito custoso (15), incentivando planejamento eficiente

### Teste de Path Cost

#### Localização: `tests/test_path_cost.py`

```python
def test_path_cost_for_actions():
    problem = fireProblem(
        initial=((0,0), ((1,1),), 3, (0,0)),
        goal=None,
        grid=[[".","."],[".","."]],
        max_water=3
    )

    s1 = ((0,0), ((1,1),), 3, (0,0))
    s2_move = ((0,1), ((1,1),), 3, (0,0))
    s2_ext = ((1,1), (), 2, (0,0))
    s2_refill = ((0,0), ((1,1),), 3, (0,0))

    assert problem.path_cost(0, s1, "RIGHT", s2_move) == 1      # ← movimento = 1
    assert problem.path_cost(10, s1, "EXTINGUISH", s2_ext) == 12  # ← 10 + 2 = 12
    assert problem.path_cost(5, s1, "REFILL", s2_refill) == 20    # ← 5 + 15 = 20
```

### ✅ Mapeamento claro: SIM
- **Onde está:** `problems/fire_problem.py` método `path_cost` (linhas 10-20)
- **Custos:** movimento=1, extinguir=2, refill=15
- **Validação:** `tests/test_path_cost.py`
- **Documentação:** `README.md` linhas 56-67

---

## Tabela Resumo: Mapeamento Completo

| Item Obrigatório | Arquivo | Método/Variável | Linhas | Testes |
|------------------|---------|-----------------|--------|--------|
| **1. Representação de estados** | `problems/fire_problem.py` | Usado em todos métodos | 24, 56, 81, 87 | Todos os testes |
| **2. Estado inicial** | `main.py` | variável `initial` | 13-18 | `test_full_execution.py` |
| **3. Conjunto de ações** | `problems/fire_problem.py` | método `actions(state)` | 24-52 | `test_actions.py` |
| **4. Modelo de transição** | `problems/fire_problem.py` | método `result(state, action)` | 55-77 | `test_result.py`, `test_extinguish.py` |
| **5. Teste de objetivo** | `problems/fire_problem.py` | método `goal_test(state)` | 80-82 | `test_goal_true.py`, `test_goal_false.py` |
| **6. Custo de caminho** | `problems/fire_problem.py` | método `path_cost(c, s1, a, s2)` | 10-20 | `test_path_cost.py` |

---

## Evidência Adicional: Tabela no README.md

O `README.md` (linhas 69-87) contém uma **tabela de mapeamento explícito** já documentada:

```markdown
## 4. Mapeamento explícito requisito → código

| Requisito AIMA | Implementação | Localização |
|----------------|---------------|-------------|
| **Estados** | tupla `((x,y), fires, water, base)` | `problems/fire_problem.py` |
| **Ações** | método `actions(state)` | `problems/fire_problem.py` |
| **Transição** | método `result(state, action)` | `problems/fire_problem.py` |
| **Teste objetivo** | método `goal_test(state)` | `problems/fire_problem.py` |
| **Custo** | método `path_cost(c, s1, a, s2)` | `problems/fire_problem.py` |
```

---

## Validação Prática

Execute os testes para comprovar funcionamento de cada item:

```bash
# Todos os testes (incluindo os 6 critérios)
.venv/bin/pytest -q

# Testes específicos por critério
.venv/bin/pytest tests/test_actions.py -v          # Critério 3
.venv/bin/pytest tests/test_result.py -v           # Critério 4
.venv/bin/pytest tests/test_goal_true.py -v        # Critério 5
.venv/bin/pytest tests/test_goal_false.py -v       # Critério 5
.venv/bin/pytest tests/test_path_cost.py -v        # Critério 6
```

---

## Conclusão

✅ **TODOS os 6 itens da especificação formal estão:**

1. **Implementados** corretamente no código
2. **Mapeados** claramente para localização específica
3. **Documentados** no README.md com tabela de referência
4. **Testados** com suite automatizada (pytest)
5. **Alinhados** com o padrão AIMA (herança de `Problem`)

**Conformidade:** 100% com o requisito do PDF da atividade.
