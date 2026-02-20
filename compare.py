import argparse
import os
import shutil
import sys
import time

from env.fire_env import FireEnvironment
from agents.compare_agent import CompareAgent
from search import (
    astar_search,
    breadth_first_graph_search,
    depth_first_graph_search,
    greedy_best_first_graph_search,
    uniform_cost_search,
)


DEFAULT_GRID = [["." for _ in range(20)] for _ in range(20)]

DEFAULT_INITIAL = (
    (0, 0),
    ((5, 5), (5, 15), (15, 5), (15, 15), (10, 10), (2, 18), (18, 2)),
    3,
    (0, 0),
)

DEFAULT_MAX_STEPS = 1000
DEFAULT_VISUALIZE = True
DEFAULT_STEP_DELAY = 0.05


def default_algorithms():
    return {
        "BFS": lambda p: breadth_first_graph_search(p),
        "DFS": lambda p: depth_first_graph_search(p),
        "UCS": lambda p: uniform_cost_search(p),
        "Greedy": lambda p: greedy_best_first_graph_search(p, lambda n: p.h(n)),
        "A*": lambda p: astar_search(p),
    }


def _clear_screen_if_needed(clear_screen):
    if not clear_screen:
        return

    term = os.environ.get("TERM", "")

    # Em terminais ANSI, limpa tela + histórico de scrollback.
    if sys.stdout.isatty() and term and term.lower() != "dumb":
        sys.stdout.write("\033[3J\033[2J\033[H")
        sys.stdout.flush()
        return

    clear_cmd = "cls" if os.name == "nt" else "clear"
    if shutil.which(clear_cmd):
        os.system(clear_cmd)
    else:
        # Último fallback para ambientes sem suporte a limpeza real.
        print("\n" * 120, end="")


def _render_step(env, algorithm_name, step):
    print(f"\n=== {algorithm_name} | Passo {step} ===")
    env.render()


def _run_single_algorithm(
    name,
    alg,
    grid,
    initial,
    max_steps,
    visualize,
    step_delay,
    clear_screen,
):
    env = FireEnvironment(grid, initial)
    agent = CompareAgent(grid, alg)
    env.add_thing(agent)

    if visualize:
        _clear_screen_if_needed(clear_screen)
        _render_step(env, name, 0)
        if step_delay > 0:
            time.sleep(step_delay)

    start = time.perf_counter()
    steps = 0

    # Mesmo padrão do main.py: step + render. Aqui com limite/controle de falha.
    while len(env.state[1]) > 0 and steps < max_steps and not agent.search_failed:
        env.step()
        steps += 1

        if visualize:
            _clear_screen_if_needed(clear_screen)
            _render_step(env, name, steps)
            if step_delay > 0:
                time.sleep(step_delay)

    elapsed = round(time.perf_counter() - start, 4)
    fires_left = len(env.state[1])

    if fires_left == 0:
        status = "OK"
        cost = agent.plan_cost
    elif agent.search_failed:
        status = "SEM_SOLUCAO"
        cost = None
    else:
        status = "TIMEOUT"
        cost = None

    return {
        "algorithm": name,
        "status": status,
        "steps": steps,
        "cost": cost,
        "time_s": elapsed,
        "expanded": agent.expanded,
        "fires_left": fires_left,
    }


def run_comparison(
    grid=DEFAULT_GRID,
    initial=DEFAULT_INITIAL,
    max_steps=DEFAULT_MAX_STEPS,
    visualize=DEFAULT_VISUALIZE,
    step_delay=DEFAULT_STEP_DELAY,
    clear_screen=False,
):
    results = []

    for name, alg in default_algorithms().items():
        print(f"\nRodando {name}...")

        result = _run_single_algorithm(
            name=name,
            alg=alg,
            grid=grid,
            initial=initial,
            max_steps=max_steps,
            visualize=visualize,
            step_delay=step_delay,
            clear_screen=clear_screen,
        )
        results.append(result)

        if visualize:
            print(
                f"[{name}] Status: {result['status']} | "
                f"Passos: {result['steps']} | "
                f"Custo: {result['cost'] if result['cost'] is not None else '-'}"
            )

    return results


def _fmt_value(value):
    return "-" if value is None else value


def print_results(results):
    print("\n===== RESULTADOS =====")
    for r in results:
        print(
            f"{r['algorithm']} -> "
            f"Status: {r['status']} | "
            f"Passos: {_fmt_value(r['steps'])} | "
            f"Custo: {_fmt_value(r['cost'])} | "
            f"Tempo: {r['time_s']}s | "
            f"Nós: {r['expanded']} | "
            f"Fogos restantes: {r['fires_left']}"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compara algoritmos de busca no problema do bombeiro."
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=DEFAULT_MAX_STEPS,
        help=f"Máximo de passos por algoritmo (padrão: {DEFAULT_MAX_STEPS}).",
    )
    parser.add_argument(
        "--step-delay",
        type=float,
        default=DEFAULT_STEP_DELAY,
        help=f"Atraso (segundos) entre renders (padrão: {DEFAULT_STEP_DELAY}).",
    )
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Desativa renderização passo a passo do mapa.",
    )
    parser.add_argument(
        "--clear-screen",
        action="store_true",
        help="Limpa o terminal antes de cada render.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    visualize = not args.no_visualize
    step_delay = args.step_delay if visualize else 0

    results = run_comparison(
        max_steps=args.max_steps,
        visualize=visualize,
        step_delay=step_delay,
        clear_screen=args.clear_screen,
    )
    print_results(results)


if __name__ == "__main__":
    main()
