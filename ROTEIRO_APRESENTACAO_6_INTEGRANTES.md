# Roteiro de Apresentação (6 Integrantes)

Este roteiro foi montado para cumprir exatamente o que o documento da atividade cobra: modelagem formal, classificação do ambiente, arquitetura Ambiente–Agente–Programa de Agente, uso de busca/heurística, testes e execução ao vivo.

---

## Visão geral do tempo (sugestão)

- Integrante 1: 2 min
- Integrante 2: 2 min
- Integrante 3: 2 min
- Integrante 4: 2 min
- Integrante 5: 2 min
- Integrante 6: 2 min
- Total técnico: ~12 min (ajustável)

---

## Parte 1 — Integrante 1: Problema + Objetivo + Originalidade

### Foco
- Apresentar o problema proposto pelo grupo.
- Mostrar que é um problema original (não copiado de exemplo pronto do AIMA).
- Conectar com o objetivo do projeto: agente que planeja para apagar incêndios com água limitada.

### O que falar
- “Nosso problema é um bombeiro em grid com focos de incêndio, água limitada e necessidade de reabastecer na base.”
- “A solução usa busca dentro do programa do agente para gerar plano de ações.”
- “O objetivo é minimizar custo de caminho apagando todos os focos.”

### Trechos para mostrar
- `README.md` (seções: descrição, objetivo e estrutura geral).
- `main.py` (cenário inicial e loop de execução).

### Pontos de código para abrir
- `main.py` (definição de `grid` e `initial`).
- `main.py` (`while len(env.fires): env.step(); env.render()`).

### Demonstração rápida (ao vivo)
```bash
python main.py
```

---

## Parte 2 — Integrante 2: Especificação Formal do Problema (AIMA)

### Foco
- Cobrir os 6 itens obrigatórios do PDF: estado, estado inicial, ações, transição, goal test, path cost.

### O que falar
- “Estado: `((x, y), fires, water, base)`.”
- “Ações: `UP`, `DOWN`, `LEFT`, `RIGHT`, `EXTINGUISH`, `REFILL`.”
- “Transição altera posição/água/fogos conforme a ação.”
- “Objetivo: não restar fogo.”
- “Custo: movimento=1, extinguir=2, refill=15.”

### Trechos para mostrar
- `problems/fire_problem.py`:
  - `class fireProblem`
  - `actions(...)`
  - `result(...)`
  - `goal_test(...)`
  - `path_cost(...)`
- `main.py` (estado inicial concreto).

### Pontos de código para abrir
- `problems/fire_problem.py` (métodos formais do modelo).
- `README.md` (tabela “mapeamento requisito → código”).
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

### O que falar
- “Determinístico: mesma ação no mesmo estado gera mesmo resultado.”
- “Totalmente observável: percept retorna o estado completo.”
- “Estático: ambiente não muda sozinho entre ações.”
- “Discreto: grid e ações discretas.”
- “Agente único: apenas um agente bombeiro decide.”

### Trechos para mostrar
- `env/fire_env.py`:
  - `percept(...)`
  - `execute_action(...)`
  - `render(...)`

### Pontos de código para abrir
- `env/fire_env.py` (estrutura do ambiente e atualização do estado).
- `README.md` (quadro de classificação do ambiente).

---

## Parte 4 — Integrante 4: Arquitetura Ambiente – Agente – Programa de Agente

### Foco
- Mostrar separação conceitual exigida no enunciado.
- Provar que busca está dentro do programa do agente (não chamada isolada fora do ciclo percepção-ação).

### O que falar
- “Ambiente: mantém estado, fornece percept e executa ação.”
- “Agente: entidade inserida no ambiente.”
- “Programa do agente: função `program(percept)` decide ação passo a passo.”
- “Quando necessário, programa formula `fireProblem`, chama A* e executa plano.”

### Trechos para mostrar
- `agents/fire_agents.py`:
  - `class FireAgent`
  - `program(percept)`
  - chamada `astar_search(problem)`
- `env/fire_env.py` (lado do ambiente no ciclo).

### Pontos de código para abrir
- `agents/fire_agents.py` (replanejamento e consumo de plano).
- `main.py` (`env.add_thing(agent)` + loop de passos).

---

## Parte 5 — Integrante 5: Algoritmos de Busca + Heurística + Comparação

### Foco
- Mostrar algoritmo padrão (A*) e justificativa.
- Explicar a heurística `h(n)` e sua intuição.
- Mostrar comparação com outros algoritmos (BFS/DFS/UCS/Greedy/A*).

### O que falar
- “A* foi escolhido como padrão por equilibrar custo acumulado e heurística.”
- “Heurística usa distância Manhattan ao fogo mais próximo e considera necessidade de refill quando água é insuficiente.”
- “Também avaliamos outros algoritmos para justificar adequação ao problema.”

### Trechos para mostrar
- `problems/fire_problem.py`:
  - `h(node)`
- `compare.py`:
  - `default_algorithms()`
  - `run_comparison(...)`
  - `print_results(...)`

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

### O que falar
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

## Script curto de transição entre integrantes

- Integrante 1 → 2: “Com o problema apresentado, agora formalizamos no modelo AIMA.”
- Integrante 2 → 3: “Com a modelagem pronta, classificamos o ambiente formalmente.”
- Integrante 3 → 4: “Agora mostramos a arquitetura Ambiente–Agente–Programa no código.”
- Integrante 4 → 5: “Com a arquitetura definida, explicamos busca e heurística.”
- Integrante 5 → 6: “Por fim, validamos com testes e encerramos com execução ao vivo.”
