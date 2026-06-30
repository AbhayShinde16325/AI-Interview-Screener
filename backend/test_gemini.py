from app.ai.gemini.client import GeminiClient

client = GeminiClient()

response = client.generate(
    """
    Say hello in exactly one sentence.
    """
)

print(response)