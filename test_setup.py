"""
Test script to verify AutoGen-EDA setup
Run this after installation to check everything is configured correctly
"""
import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False


def check_dependencies():
    """Check if all dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    required = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scipy',
        'google.generativeai',
        'dotenv',
        'jinja2'
    ]
    
    all_good = True
    
    for package in required:
        try:
            __import__(package.replace('.', '_') if '.' in package else package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (run: pip install -r requirements.txt)")
            all_good = False
    
    return all_good


def check_env_file():
    """Check if .env file exists and has API key."""
    print("\n🔑 Checking environment configuration...")
    
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ❌ .env file not found")
        print("      Run: cp .env.example .env")
        print("      Then add your Gemini API key")
        return False
    
    print("   ✅ .env file exists")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("   ⚠️  GEMINI_API_KEY not configured")
        print("      Edit .env and add your API key from:")
        print("      https://aistudio.google.com/app/apikey")
        return False
    
    print(f"   ✅ GEMINI_API_KEY configured ({api_key[:10]}...)")
    return True


def check_directories():
    """Check if required directories exist."""
    print("\n📁 Checking directory structure...")
    
    required_dirs = ['src', 'data', 'output', 'logs', 'video']
    all_good = True
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ (missing)")
            all_good = False
    
    return all_good


def check_source_files():
    """Check if all source files exist."""
    print("\n📄 Checking source files...")
    
    required_files = [
        'src/main.py',
        'src/data_loader.py',
        'src/llm_client.py',
        'src/eda_planner.py',
        'src/analyzer.py',
        'src/visualizer.py',
        'src/insight_generator.py',
        'src/report_builder.py',
        'src/utils.py'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            all_good = False
    
    return all_good


def test_llm_connection():
    """Test connection to Gemini API."""
    print("\n🤖 Testing LLM connection...")
    
    try:
        from src.llm_client import LLMClient
        
        client = LLMClient()
        response = client.generate(
            "Say 'Hello from AutoGen-EDA!' and nothing else.",
            purpose="Connection Test",
            temperature=0.0
        )
        
        print(f"   ✅ LLM connection successful!")
        print(f"   Response: {response[:100]}...")
        return True
    
    except Exception as e:
        print(f"   ❌ LLM connection failed: {str(e)[:100]}")
        return False


def main():
    """Run all checks."""
    print("="*80)
    print("🚀 AutoGen-EDA Setup Verification")
    print("="*80)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Directory Structure", check_directories),
        ("Source Files", check_source_files),
    ]
    
    results = []
    
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    # Test LLM only if other checks pass
    if all(r[1] for r in results):
        llm_result = test_llm_connection()
        results.append(("LLM Connection", llm_result))
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    
    if all_passed:
        print("🎉 All checks passed! You're ready to run AutoGen-EDA!")
        print("\nNext steps:")
        print("  1. Download a CSV dataset to data/")
        print("  2. Run: python src/main.py data/your_dataset.csv")
        print("  3. Check output/ for your reports!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nSee QUICKSTART.md for setup instructions.")
    
    print("="*80 + "\n")
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
