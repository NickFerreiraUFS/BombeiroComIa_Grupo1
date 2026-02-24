## Parte 1: Problema + Objetivo + Originalidade

### Foco

- “Nosso problema é um bombeiro em grid com focos de incêndio, água limitada e necessidade de reabastecer na base.”
- “A solução usa busca dentro do programa do agente para gerar plano de ações.”
- “O objetivo é minimizar custo de caminho apagando todos os focos.”
- "O ambiente é completamente observável, determinístico, estático, discreto e de agente único."


### Pontos de código
- [main.py](../main.py) (configuração do ambiente e agente)
- [env/fire_env.py](../env/fire_env.py) (definição do ambiente, percept e renderização)
- [compare.py](../compare.py) (comparação de algoritmos)
- [TestesAutomatizados](../tests/) (qualidade e confiabilidade) 

### Demonstração rápida (ao vivo)
```bash
python main.py
```

---

## Parte 2 — Integrante 2: Especificação Formal do Problema (AIMA)

### Foco
- Cobrir os 6 itens obrigatórios do PDF: estado, estado inicial, ações, transição, goal test, path cost.

### O que
- “Estado: `((x, y), fires, water, base)`.”
- “Ações: `UP`, `DOWN`, `LEFT`, `RIGHT`, `EXTINGUISH`, `REFILL`.”
- “Transição altera posição/água/fogos conforme a ação.”
- “Objetivo: não restar fogo.”
- “Custo: movimento=1, extinguir=2, refill=15.”

### Trechos para mostrar
- [`class fireProblem`](../problems/fire_problem.py#L3) (L3)
- [`path_cost(...)`](../problems/fire_problem.py#L11-L19) (L11-19) — custo de movimento, extinguir, refill
- [`actions(...)`](../problems/fire_problem.py#L23-L49) (L23-49) — ações válidas conforme estado
- [`result(...)`](../problems/fire_problem.py#L53-L74) (L53-74) — transição de estado
- [`goal_test(...)`](../problems/fire_problem.py#L77-L80) (L77-80) — teste de objetivo
- [`h(node)`](../problems/fire_problem.py#L83-L101) (L83-101) — função heurística

### Pontos de código para abrir
- [`problems/fire_problem.py`](../problems/fire_problem.py) (métodos formais do modelo).
- [`README.md`](../README.md) (tabela "mapeamento requisito → código").
### Material de apoio
- Se perguntarem sobre mapeamento detalhado: `VERIFICACAO_ESPECIFICACAO_FORMAL.md`
---

## Parte 3 — Integrante 3: Classificação do Ambiente + Justificativas

### Foco
- Classificar formalmente o ambiente segundo AIMA:
  - determinístico/estocástico
  - observável
  - estático/dinâmico
  - discreto/contínuo
  - agente único/múltiplos

### O que
- “Determinístico: mesma ação no mesmo estado gera mesmo resultado.”
- “Totalmente observável: percept retorna o estado completo.”
- “Estático: ambiente não muda sozinho entre ações.”
- “Discreto: grid e ações discretas.”
- “Agente único: apenas um agente bombeiro decide.”

### Trechos para mostrar
- [`percept(...)`](../env/fire_env.py#L15) (L15) — fornece estado completo
- [`execute_action(...)`](../env/fire_env.py#L18-L40) (L18-40) — executa ação e atualiza estado
- [`render(...)`](../env/fire_env.py#L42-L60) (L42-60) — renderização do mundo

### Pontos de código para abrir
- [`env/fire_env.py`](../env/fire_env.py) (estrutura do ambiente e atualização do estado).
- [`README.md`](../README.md) (quadro de classificação do ambiente).

---

## Parte 4 — Integrante 4: Arquitetura Ambiente – Agente – Programa de Agente

### Foco
- Mostrar separação conceitual exigida no enunciado.
- Provar que busca está dentro do programa do agente (não chamada isolada fora do ciclo percepção-ação).

### O que
- “Ambiente: mantém estado, fornece percept e executa ação.”
- “Agente: entidade inserida no ambiente.”
- “Programa do agente: função `program(percept)` decide ação passo a passo.”
- “Quando necessário, programa formula `fireProblem`, chama A* e executa plano.”

### Trechos para mostrar
- [`class FireAgent`](../agents/fire_agents.py#L5) (L5) — agente que planeja com A*
- [`program(percept)`](../agents/fire_agents.py#L17-L47) (L17-47) — função que decide ação baseado em percept
- [`astar_search(problem)`](../agents/fire_agents.py#L29) — chamada de busca dentro do programa

### Pontos de código para abrir
- [`agents/fire_agents.py`](../agents/fire_agents.py) (replanejamento e consumo de plano).
- [`main.py`](../main.py) (`env.add_thing(agent)` + loop de passos).

---

## Parte 5 — Integrante 5: Algoritmos de Busca + Heurística + Comparação

### Foco
- Mostrar algoritmo padrão (A*) e justificativa.
- Explicar a heurística `h(n)` e sua intuição.
- Mostrar comparação com outros algoritmos (BFS/DFS/UCS/Greedy/A*).

### O que
- “A* foi escolhido como padrão por equilibrar custo acumulado e heurística.”
- “Heurística usa distância Manhattan ao fogo mais próximo e considera necessidade de refill quando água é insuficiente.”
- “Também avaliamos outros algoritmos para justificar adequação ao problema.”

### Trechos para mostrar
- [`h(node)`](../problems/fire_problem.py#L83-L101) (L83-101) — função heurística
- [`compare.py`](../compare.py) — comparação de algoritmos de busca

### Demonstração ao vivo (comparação)
```bash
python compare.py --no-visualize
```

### Se quiser mostrar mapa animado
```bash
python compare.py --step-delay 0.1
```

---

## Parte 6 — Integrante 6: Testes Automatizados + Execução Final + Fechamento

### Foco
- Comprovar qualidade e confiabilidade via testes automatizados.
- Encerrar com execução final ao vivo e ligação com critérios de avaliação.

### O que
- “Temos testes para ações, transição, objetivo, custo, heurística, agente e execução completa.”
- “A suíte garante que o comportamento esperado está preservado.”
- “Fechamos demonstrando execução em tempo real.”

### Trechos para mostrar
- Pasta `tests/` (exemplos):
  - `tests/test_actions.py`
  - `tests/test_result.py`
  - `tests/test_goal_true.py` e `tests/test_goal_false.py`
  - `tests/test_path_cost.py`
  - `tests/test_heuristic.py` e `tests/test_heuristic_no_water.py`
  - `tests/test_agent_plan.py`
  - `tests/test_full_execution.py`

### Demonstração ao vivo (testes)
```bash
.venv/bin/pytest -q
```

### Fechamento ao vivo
```bash
python main.py
```

---

## Ordem prática para abrir arquivos durante a apresentação

1. `README.md`
2. `main.py`
3. `problems/fire_problem.py`
4. `env/fire_env.py`
5. `agents/fire_agents.py`
6. `compare.py`
7. `tests/`

---

## Checklist final (antes de apresentar)

- [ ] Rodar `python main.py` sem erro.
- [ ] Rodar `.venv/bin/pytest -q` e confirmar testes passando.
- [ ] Rodar `python compare.py --no-visualize` para ter números de comparação.
- [ ] Cada integrante ensaiar sua parte com 1 arquivo principal.
- [ ] Deixar terminal já na raiz do projeto.
- [ ] Ter um plano B: se animação estiver lenta, usar `--no-visualize`.

---
