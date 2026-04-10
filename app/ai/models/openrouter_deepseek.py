from agno.models.openrouter import OpenRouter

from app.core.settings import get_settings

deepseek = OpenRouter(
    id="deepseek/deepseek-v3.2",
    api_key=get_settings().OPENROUTER_API_KEY,
    reasoning_effort="high"
)
