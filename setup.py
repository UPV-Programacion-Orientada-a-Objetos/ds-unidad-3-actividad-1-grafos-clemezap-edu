"""
setup.py - Script de compilación para NeuroNet
Compila el código C++ y genera la extensión Python usando Cython
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import os

# Configuración para diferentes plataformas
extra_compile_args = []
extra_link_args = []

if sys.platform == 'win32':
    # Windows (MSVC)
    extra_compile_args = ['/O2', '/std:c++14']
elif sys.platform == 'darwin':
    # macOS
    extra_compile_args = ['-std=c++14', '-O3', '-stdlib=libc++']
    extra_link_args = ['-stdlib=libc++']
else:
    # Linux y otros Unix
    extra_compile_args = ['-std=c++14', '-O3']

# Definir la extensión
extensions = [
    Extension(
        name="neuronet",
        sources=[
            "neuronet.pyx",      # Wrapper Cython
            "graph_core.cpp"      # Implementación C++
        ],
        include_dirs=["."],       # Directorio actual para headers
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

# Configurar el paquete
setup(
    name="neuronet",
    version="1.0.0",
    description="Sistema híbrido C++/Python para análisis de grafos masivos",
    author="NeuroNet Team",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",  # Python 3
            'embedsignature': True,  # Documentación en firmas
        }
    ),
    zip_safe=False,
)

print("\n" + "="*60)
print("  Compilación de NeuroNet completada exitosamente")
print("="*60)
print("\nPara usar el módulo, ejecuta:")
print("  python main_gui.py")
print("="*60 + "\n")