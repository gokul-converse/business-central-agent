import inspect

from agent_framework import AgentSession

print(inspect.signature(AgentSession))
print(inspect.signature(AgentSession.from_dict))