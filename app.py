# =============================
# Importación de librerías
# =============================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import random

# =============================
# Configuración de la pestaña
# =============================
st.set_page_config(
    page_title="AO3 Ships",
    page_icon="🗃️"
)

# =============================
# Cargar y cachear el Excel con todas las hojas (2020–2024)
# =============================
@st.cache_data
@st.cache_data
def load_data():
    excel_path = Path("data/ships_data.xlsx")
    sheets = pd.read_excel(excel_path, sheet_name=None, header=0)
    return sheets

sheets = load_data()
YEARS = list(sheets.keys())

# =============================
# Cargar el archivo CSS personalizado
# =============================
def load_css():
    css_path = Path("css/style.css")
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =============================
# Definir la barra lateral interactiva con navegación
# =============================
def sidebar():
    st.markdown("""
    <div class="sidebar" style="margin-left: 10px;">
        <div class="sidebar-title-container">
            <a href="?page=Inicio" class="sidebar-title-box" style="text-decoration: none; color: white;">
                Shippeo en AO3
            </a>
        </div>
        <nav class="sidebar-nav">
            <a href="?page=Inicio">Inicio</a>
            <a href="?page=Random">Random</a>
            <a href="?page=Tipo">Tipo de relación</a>
            <a href="?page=Raza">Raza</a>
            <a href="?page=Listas">Ver listas completas</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)


# =============================
# Página de inicio con texto introductorio y tarjetas
# =============================
def show_inicio():
    st.markdown('<div class="page-header">Inicio<hr></div>', unsafe_allow_html=True)
    
    # Texto de bienvenida
    st.markdown("""
<p>¡Bienvenidos a nuestra página de tendencias en AO3! Este es un proyecto universitario hecho gracias al increíble trabajo de 
<a href="https://archiveofourown.org/series/1209645" target="_blank" style="color: #970A0A; font-weight: bold; text-decoration: none;">
centreofthelights</a>, quien viene recopilando los 100 ships con más fanfics de cada año desde 2013. Los datos que podrán ver en esta página corresponden al periodo de años entre 2020 y 2024, y se basan en el número de fanfics escritos.</p>

<p><strong>Para empezar, selecciona alguna de las opciones:</strong></p>

<ul>
  <li><strong>Random:</strong> ¡Empecemos con algo divertido! Aprieta el botón, y te aparecerá un ship random con el fandom al que pertenece, los años en los que estuvo en el top 100, y las posiciones que ocupó en esos años.</li>
  <li><strong>Tipo de relación:</strong> podrás ver las estadísticas de acuerdo a este tag. Los tipos de ship son:</li>
</ul>
""", unsafe_allow_html=True)

    # Ruta base a las imágenes de las tarjetas
    image_path = Path("images")

    # Fila 1: Gen | F/M | M/M
    col1, col2, col3, col4, col5 = st.columns(5)

    with col2:
        st.image(str(image_path / "gen.png"), width=180)
        st.markdown('<div class="mini-card"><div class="title">Gen</div><div class="desc">Fanfic no enfocado en una relación romántica</div></div>', unsafe_allow_html=True)

    with col3:
        st.image(str(image_path / "fm.png"), width=180)
        st.markdown('<div class="mini-card"><div class="title">F/M</div><div class="desc">Relación heterosexual</div></div>', unsafe_allow_html=True)

    with col4:
        st.image(str(image_path / "mm.png"), width=180)
        st.markdown('<div class="mini-card"><div class="title">M/M</div><div class="desc">Relación homosexual masculina</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila 2: F/F | Multi | Other
    col1b, col2b, col3b, col4b, col5b = st.columns(5)

    with col2b:
        st.image(str(image_path / "ff.png"), width=180)
        st.markdown('<div class="mini-card"><div class="title">F/F</div><div class="desc">Relación homosexual femenina</div></div>', unsafe_allow_html=True)

    with col3b:
        st.image(str(image_path / "multi.png"), width=180)
        st.markdown('<div class="mini-card"><div class="title">Multi o Poly</div><div class="desc">Varias relaciones, o relación en la que participan más de dos personas</div></div>', unsafe_allow_html=True)

    with col4b:
        st.image(str(image_path / "other.png"), width=180)
        st.markdown('<div class="mini-card"><div class="title">Other</div><div class="desc">Relaciones entre personajes que no encajan dentro de lo binario</div></div>', unsafe_allow_html=True)

    # Texto final de las secciones
    st.markdown("""
<ul>
  <li><strong>Raza:</strong> para apreciar mejor la diversidad en los fanfics.</li>
  <li><strong>Ver listas completas:</strong> podrás ver las tablas de clasificación originales según el año que selecciones.</li>
</ul>
""", unsafe_allow_html=True)

# =============================
# Página de tipo de relación
# =============================
def show_tipo(sheets, YEARS):
    st.markdown('<div class="page-header">Tipo de relación<hr></div>', unsafe_allow_html=True)

    # Texto introductorio
    st.markdown("""
    La mayoría de fanfics en AO3 son muy homosexuales. Pero, ¿de qué tipo de relación se han escrito más fanfics? A la derecha, podrás ver las estadísticas de cada tipo de relación a través del tiempo. A la izquierda, podrás seleccionar un tipo de relación, para ver su proporción con respecto a los otros.
    """)

    # Filtrar datos por tipo válido
    valores_validos = {"M/M", "F/F", "F/M", "Gen", "Poly", "Other"}
    datos_por_anio = {}

    for year in YEARS:
        df = sheets[year]
        try:
            columna = df["Type"].iloc[0:100]  # E2 a E101 si encabezado está en E1
            datos_filtrados = columna.astype(str).str.strip()
            datos_por_anio[year] = datos_filtrados[datos_filtrados.isin(valores_validos)].tolist()
        except Exception as e:
            datos_por_anio[year] = []

    total_datos = sum(datos_por_anio.values(), [])
    conteo_total = Counter(total_datos)

    # Layout: columna izquierda con selectbox y gráfico circular
    col1, col2 = st.columns([1, 2])

    with col1:
        opcion = st.selectbox("Selecciona un tipo de relación:", list(valores_validos))
        seleccion = conteo_total.get(opcion, 0)
        otros = sum(v for k, v in conteo_total.items() if k != opcion)

        # Gráfico pie chart comparando opción vs otras
        if seleccion + otros == 0:
            st.warning("No hay datos suficientes para generar este gráfico.")
        else:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(
                [seleccion, otros],
                labels=[opcion, "Otras categorías"],
                colors=["#970A0A", "#F1F0E7"],
                autopct='%1.1f%%',
                startangle=90,
                textprops=dict(color="black"),
                wedgeprops=dict(width=0.5)
            )
            ax.axis('equal')
            plt.title(f"Proporción acumulada: {opcion} vs otras categorías (2020–2024)")
            st.pyplot(fig)

    with col2:
        # Gráfico de línea mostrando evolución anual por tipo
        categorias = ['M/M', 'F/M', 'F/F', 'Gen', 'Other', 'Poly']
        colores = ['#970A0A', '#B1484A', '#BE676A', '#CB8589', '#D09094', '#D49A9E']
        conteo_anual = {cat: [] for cat in categorias}

        for anio in YEARS:
            conteo = Counter(datos_por_anio[anio])
            for cat in categorias:
                conteo_anual[cat].append(conteo.get(cat, 0))

        plt.figure(figsize=(10, 6))
        for cat, color in zip(categorias, colores):
            nombre = "Multi" if cat == "Poly" else cat
            plt.plot(YEARS, conteo_anual[cat], marker='o', label=nombre, color=color)

        plt.title("Evolución por categoría (2020–2024)")
        plt.xlabel("Año")
        plt.ylabel("Cantidad")
        plt.legend(title="Categorías")
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

    # Texto reflexivo final
    st.markdown("""
    <br><br>
    <p style="font-size: 16px;">
    ¿Viste que las relaciones homosexuales entre hombres (M/M) son de las que más se escriben? Originalmente, 
    <a href="https://archiveofourown.org/series/1209645" target="_blank" style="color: #970A0A; font-weight: bold; text-decoration: none;">
    centreofthelights</a> (la increíble persona detrás de las estadísticas) inició su investigación al detectar este problema. 
    ¿Es el hecho de que se escriban más fanfics gays, a comparación de lésbicos o con otras expresiones de género, 
    una manifestación del mandato de la hegemonía patriarcal a nivel global?
    </p>
    <p style="font-size: 16px;"><em>Hmm. Para pensar.</em></p>
    """, unsafe_allow_html=True)

# =============================
# Página de raza
# =============================
def show_raza(sheets, YEARS):
    st.markdown('<div class="page-header">Raza<hr></div>', unsafe_allow_html=True)

    # Texto introductorio
    st.markdown("""
    <p style="font-size: 16px;">
    Primero lo primero: entre seres humanos, no existe más raza que la humana. Cualquier persona que opine lo contrario puede apretar <strong>alt+F4</strong> para cargar una versión de página que esté de acuerdo con sus ideas.
    </p>

    <p style="font-size: 16px;">
    En segundo lugar, somos totalmente conscientes de que no todos los seres en historias ficticias son humanos. Pero, esos seres han sido <em>creados por <strong>humanos</strong></em>. Esto implica que los seres humanos cuentan historias sobre otros seres no humanos que <em>se comportan</em> como seres humanos. En consecuencia, las categorías que se aplican sobre distintos grupos de personas según su color de piel o procedencia también se repiten en la ficción.
    </p>

    <p style="font-size: 16px;">
    En fin, dejemos de lado lo académico y veamos si al fin nuestros idols lograron vencer a los ships blancos.
    </p>
    """, unsafe_allow_html=True)

    # Construcción de diccionario con la combinación de columnas F y G
    datos_por_anio = {}

    for year in YEARS:
        df = sheets[year]
        try:
            col_f = df.iloc[1:101, 5]  # columna F, desde la fila 2 a 101 (índice 1 a 100)
            col_g = df.iloc[1:101, 6]  # columna G, mismo rango
            combinados = (col_f.fillna("Unknown").astype(str).str.strip() + "-" +
                          col_g.fillna("Unknown").astype(str).str.strip())
            datos_por_anio[year] = combinados.tolist()
        except Exception as e:
            st.error(f"Error procesando el año {year}: {e}")
            datos_por_anio[year] = []

    # Conteo acumulado y gráfico de líneas para top 2 + otras
    conteo_acumulado = defaultdict(lambda: defaultdict(int))
    for anio in sorted(datos_por_anio.keys()):
        conteo_anual = Counter(datos_por_anio[anio])
        for pareja, cantidad in conteo_anual.items():
            conteo_acumulado[pareja][anio] = cantidad

    parejas_totales = list(conteo_acumulado.keys())
    anios = sorted(datos_por_anio.keys())
    conteo_ordenado = {
        pareja: [conteo_acumulado[pareja].get(anio, 0) for anio in anios]
        for pareja in parejas_totales
    }

    totales = {pareja: sum(valores) for pareja, valores in conteo_ordenado.items()}
    top_2 = sorted(totales, key=totales.get, reverse=True)[:2]

    fig, ax = plt.subplots(figsize=(14, 8))
    colores_extra = ['#B1484A', '#B3AD6B', '#BE676A', '#BAB478', '#CB8589', '#C1BC86', '#F1F0E7', '#CAC6A5']
    extras_idx = 0

    for pareja, conteos in sorted(conteo_ordenado.items(), key=lambda x: totales[x[0]], reverse=True):
        if pareja == top_2[0]:
            color = '#970A0A'
        elif pareja == top_2[1]:
            color = '#100007'
        else:
            color = colores_extra[extras_idx % len(colores_extra)]
            extras_idx += 1
        ax.plot(anios, conteos, marker='o', label=pareja, color=color)

    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de repeticiones")
    ax.set_title("Conteo de parejas por raza del 2020 al 2024")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    ax.set_yticks(np.arange(0, max(max(v) for v in conteo_ordenado.values()) + 2, 2))
    plt.tight_layout()
    st.pyplot(fig)

    # Texto intermedio
    st.markdown("""
    <p style="font-size: 16px;">
    ...bueno, van en camino. De todos modos, AO3 es principalmente usado por personas angloparlantes. ¡La mayoría de fanfics están en inglés! Si hubiera más gente latina, probablemente las cifras subirían. Otra cifra que probablemente sería mayor es la de ships con personajes latinoamericanos... les dejamos ahí el encargo de hacer que suba.
    </p>

    <p style="font-size: 16px;">
    Por otro lado, los White y los Asian no han dejado brillar al resto, ¿no? Entonces, aquí debajo un gráfico con todos ellos:
    </p>
    """, unsafe_allow_html=True)

    # Gráfico de barras horizontales: 15 parejas menos frecuentes
    total_conteo = Counter()
    for lista in datos_por_anio.values():
        total_conteo.update(lista)

    menos_comunes = sorted(total_conteo.items(), key=lambda x: x[1])[:15]
    parejas, cantidades = zip(*menos_comunes)
    colores_barras = [
        '#970A0A', '#A4292A', '#B1484A', '#BE676A', '#CB8589', '#D09094', '#D39B9C',
        '#D6A5A3', '#D9B0AA', '#DBBAB1', '#DEC5B9', '#E1CFC0', '#E4DAC7', '#E6E4CE', '#E6DDCC'
    ]

    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    ax_bar.barh(parejas, cantidades, color=colores_barras)
    ax_bar.set_xlabel("Frecuencia total (2020–2024)")
    ax_bar.set_title("15 parejas menos frecuentes entre 2020 y 2024")
    ax_bar.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_bar)

    # Texto final
    st.markdown("""
    <p style="font-size: 16px;">
    Están bien parejos, pero no llegan ni a los diez. Ahora, ¿esto tendrá que ver con prejuicios personales de quien escribe fanfics? ¿O tendrá que ver más con el tipo de personajes representados en las historias? 
    </p>
    <p style="font-size: 16px;">
    Con esta sección, y la anterior, buscamos que se hagan estas y más preguntas. ¡Denles vueltas en su cabeza! Es lo mínimo que se puede hacer, a menos que tú seas quien escribe las historias. Y en ese caso... ¡puedes ser el cambio y darles más representación a estos grupos!
    </p>
    """, unsafe_allow_html=True)

# =============================
# Página Ver listas completas
# =============================
def show_listas(sheets, YEARS):
    st.markdown('<div class="page-header">Listas completas<hr></div>', unsafe_allow_html=True)

    # Texto introductorio
    st.markdown("""
    <p style="font-size: 16px;">
    ¡Un alma curiosa! No creíste que era suficiente con ver los datos presentados en gráficos y quieres la data real.
    ¡Pues aquí está! Si quieres, la puedes encontrar en AO3 directamente 
    <a href="https://archiveofourown.org/series/1209645" target="_blank" style="color: #970A0A; font-weight: bold; text-decoration: none;">aquí</a>. 
    Pero, si AO3 aún te parece confuso, puedes ver las tablas aquí mismo. Solo selecciona el año en la lista desplegable.
    </p>
    """, unsafe_allow_html=True)

    # Lista desplegable para seleccionar año
    year_selected = st.selectbox("Selecciona un año:", YEARS, index=0)
    df = sheets[year_selected].copy()

    # Unir columnas "Race" y "Unnamed: 6"
    df["Races"] = df["Race"].astype(str).str.strip() + " – " + df["Unnamed: 6"].astype(str).str.strip()
    df.drop(columns=["Race", "Unnamed: 6"], inplace=True)

    # Renombrar columna Total Works como "Total"
    if "Total Works" in df.columns:
        df.rename(columns={"Total Works": "Total"}, inplace=True)

    # Mostrar tabla interactiva
    st.dataframe(df, use_container_width=True, height=3502)

# =============================
# Página Random: ship aleatorio
# =============================
def show_random(sheets, YEARS):
    st.markdown('<div class="page-header">Random<hr></div>', unsafe_allow_html=True)

    # Recorrer todos los años y juntar los datos de cada ship
    todos_los_ships = []

    for year in YEARS:
        df = sheets[year]
        for i in range(1, min(101, len(df))):
            nombre = str(df.iloc[i, 1]).strip()  # Columna B = Relationship
            fandom = str(df.iloc[i, 2]).strip()  # Columna C = Fandom
            puesto = str(df.iloc[i, 0]).strip()  # Columna A = Rank

            if nombre.lower() == 'nan' or fandom.lower() == 'nan':
                continue

            todos_los_ships.append({
                "ship": nombre,
                "fandom": fandom,
                "year": year,
                "rank": f"#{puesto}"
            })


    # Agrupar por ship
    agrupados = {}
    for item in todos_los_ships:
        nombre = item["ship"]
        if nombre not in agrupados:
            agrupados[nombre] = {"fandom": item["fandom"], "years": [], "ranks": []}
        agrupados[nombre]["years"].append(str(item["year"]))
        agrupados[nombre]["ranks"].append(item["rank"])

    # Mostrar dos columnas
    col1, col2 = st.columns([1, 2])

    # Botón para seleccionar aleatoriamente un ship
    with col1:
        st.write("")
        st.write("")
        st.write("")
        if st.button("¡Prueba tu suerte!"):
            st.session_state.ship_aleatorio = random.choice(list(agrupados.items()))

    # Mostrar ficha del ship seleccionado
    with col2:
        ship_data = st.session_state.get("ship_aleatorio", None)
        if ship_data:
            nombre, info = ship_data
            st.markdown(f"""
                <div style="
                    border: 2px solid #970A0A;
                    border-radius: 10px;
                    padding: 20px;
                    background-color: #FCFCFF;
                    color: #100007;
                ">
                    <h3 style="text-align: center; color: #970A0A;">{nombre}</h3>
                    <ul style="font-size: 16px;">
                        <li><strong>Fandom:</strong> {info['fandom']}</li>
                        <li><strong>Año:</strong> {', '.join(info['years'])}</li>
                        <li><strong>Puesto:</strong> {', '.join(info['ranks'])}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# =============================
# Sistema de ruteo principal
# =============================
def main():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    load_css()
    sidebar()

    query = st.query_params
    page = query.get("page", "Inicio")

    if page == "Inicio":
        show_inicio()
    elif page == "Random":
        show_random(sheets, YEARS)
    elif page == "Tipo":
        show_tipo(sheets, YEARS)
    elif page == "Raza":
        show_raza(sheets, YEARS)
    elif page == "Listas":
        show_listas(sheets, YEARS)
    elif page.startswith("Tipo-"):
        tipo = page[5:]
        st.markdown(f'<div class="page-header">Tipo de relación: {tipo}<hr></div>', unsafe_allow_html=True)
        st.write("Sección en desarrollo...")
    elif page.startswith("List-"):
        year = page[5:]
        st.markdown(f'<div class="page-header">{year}<hr></div>', unsafe_allow_html=True)
        st.write("Esta tabla fue elaborada por centerofthelights:")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# PUNTO DE ENTRADA
# =============================
if __name__ == "__main__":
    main()
