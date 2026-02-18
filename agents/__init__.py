"""
Pacote agents - Re-exporta classes do agents.py (AIMA) ou fornece fallback leve.
"""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

_base_agents_path = Path(__file__).resolve().parent.parent / "agents.py"

# Classes fallback (definidas primeiro)
class Thing:
    pass


class Agent(Thing):
    def __init__(self, program=None):
        self.alive = True
        self.program = program if program is not None else (lambda percept: "NoOp")


class Environment:
    def __init__(self):
        self.things = []
        self.agents = []

    def add_thing(self, thing):
        self.things.append(thing)
        if isinstance(thing, Agent):
            self.agents.append(thing)

    def step(self):
        for agent in list(self.agents):
            if agent.alive:
                action = agent.program(self.percept(agent))
                self.execute_action(agent, action)

    def percept(self, agent):
        raise NotImplementedError

    def execute_action(self, agent, action):
        raise NotImplementedError


__all__ = ["Thing", "Agent", "Environment"]

# Tenta sobrescrever com versão completa do AIMA se disponível
try:
    _spec = spec_from_file_location("_base_agents", _base_agents_path)
    _base_agents = module_from_spec(_spec)
    _spec.loader.exec_module(_base_agents)

    _aima_all = getattr(
        _base_agents,
        "__all__",
        [name for name in dir(_base_agents) if not name.startswith("_")]
    )

    # Sobrescreve com versões do AIMA
    for name in _aima_all:
        globals()[name] = getattr(_base_agents, name)
    
    __all__ = _aima_all
    print(f"[agents] Usando AIMA agents.py completo", file=sys.stderr)
    
except Exception as e:
    print(f"[agents] Usando fallback (AIMA indisponível: {e})", file=sys.stderr)
