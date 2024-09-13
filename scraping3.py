import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL de la página especial donde se listan todas las páginas
base_url = 'https://onepiece.fandom.com/es/wiki/Especial:Todas'

# Función para obtener los enlaces de las páginas desde una página paginada
def obtener_enlaces_pagina(url):
    enlaces = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todos los enlaces de la lista de páginas
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/es/wiki/'):
            full_url = 'https://onepiece.fandom.com' + href
            enlaces.append(full_url)
    
    return enlaces

# Función para obtener todas las páginas desde las diferentes paginaciones
def obtener_todas_las_paginas(base_url):
    todas_las_paginas = []
    url_actual = base_url

    while url_actual:
        # Obtener enlaces de la página actual
        enlaces_pagina = obtener_enlaces_pagina(url_actual)
        todas_las_paginas.extend(enlaces_pagina)

        # Encontrar el enlace de la siguiente página (si existe)
        soup = BeautifulSoup(requests.get(url_actual).content, 'html.parser')
        next_link = soup.find('a', {'class': 'category-page__pagination-next'})  # Ajustar según sea necesario
        if next_link:
            url_actual = 'https://onepiece.fandom.com' + next_link['href']
        else:
            url_actual = None
    
    # Eliminar duplicados de enlaces
    return list(set(todas_las_paginas))

# Función para extraer el contenido de una página dada
def extraer_contenido(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer el título principal de la página
    titulo_principal = soup.find('h1').text.strip() if soup.find('h1') else 'Sin Título'

    # Extraer los subtítulos (h2, h3, etc.)
    subtitulos = []
    for subtitulo in soup.find_all(['h2', 'h3', 'h4']):
        subtitulos.append(subtitulo.text.strip())
    
    return titulo_principal, subtitulos

# Obtener enlaces de todas las páginas listadas en la sección "Especial:Todas"
enlaces_todas_paginas = obtener_todas_las_paginas(base_url)

# Crear listas para almacenar los datos
titulos = []
todos_subtitulos = []
enlaces_visitados = []

# Limitar el número de páginas para evitar excesos durante las pruebas
limite_paginas = 100  # Limite ajustable

# Recorrer los enlaces obtenidos y extraer el contenido de cada página
for i, enlace in enumerate(enlaces_todas_paginas):
    if i >= limite_paginas:
        break  # Limitar el número de páginas por seguridad
    if enlace not in enlaces_visitados:
        try:
            titulo, subtitulos = extraer_contenido(enlace)
            titulos.append(titulo)
            todos_subtitulos.append(subtitulos)
            enlaces_visitados.append(enlace)
            print(f'Página {i + 1}: {titulo} - {enlace}')
        except Exception as e:
            print(f'Error al extraer contenido de {enlace}: {e}')
        # Pausa para evitar sobrecargar el servidor
        time.sleep(1)

# Crear un dataframe de pandas con los datos extraídos
df = pd.DataFrame({
    'Título': titulos,
    'Subtítulos': [', '.join(subs) for subs in todos_subtitulos],
    'URL': enlaces_visitados
})

# Guardar los datos en un archivo CSV
df.to_csv('onepiece_wiki_paginas.csv', index=False, encoding='utf-8')

print("Datos exportados a onepiece_wiki_paginas.csv")

