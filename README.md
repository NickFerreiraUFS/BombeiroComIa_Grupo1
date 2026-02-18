# Projeto Agente Bombeiro - Busca IA

## 1. Descrição do problema
Este projeto implementa um agente inteligente baseado em busca para extinguir focos de incêndio em um grid. O agente possui água limitada, precisa apagar todos os focos e, quando necessário, retornar à base para reabastecer.

## 2. Objetivo
Encontrar e executar um plano de ações que elimine todos os incêndios com custo de caminho mínimo, usando algoritmos de busca do `aima-python` dentro do programa do agente.

## 3. Especificação formal do problema (AIMA)

### Representação de estados
Estado no formato:  
`((x, y), fires, water, base)`

- `(x, y)`: posição atual do agente.
- `fires`: tupla de coordenadas dos focos ativos.
- `water`: quantidade de água atual do agente.
- `base`: posição da base de reabastecimento.

### Espaço de Estados (Definição Formal)

Considere um grid de dimensões N x M.

Um estado é definido como:

s = ((x, y), F, w, b)

onde:

- x ∈ {0, 1, ..., N-1}
- y ∈ {0, 1, ..., M-1}
- F ⊆ {(i,j) | 0 ≤ i < N, 0 ≤ j < M} representa o conjunto de focos de incêndio ativos
- w ∈ {0, 1, ..., max_water} representa a quantidade de água disponível
- b ∈ {(i,j) | 0 ≤ i < N, 0 ≤ j < M} representa a posição da base

Logo, o espaço de estados é dado por:

S = Grid × P(Grid) × {0,...,max_water} × Grid

### Estado inicial
Definido em `main.py` pela variável `initial`.

### Conjunto de ações
`UP`, `DOWN`, `LEFT`, `RIGHT`, `EXTINGUISH`, `REFILL`.

### Modelo de transição (`result(s, a)`)
Implementado em `problems/fire_problem.py`, método `result`:
- ações de movimento alteram apenas posição;
- `EXTINGUISH` remove fogo na célula atual e consome 1 unidade de água;
- `REFILL` restaura a água para a capacidade máxima do agente.

### Teste de objetivo (`goal_test`)
Implementado em `problems/fire_problem.py`, método `goal_test`:  
`len(fires) == 0`.

### Custo de caminho (`path_cost`)
Implementado em `problems/fire_problem.py`, método `path_cost`.

O custo das ações é definido da seguinte forma:

- Movimentos (`UP`, `DOWN`, `LEFT`, `RIGHT`): custo 1  
- `EXTINGUISH`: custo 2  
- `REFILL`: custo 15  

Logo, o problema passa a ser de custo não uniforme, exigindo o uso de algoritmos
de busca informada ou de custo uniforme para garantir a otimalidade da solução.


## 4. Mapeamento explícito requisito → código

| Requisito AIMA | Implementação | Localização |
|----------------|---------------|-------------|
| **Ambiente** | `FireEnvironment` | `env/fire_env.py` |
| **Agente** | `FireAgent` | `agents/fire_agents.py` |
| **Programa de agente** | função `program(percept)` | `agents/fire_agents.py` (dentro de `FireAgent.__init__`) |
| **Subclasse de Problem** | `fireProblem` | `problems/fire_problem.py` |
| **Estados** | tupla `((x,y), fires, water, base)` | `problems/fire_problem.py` |
| **Ações** | método `actions(state)` | `problems/fire_problem.py` |
| **Transição** | método `result(state, action)` | `problems/fire_problem.py` |
| **Teste objetivo** | método `goal_test(state)` | `problems/fire_problem.py` |
| **Custo** | método `path_cost(c, s1, a, s2)` | `problems/fire_problem.py` |
| **Heurística** | método `h(node)` | `problems/fire_problem.py` |
| **Execução** | loop `env.step()` | `main.py` |
| **Testes** | suite com pytest | `tests/` |

## 5. Classificação do ambiente (com justificativa)

| Critério | Classificação | Justificativa |
|----------|---------------|---------------|
| **Determinístico** | Sim | Uma ação em um estado gera sempre o mesmo próximo estado. |
| **Observabilidade** | Totalmente observável | O percept contém posição do agente, todos os fogos, água disponível e base. |
| **Temporalidade** | Estático | O ambiente não muda sozinho entre ações do agente. |
| **Natureza** | Discreto | Estados e ações são finitos/discretos (células do grid e comandos). |
| **Agentes** | Único | Apenas um agente toma decisões no ambiente. |

