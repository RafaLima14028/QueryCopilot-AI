from agno.models.openrouter import OpenRouter

from app.core.settings import get_settings

gemini3_1_flash_lite = OpenRouter(
    id="google/gemini-3.1-flash-lite-preview",
    api_key=get_settings().OPENROUTER_API_KEY
)
