from agno.agent import Agent

sql_validator_agent = Agent()

"""
3. SQLValidatorAgent
Valida o SQL gerado antes de executar.

Verifica sintaxe (sem executar)
Verifica se tabelas/colunas existem no schema
Verifica risco da query (ex: DELETE sem WHERE → bloqueia)
Retorna { valid: bool, issues: list, risk_level: str }
"""
