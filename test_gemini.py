"""Quick test for Gemini API"""
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Please edit .env file and add your actual Gemini API key")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Hello from AutoGen-EDA!' in exactly 5 words.")
        print("✅ Gemini API is working!")
        print(f"Response: {response.text}")
except ImportError:
    print("❌ google-generativeai not installed")
    print("Run: pip install google-generativeai")
except Exception as e:
    print(f"❌ Error: {e}")
