import os

# --- CONFIGURACIÓN ---
# Nombre del archivo de salida
OUTPUT_FILE = "PROYECTO_COMPLETO.txt"

# Carpetas que queremos ignorar (basura o binarios)
IGNORE_DIRS = {'__pycache__', '.git', '.idea', '.vscode', 'venv', 'env'}

# Extensiones de archivos que queremos leer (puedes agregar .txt, .md, .json, etc.)
VALID_EXTENSIONS = {'.py', '.md', '.txt', '.json'}

def get_tree_structure(startpath):
    """Genera una representación visual del árbol de directorios."""
    tree_str = "=== ESTRUCTURA DEL PROYECTO ===\n\n"
    
    for root, dirs, files in os.walk(startpath):
        # Filtrar directorios ignorados in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if any(f.endswith(ext) for ext in VALID_EXTENSIONS):
                tree_str += '{}{}\n'.format(subindent, f)
                
    tree_str += "\n" + "="*50 + "\n\n"
    return tree_str

def collect_files(startpath):
    """Lee el contenido de los archivos y los concatena."""
    content_str = "=== CONTENIDO DE LOS ARCHIVOS ===\n\n"
    
    for root, dirs, files in os.walk(startpath):
        # Filtrar directorios ignorados
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            # Verificar si es el archivo de salida o el mismo script para no incluirlos
            if file == OUTPUT_FILE or file == os.path.basename(__file__):
                continue

            # Verificar extensión válida
            if any(file.endswith(ext) for ext in VALID_EXTENSIONS):
                file_path = os.path.join(root, file)
                
                content_str += f"START_FILE: {file_path}\n"
                content_str += "-" * 50 + "\n"
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_str += f.read()
                except UnicodeDecodeError:
                    content_str += "[ERROR: No se pudo leer este archivo con codificación UTF-8]"
                except Exception as e:
                    content_str += f"[ERROR: {str(e)}]"
                    
                content_str += "\n" + "-" * 50 + "\n"
                content_str += f"END_FILE: {file_path}\n\n"
                
    return content_str

def main():
    root_dir = os.getcwd() # Obtiene la carpeta actual
    print(f"Escaneando proyecto en: {root_dir}")
    
    tree = get_tree_structure(root_dir)
    contents = collect_files(root_dir)
    
    full_report = tree + contents
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_report)
        
    print(f"¡Listo! Archivo generado exitosamente: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()