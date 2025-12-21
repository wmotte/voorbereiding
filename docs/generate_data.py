import os
import json

def generate_data():
    data = {}
    
    # Krijg de root directory van het project (ga één niveau omhoog vanaf docs/)
    # We gaan ervan uit dat dit script in 'docs/' staat en 'output/' in de root.
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(docs_dir)
    output_dir = os.path.join(project_root, "output")
    
    if not os.path.exists(output_dir):
        print(f"❌ Fout: Map '{output_dir}' niet gevonden.")
        return

    # Exclude list
    exclude_dirs = {'.git', '.DS_Store', 'css', 'js', 'node_modules', '.gemini', '__pycache__', 'bijbelteksten'}

    for item in os.listdir(output_dir):
        full_path = os.path.join(output_dir, item)
        if os.path.isdir(full_path) and item not in exclude_dirs and not item.startswith('.'):
            municipality = item
            data[municipality] = {}
            
            # Walk through files in this directory
            for filename in os.listdir(full_path):
                if filename.endswith('.md'):
                    filepath = os.path.join(full_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        data[municipality][filename] = content
                    except Exception as e:
                        print(f"Error reading {filepath}: {e}")
                        
    # Schrijf naar data.js in de docs map
    js_content = f"window.CONTEXT_DATA = {json.dumps(data, indent=2)};"
    
    data_js_path = os.path.join(docs_dir, 'data.js')
    with open(data_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Generated docs/data.js with {len(data)} municipalities from output/.")

if __name__ == "__main__":
    generate_data()
