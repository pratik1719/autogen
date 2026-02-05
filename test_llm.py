from src.llm_client import LLMClient

try:
    client = LLMClient()
    response = client.generate("Say hello in exactly 5 words", "Test")
    print("✅ LLM is working!")
    print(f"Response: {response}")
except Exception as e:
    print(f"❌ Error: {e}")
