from agno.agent import Agent


intent_agent = Agent()

"""
1. IntentAgent
Entende o que o usuário quer antes de gerar qualquer SQL.

Extrai: entidade alvo, operação (SELECT/INSERT/UPDATE/DELETE), filtros, ordenação, limite
Retorna um objeto estruturado (schema Pydantic) para o próximo agent
"""
