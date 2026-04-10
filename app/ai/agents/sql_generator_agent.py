from agno.agent import Agent

sql_generator_agent = Agent()

"""
2. SQLGeneratorAgent
Recebe o intent estruturado + schema do banco e gera o SQL.

Precisa ter o schema do banco no contexto (via tool ou knowledge)
Usa structured_output para retornar { sql: str, params: list, explanation: str }
"""
