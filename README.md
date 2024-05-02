# Evidencia Final Compiladores: Traductor de Flujos de Imagen

## Integrantes
- Sebastián González Villacorta - A01029746

    [Video Reflexión Personal](https://drive.google.com/file/d/15WJpszDJaztdohZ5SAzHtjiyj4yvEniJ/view?usp=drive_link)
- Andreína

    [Video Reflexión Personal]()
- Luis Javier

    [Video Reflexión Personal]()
## Objetivo

El objetivo de este proyecto es implementar una traductor que permita aceptar expresiones de lenguaje como aritmética básica, asignación de variables, manejo de string y condicionales; así como diseñar flujos de trabajo con imágenes, facilitando así el acceso a funciones de filtrado y procesamiento de imágenes de OpenCV.

## Desarrollo

La herramienta permite:

- Facilitar el acceso a funciones de filtrado y procesamiento de imágenes de OpenCV.
- Implementar flujos de transformaciones en imágenes a través de secuencias del lenguaje.
- Exportar los resultados del procesamiento de una imagen con un archivo de salida.

## Método

El proyecto se desarrollo utilizando la herramienta de Python ply, la cual permite, con la ayuda de lex y yacc, el desarrollo de un compilador o traductor. Asímismo se utilizo Graphviz en conjunto con networkkx para la visualización del árbol de sintaxis. Se integró también, como parte de a funcionalidad, la posibilidad de utilizar funciones externas de la librería OpenCV.

## Cómo Empezar

1. Clone el repositorio:
```bash
git clone "https://github.com/asananez2000/evidencia-compiladores.git"
```

2. Navegue al directorio de compiler:
```bash
cd evidencia-compiladores/compiler
```

3. Instale las dependencias necesarias:
> Asegurese de tener [Python](https://www.python.org/downloads/) y [pip](https://pip.pypa.io/en/stable/installation/) instalados.
```bash
pip install -r "requirements.txt"
```
4. Instale [Graphviz](https://graphviz.org/download/) para poder visualizar el grafo.

4. Ejecute el script principal para ver una demostración:
```bash
python translator.py
```

## Tests

El repositorio incluye tests automatizados para validar todas las reglas de la gramática implementada y las funciones que no provienen de bibliotecas externas. Para ejecutar los tests, use el siguiente comando:
```bash
pytest
```

## Reglas del Traductor Implementadas

En esta sección se listan de manera general las reglas implementadas en el traductor:

- 📝 **Asignaciones**: Permite asignar valores a variables o resultados de expresiones a variables.
- 🔍 **Operaciones Aritméticas**: Soporta operaciones básicas como suma (`+`), resta (`-`), multiplicación (`*`) y división (`/`).
- 🔢 **Comparaciones**: Incluye operadores de comparación como mayor que (`>`), menor que (`<`), igual (`==`), diferente (`!=`), mayor o igual (`>=`), y menor o igual (`<=`).
- 🔄 **Operadores Lógicos**: Implementa operadores lógicos AND (`&&`) y OR (`||`) para combinar condiciones.
- 📂 **Acceso a Funciones de Imágenes**: Facilita el acceso a funciones específicas de OpenCV para cargar, guardar, y mostrar imágenes, además de otras funciones de procesamiento avanzado.
- 🔄 **Condicionales**: Soporta instrucciones condicionales `if` `else` y operación ternaria `?` `:` para ejecutar diferentes bloques de código basados en condiciones.
- 🧮 **Funciones Matemáticas y de Transformación**: Permite llamar funciones para manipular matrices y vectores, crucial para el procesamiento de datos de imágenes.
- 🖼️ **Flujos de Trabajo con Imágenes**: Permite definir y ejecutar secuencias de transformaciones y análisis de imágenes, leyendo los comandos desde archivos o entradas de usuario.

Estas reglas están diseñadas para ser flexibles y potentes, permitiendo a los desarrolladores crear flujos de trabajo complejos con facilidad.

## Sumatoria de puntos

En el presente entregable, se desarrollaron los elementos que resultan en la siguiente sumatoria de puntos:

| Característica | Puntaje |
|----------|----------|
| Implementar condicionales   | 75 | 
| Implementación de pruebas automatizadas | 25 | 
| Todas las tareas entregadas (Todo el equipo cuenta con puntaje completo)   | 15 | 
||= 115