## 6. Algoritmos de busca e heurística

### Algoritmo utilizado
**A\*** (`astar_search`), implementado em `agents/fire_agents.py`.

### Algoritmos não utilizados (e justificativa)

O problema modelado é sequencial e envolve planejamento com recurso limitado (água),
o que aumenta significativamente o espaço de estados e torna algoritmos de busca cega
menos eficientes neste domínio.

- **BFS**: não garante solução ótima neste domínio, pois assume custo uniforme entre ações.
- **Uniform-Cost Search (UCS)**: garante solução ótima mesmo com custos distintos entre ações, porém tende a expandir grande número de nós.
- **DFS**: baixo custo de memória, mas não garante melhor plano neste problema.
- **Greedy Best-First**: pode ser rápido, mas não garante otimalidade do caminho.

### Heurística `h(n)`
Implementada em `problems/fire_problem.py`, método `h`:

- estima a distância Manhattan até o foco de incêndio mais próximo;
- caso a quantidade de água disponível seja insuficiente para extinguir todos
os focos restantes, adiciona o custo mínimo obrigatório de uma visita à base
(distância até a base + custo da ação `REFILL`).


### Definição Formal da Heurística

Seja um estado:

n = ((x, y), F, w, b)

onde:

- (x, y) é a posição atual do agente
- F é o conjunto de focos de incêndio ativos
- w é a quantidade de água disponível
- b = (bx, by) é a posição da base

A heurística h(n) é definida como:

d_fire(n) = min { |x - fx| + |y - fy| : (fx, fy) ∈ F }

Se |F| > w:

d_base(n) = |x - bx| + |y - by|

h(n) = max( d_fire(n), d_base(n) + 15 )

Caso contrário:

h(n) = d_fire(n)

Essa heurística considera que, caso a quantidade de água disponível não seja
suficiente para extinguir todos os focos restantes, será obrigatória ao menos
uma visita à base para reabastecimento, cujo custo mínimo é estimado como a
distância até a base somada ao custo da ação REFILL (15).


**Intuição**: aproxima o custo mínimo real para agir sobre incêndios, considerando necessidade de recarga.

**Discussão (informal)**:
- é **admissível** para o domínio modelado, pois considera apenas custos mínimos
de deslocamento (distância Manhattan) e, quando necessário, o custo mínimo obrigatório de uma ação de reabastecimento (REFILL), sem superestimar o custo real;
- tende a ser **consistente** para movimentos unitários no grid, mantendo diferença local limitada entre estados adjacentes;
De fato, a heurística é consistente, pois:

h(n) ≤ c(n,a,n') + h(n')

para toda ação a que leva de n para n'.

Isso ocorre porque:

- a distância Manhattan varia no máximo em 1 unidade entre estados adjacentes;
- o custo mínimo de qualquer ação de movimento é 1;
- a penalidade de reabastecimento (15) só é considerada quando
|F| > w, representando um custo obrigatório futuro mínimo,
não sendo reduzida por ações locais de custo inferior.

Logo, a função h(n) satisfaz a desigualdade triangular e é
monotônica, garantindo que o A* encontre uma solução ótima.

- melhora o desempenho do A\* reduzindo expansões em comparação com busca cega.

## 7. Estrutura do projeto

```text
BombeiroComIa_Grupo1/
├── env/              # Ambiente
├── agents/           # Agente e programa do agente
├── problems/         # Subclasse de Problem (AIMA)
├── tests/            # Testes automatizados
├── main.py           # Ponto de entrada
├── compare.py        # Ponto de Comparação
└── README.md         # Documentação
```

## 8. Requisitos
- Python 3.8+
- Dependências: `aima-python`, `pytest`

## 9. Como executar

### 1. (Opcional) Criar ambiente virtual
**Linux/macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências
```bash
pip install aima pytest
```

### (Se necessário) Instalar numpy para testes
```bash
pip install numpy
```


### 3. Executar simulação
```bash
python main.py
# ou python3 main.py no Linux/macOS
```

## (Opcional) Instalar pytest para testes
```bash
pip install pytest
# ou
pip3 install pytest
```

### 4. Executar testes
```bash
pytest tests/
```

## 10. Observações técnicas
- A capacidade de água foi parametrizada (`max_water`) para evitar valor fixo no modelo.
- O replanejamento do agente ocorre apenas quando o plano termina (evita recomputação desnecessária).
- O ambiente deriva `base` e `max_water` do estado inicial.
- Prints de debug foram removidos para limpeza de saída.
