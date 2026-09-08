# DS-Online-Emilio-Garrote
Repositorio del Bootcamp de Data Science + IA — material, ejercicios y prácticas.

## Resumen
Este repositorio contiene los Sprints, ejercicios, notebooks y proyectos utilizados durante el curso. Está organizado por sprints y unidades para facilitar el seguimiento y la entrega de ejercicios.

## Estructura principal (destacada)
- **Projects/**: Proyectos independientes y entregables (p. ej. Project_Break_I, Project_Break_II).
- **Sprints/**: Contiene los sprints del curso, cada uno con sus unidades y ejercicios.
	- `Sprint_01`, `Sprint_02`, ... `Sprint_18` (cada sprint puede contener varias unidades).
	- Dentro de cada `Sprint_##` las unidades suelen seguir este patrón:
		- `Unidad_XX_<Nombre>/`
			- `01_Workout/` — notebooks de ejercicios guiados
			- `02_Ejercicios_Workout/` — ejercicios para practicar
			- `03_Practica_Obligatoria/` — prácticas evaluables
			- Otras carpetas específicas (p. ej. `03_Live_Session`, `04_Ejercicios_Extra`)
- **Masterclasses/**: Notebooks y material de masterclasses (p. ej. Git/GitHub).
- **Sprints/.../Team_Challenges/**: Retos en equipo con notebooks y recursos (ej., Hundir la Flota).

Ejemplo: [Sprints/Sprint_01/](Sprints/Sprint_01/)

## Convenciones y buenas prácticas
- Nombres: usar `Sprint_##` y `Unidad_##_<Nombre>` para consistencia.
- Notebooks: mantén nombres descriptivos y añade una celda inicial con objetivos y requisitos de kernel.
- Datos: los ficheros grandes o datos descargables deben almacenarse en subcarpetas `data/` o enlazarse desde `README` de la unidad.

## Cómo usar este repositorio
1. Clonar el repositorio.
2. Abrir el directorio en VS Code o JupyterLab.
3. Seleccionar el kernel Python adecuado (recomendado: crear un entorno virtual con las dependencias del curso).
4. Navegar a `Sprints/` → elegir sprint → abrir la unidad y ejecutar los notebooks en orden: `01_Workout` → `02_Ejercicios_Workout` → `03_Practica_Obligatoria`.

Comandos útiles:

```powershell
# Crear y activar entorno virtual (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # si existe
```

## Contribuciones y actualizaciones
- Si añades material, respeta la estructura `Sprint_XX/Unidad_YY/` y actualiza el `README` de la unidad.
- Para cambios mayores, abre una rama nueva y crea un Pull Request describiendo el contenido.

## Contacto
Para dudas o propuestas, contacta a Emilio (autor del repositorio) o abre un issue en este repositorio.

---
Fecha de actualización: abril de 2026
