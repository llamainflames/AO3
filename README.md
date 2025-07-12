# 📦 AO3 Ships: Tendencias de fanfics 2020–2024

Este es un proyecto académico desarrollado como trabajo final para el curso **Pensamiento Computacional para Comunicaciones**, de la Facultad de Ciencias y Artes de la Comunicaciones. La aplicación permite explorar de manera visual, clara y accesible las tendencias en fanfiction romántico (ships) dentro de **AO3 (Archive of Our Own)** durante el periodo **2020–2024**.

Gracias a la recopilación de datos de [centreofthelights](https://archiveofourown.org/series/1209645), se han analizado los 100 ships más populares de cada año, y clasificado según su tipo de relación y la raza de los personajes.

## 🚀 ¿Qué hace esta app?

La aplicación permite:

- 📊 Visualizar la **evolución temporal** de los tipos de relación (M/M, F/F, F/M, Gen, Poly, Other).
- 🧬 Explorar la **diversidad racial** de los ships más populares.
- 📝 Consultar las **listas completas** año por año.
- 🎲 Obtener un **ship aleatorio** con información de fandom, años y posiciones.
  
Todo se presenta de forma interactiva a través de una **barra lateral de navegación**, gráficos y tablas.

## 🧰 Tecnologías utilizadas

- [Streamlit](https://streamlit.io/): para crear la interfaz de usuario.
- [Pandas](https://pandas.pydata.org/): para manipulación de datos.
- [Matplotlib](https://matplotlib.org/): para visualizaciones.
- [NumPy](https://numpy.org/): operaciones matemáticas.
- [Pillow](https://python-pillow.org/): para mostrar imágenes.
- [CSS personalizado](css/style.css): para dar formato visual a la aplicación.

## 🗃️ Estructura del proyecto
📁 AO3-Ships
├── app.py ← Código principal en Streamlit
├── data/
│ └── ships_data.xlsx ← Archivo Excel con los datos 2020–2024
├── css/
│ └── style.css ← Estilo visual personalizado
├── images/
│ └── *.png ← Íconos de categorías
├── requirements.txt ← Dependencias necesarias
└── README.md ← Este archivo

## 📊 Datos utilizados

Todos los datos fueron recopilados por el usuario [centreofthelights](https://archiveofourown.org/series/1209645), quien publica anualmente el ranking de los 100 ships más populares en AO3.  
Este proyecto **no almacena contenido de fanfics**, solo utiliza sus metadatos (nombre del ship, fandom, tipo de relación, raza, etc.) de manera agregada **con fines educativos**.

## ⚠️ Licencia y uso

Este proyecto es de **uso educativo** y **no tiene fines comerciales**.  
El contenido analizado pertenece a usuarios de AO3 y ha sido procesado respetando la política de uso de datos del sitio.
