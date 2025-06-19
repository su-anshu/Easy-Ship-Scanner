import ast
import sys

def check_syntax(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        
        # Try to parse the AST
        ast.parse(code)
        print(f"✅ {filename} syntax is CORRECT!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error in {filename}:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error checking {filename}: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking app.py syntax...")
    result = check_syntax("app.py")
    
    if result:
        print("\n🎉 Your app is ready to run!")
        print("💡 Try: streamlit run app.py")
    else:
        print("\n🔧 Fix the syntax errors above and try again.")
