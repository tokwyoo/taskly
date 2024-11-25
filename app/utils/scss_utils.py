import os
import sass

def compile_scss(input_file, output_file):
    """Compila un archivo SCSS a CSS"""
    compiled_css = sass.compile(filename=input_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(compiled_css)

def compile_all_scss(scss_folder, css_folder):
    """Compila todos los archivos SCSS en un directorio y genera archivos CSS correspondientes"""
    for filename in os.listdir(scss_folder):
        if filename.endswith(".scss"):
            input_file = os.path.join(scss_folder, filename)
            output_file = os.path.join(css_folder, filename.replace(".scss", ".css"))
            compile_scss(input_file, output_file)
            print(f"Compilado {filename} a {output_file}")

# Llamar a la función para compilar todos los archivos SCSS en la carpeta
if __name__ == "__main__":
    scss_folder = "static/scss"  # Carpeta con tus archivos SCSS
    css_folder = "static/css"    # Carpeta donde se guardarán los archivos CSS compilados
    
    compile_all_scss(scss_folder, css_folder)
