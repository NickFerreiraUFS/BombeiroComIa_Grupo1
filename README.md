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
Implementado em `problems/fire_problem.py`, método `path_cost`:  
cada ação tem custo unitário (`+1`).

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
- **BFS / Uniform-Cost Search**: garantem solução ótima em custo unitário, mas tendem a expandir mais nós para grids maiores.
- **DFS**: baixo custo de memória, mas não garante melhor plano neste problema.
- **Greedy Best-First**: pode ser rápido, mas não garante otimalidade do caminho.

### Heurística `h(n)`
Implementada em `problems/fire_problem.py`, método `h`:
- com água `> 0`: distância Manhattan até o fogo mais próximo;
- com água `== 0`: distância até a base + distância da base até o fogo mais próximo.

**Intuição**: aproxima o custo mínimo real para agir sobre incêndios, considerando necessidade de recarga.

**Discussão (informal)**:
- é **admissível** na prática para o domínio modelado (custo unitário, movimentos Manhattan), pois não superestima deslocamentos mínimos;
- tende a ser **consistente** para movimentos unitários no grid, mantendo diferença local limitada entre estados adjacentes;
- melhora o desempenho do A\* reduzindo expansões em comparação com busca cega.

## 7. Estrutura do projeto

```text
BombeiroComIa_Grupo1/
├── env/              # Ambiente
├── agents/           # Agente e programa do agente
├── problems/         # Subclasse de Problem (AIMA)
├── tests/            # Testes automatizados
├── main.py           # Ponto de entrada
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
