# Ruta sencilla para aprender con los proyectos

El objetivo no es memorizar todo el código. Debes entender qué problema resuelve
cada programa, ejecutarlo, cambiar una cosa pequeña y explicar el resultado.

## Proyecto 1: Monitor de integridad de archivos

**Problema:** si alguien modifica un archivo importante, necesitamos detectarlo.

**Idea principal:** el programa calcula una huella SHA-256 de cada archivo. Si el
contenido cambia, también cambia la huella.

Qué debes practicar:

1. Crear una línea base de una carpeta de ejemplo.
2. Modificar, añadir y eliminar un archivo.
3. Ejecutar la verificación y reconocer los tres cambios.
4. Leer una prueba automática y explicar qué comprueba.

Mejora para hacer tú mismo: añadir una opción que ignore extensiones como `.tmp`.

## Proyecto 2: Analizador de correos sospechosos

**Problema:** un correo puede intentar engañarnos mediante el remitente, los
enlaces o un mensaje urgente.

**Idea principal:** el programa abre un archivo `.eml` como datos; no visita sus
enlaces. Después aplica reglas sencillas y muestra evidencias.

Qué debes practicar:

1. Analizar el correo ficticio incluido.
2. Identificar qué regla produjo cada aviso.
3. Cambiar el correo para eliminar una señal y volver a ejecutarlo.
4. Explicar por qué un aviso no demuestra por sí solo que exista phishing.

Mejora para hacer tú mismo: añadir una regla para archivos adjuntos ejecutables.

## Proyecto 3: Analizador de logs SSH

**Problema:** muchos intentos de acceso en poco tiempo pueden indicar un ataque.

**Idea principal:** el programa convierte líneas de log en eventos y busca
patrones dentro de ventanas de tiempo.

Qué debes practicar:

1. Ejecutar el log de ejemplo.
2. Encontrar en el archivo las líneas que generaron cada alerta.
3. Explicar la diferencia entre fuerza bruta y password spraying.
4. Cambiar un dato de ejemplo y observar cómo cambia el resultado.

Mejora para hacer tú mismo: permitir configurar los umbrales desde la terminal.

## Cómo hablar de ellos en una entrevista

Usa esta estructura para cada proyecto:

1. **Problema:** qué situación de seguridad querías detectar.
2. **Decisión:** por qué elegiste esa solución sencilla.
3. **Prueba:** cómo comprobaste que funciona y evita errores básicos.
4. **Limitación:** qué no puede hacer todavía.
5. **Siguiente paso:** una mejora concreta que implementarías.

No afirmes que son herramientas listas para producción. Son proyectos educativos
reproducibles que demuestran fundamentos, capacidad de prueba y aprendizaje.
