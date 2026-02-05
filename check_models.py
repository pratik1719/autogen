from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

print("✅ Checking available models with your API key...\n")
try:
    models = client.models.list()
    print("Available models for generateContent:")
    for model in models:
        if hasattr(model, 'supported_generation_methods'):
            if 'generateContent' in model.supported_generation_methods:
                print(f"  ✓ {model.name}")
        else:
            # Just list all models
            print(f"  • {model.name}")
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative method...")
    try:
        # Try direct model names
        test_models = [
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro-latest',
            'gemini-pro',
            'gemini-1.0-pro',
        ]
        print("\nTesting common model names:")
        for model_name in test_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents="test"
                )
                print(f"  ✓ {model_name} - WORKS!")
                break
            except:
                print(f"  ✗ {model_name} - doesn't work")
    except Exception as e2:
        print(f"Alternative test failed: {e2}")
