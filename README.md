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
| **Comparação de algoritmos** | `CompareAgent` + script de benchmark | `agents/compare_agent.py` + `compare.py` |
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

### Algoritmo padrão na simulação
**A\*** (`astar_search`), implementado em `agents/fire_agents.py`.

### Algoritmos avaliados no comparador

O problema modelado é sequencial e envolve planejamento com recurso limitado (água),
o que aumenta significativamente o espaço de estados e torna algoritmos de busca cega
menos eficientes neste domínio.

- **BFS**: rápido para custos uniformes, mas pode gerar planos com custo maior quando ações têm custos diferentes.
- **UCS**: encontra plano ótimo em custo, porém costuma expandir muitos nós.
- **DFS**: baixo uso de memória, mas não garante custo mínimo nem menor número de passos.
- **Greedy Best-First**: usa a heurística para acelerar busca, mas não garante otimalidade.
- **A\***: combina custo acumulado + heurística, buscando equilíbrio entre qualidade e esforço computacional.

### Justificativa por tipo de busca (por que não foi adotada como padrão)

#### 1) Busca não informada (cega)
- **BFS**: foi testada no comparador, mas não é adequada como padrão porque o problema tem custos não uniformes (`EXTINGUISH=2`, `REFILL=15`).
- **UCS**: foi testada e é ótima em custo, porém com alto custo computacional (muitas expansões e maior tempo).
- **DFS**: foi testada, mas tende a retornar planos longos/subótimos neste domínio.
- **Profundidade Limitada (DLS)**: depende fortemente de um limite correto; limite baixo perde solução, limite alto degrada para comportamento de DFS.
- **Aprofundamento Iterativo (IDS)**: bom para profundidade desconhecida em custo unitário, mas aqui reexpande muitos nós e não otimiza custo em domínio com pesos diferentes.
- **Bidirecional**: exige alvo bem definido e transição reversa prática; aqui o objetivo é um conjunto de estados (`fires` vazio) com componente de recurso (`water`) e ação de recarga, o que dificulta modelagem reversa eficiente.

#### 2) Busca informada (heurística)
- **Greedy Best-First**: foi testada, mas não garante otimalidade por considerar apenas `h(n)`.
- **A\***: escolhida como padrão por equilibrar qualidade de solução e orientação heurística.
- **MA\*/SMA\*** (memória limitada): não foram adotadas porque o projeto não tinha restrição explícita de RAM; aumentariam complexidade de implementação/manutenção sem ganho claro para o escopo atual.

#### 3) Busca local e otimização
- **Hill Climbing**, **Simulated Annealing**, **Local Beam** e **Algoritmos Genéticos** não foram usados como método principal porque priorizam encontrar estados “bons”, não necessariamente um plano de ações ótimo e completo.
- Neste problema, o caminho importa (custos acumulados e sequência válida de ações com `water`/`REFILL`), então métodos de otimização local podem encontrar soluções inviáveis ou sem garantia de completude/otimalidade.

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
- Dependência para testes: `pytest`
- O projeto já inclui os arquivos usados da AIMA (`search.py` e `agents.py`) na raiz.

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

### 2. Instalar dependência de testes
```bash
pip install pytest
```

### 3. Executar simulação
```bash
python main.py
# ou python3 main.py no Linux/macOS
```

## 10. Comparação entre algoritmos

O benchmark de busca está em `compare.py` e executa `BFS`, `DFS`, `UCS`, `Greedy` e `A*`
no mesmo cenário, usando `CompareAgent` (`agents/compare_agent.py`).

### Executar comparação
```bash
python compare.py
# ou, sem ativar a virtualenv:
.venv/bin/python compare.py
```

Por padrão, o `compare.py` renderiza o mapa passo a passo para cada algoritmo
(mesmo padrão de `main.py`: `env.step()` + `env.render()`).

### Executar comparação sem renderização (modo rápido)
```bash
python compare.py --no-visualize
```

### Ajustar velocidade da animação
```bash
python compare.py --step-delay 0.1
```

### Limpar tela a cada passo (animação em terminal)
```bash
python compare.py --clear-screen
```

Observação: execute em um terminal interativo (ex.: bash/zsh/PowerShell). Em painéis
de saída que não suportam controle ANSI, a limpeza por passo pode não funcionar.

### Métricas exibidas
- `Status`: `OK`, `TIMEOUT` ou `SEM_SOLUCAO`
- `Passos`: número de ações executadas no ambiente
- `Custo`: custo total do plano encontrado
- `Tempo`: tempo total de execução do algoritmo
- `Nós`: expansões de nós (via `InstrumentedProblem`)
- `Fogos restantes`: quantos focos não foram apagados ao final

### Ajustar cenário da comparação
- `DEFAULT_GRID` em `compare.py`
- `DEFAULT_INITIAL` em `compare.py`
- `DEFAULT_MAX_STEPS` em `compare.py`
- Também é possível sobrescrever o limite via CLI: `python compare.py --max-steps 2000`

### Observações sobre a execução dos algoritmos
- O agente de comparação calcula um plano completo antes de executar a primeira ação de cada ciclo de planejamento.
- Por isso, em alguns casos (principalmente no **A\***), pode haver uma pausa perceptível antes do primeiro movimento no mapa.
- Isso não indica falha: é o tempo de busca/planejamento inicial.
- Quando a visualização está ativa, o tempo reportado também inclui renderização e `--step-delay`.
- Para comparar tempo de busca de forma mais justa, use: `python compare.py --no-visualize`.

## 11. Área de testes
- Os testes automatizados do projeto ficam em `tests/`.
- O arquivo `pytest.ini` limita a coleta para `tests/`, evitando coletar `aima-python/tests` (que exigem bibliotecas extras não usadas neste projeto).
- A suíte cobre ações, transição de estados, custo de caminho, heurística, goal test, ambiente e execução completa.

### Executar todos os testes
```bash
pytest
# ou, sem ativar a virtualenv:
.venv/bin/pytest
```

### Executar um teste específico
```bash
pytest tests/test_heuristic_no_water.py
```

## 12. Observações técnicas
- A capacidade de água foi parametrizada (`max_water`) para evitar valor fixo no modelo.
- O replanejamento do agente ocorre apenas quando o plano termina (evita recomputação desnecessária).
- O ambiente deriva `base` e `max_water` do estado inicial.
- O custo de `REFILL` é 15 e isso já está coberto nos testes.
- O comparador trata explicitamente casos de `TIMEOUT` e `SEM_SOLUCAO`, sem quebrar a impressão dos resultados.
- Prints de debug foram removidos para limpeza de saída.
