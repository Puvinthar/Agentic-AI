"""
Setup Script for Agentic AI Backend
Helps with initial configuration and testing
"""
import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_env_file():
    """Check if .env file exists"""
    print("\n🔍 Checking environment configuration...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("📝 Creating .env from .env.example...")
        
        example_path = Path(".env.example")
        if example_path.exists():
            import shutil
            shutil.copy(example_path, env_path)
            print("✅ .env file created")
            print("\n⚠️  IMPORTANT: Edit .env and add your API keys:")
            print("   - GROQ_API_KEY (get from https://console.groq.com/)")
            print("   - OPENWEATHER_API_KEY (get from https://openweathermap.org/)")
            return False
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file exists")
        
        # Check if keys are configured
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        weather_key = os.getenv("OPENWEATHER_API_KEY")
        
        if not groq_key or groq_key == "your_groq_api_key_here":
            print("⚠️  GROQ_API_KEY not configured in .env")
        else:
            print("✅ GROQ_API_KEY configured")
        
        if not weather_key or weather_key == "your_openweather_api_key_here":
            print("⚠️  OPENWEATHER_API_KEY not configured in .env")
        else:
            print("✅ OPENWEATHER_API_KEY configured")
        
        return True


def check_dependencies():
    """Check if dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "langchain",
        "langgraph",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install -r requirements.txt")
        return False
    
    return True


def check_database():
    """Check database connection"""
    print("\n🔍 Checking database connection...")
    
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv("SYNC_DATABASE_URL", "")
        
        if not db_url:
            print("⚠️  DATABASE_URL not configured")
            return False
        
        # Parse connection string
        # Format: postgresql://user:pass@host:port/db
        parts = db_url.replace("postgresql://", "").split("@")
        if len(parts) != 2:
            print("⚠️  Invalid DATABASE_URL format")
            return False
        
        user_pass = parts[0].split(":")
        host_port_db = parts[1].split("/")
        host_port = host_port_db[0].split(":")
        
        conn = psycopg2.connect(
            host=host_port[0],
            port=host_port[1] if len(host_port) > 1 else "5432",
            user=user_pass[0],
            password=user_pass[1],
            database=host_port_db[1]
        )
        conn.close()
        
        print("✅ Database connection successful")
        return True
        
    except ImportError:
        print("⚠️  psycopg2 not installed (will be installed with requirements)")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Start PostgreSQL with Docker:")
        print("   docker run --name postgres -e POSTGRES_PASSWORD=postgres \\")
        print("     -e POSTGRES_DB=agentic_db -p 5432:5432 -d postgres:15-alpine")
        return False


def create_directories():
    """Create necessary directories"""
    print("\n🔍 Creating directories...")
    
    dirs = ["uploads", "logs"]
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"✅ Created {dir_name}/ directory")
        else:
            print(f"✅ {dir_name}/ directory exists")


def print_next_steps():
    """Print next steps"""
    print_header("🎯 NEXT STEPS")
    
    print("1. Configure API Keys (if not done):")
    print("   - Edit .env file")
    print("   - Add GROQ_API_KEY from https://console.groq.com/")
    print("   - Add OPENWEATHER_API_KEY from https://openweathermap.org/")
    
    print("\n2. Start PostgreSQL:")
    print("   docker run --name postgres -e POSTGRES_PASSWORD=postgres \\")
    print("     -e POSTGRES_DB=agentic_db -p 5432:5432 -d postgres:15-alpine")
    
    print("\n3. Start the application:")
    print("   python main.py")
    print("   OR")
    print("   uvicorn main:app --reload --port 8000")
    
    print("\n4. Test the API:")
    print("   - Open http://localhost:8000/docs")
    print("   - Run: python test_api.py")
    
    print("\n5. Alternative - Use Docker Compose:")
    print("   docker-compose up -d")
    
    print("\n📚 Documentation:")
    print("   - README.md - Overview and features")
    print("   - SETUP.md - Detailed setup instructions")
    print("   - API_EXAMPLES.md - API usage examples")


def main():
    """Main setup function"""
    print_header("🚀 AGENTIC AI BACKEND - SETUP")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
    
    # Create directories
    create_directories()
    
    # Summary
    print_header("📊 SETUP SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅" if success else "⚠️ "
        print(f"{status} {name}")
    
    print(f"\n🎯 Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Setup complete! Ready to start.")
        print_next_steps()
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print_next_steps()


if __name__ == "__main__":
    main()
