import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# URL de la página especial donde se listan todas las páginas
base_url = 'https://onepiece.fandom.com/es/wiki/Especial:Todas'

# Inicializar listas para almacenar datos
todos_los_enlaces = []
titulos = []
todos_subtitulos_y_contenidos = []
enlaces_visitados = []

# Función para obtener los enlaces de las páginas desde una página paginada
def obtener_enlaces_pagina(soup):
    enlaces = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/es/wiki/'):
            full_url = 'https://onepiece.fandom.com' + href
            enlaces.append(full_url)
    return enlaces

# Función para buscar el enlace "Página siguiente"
def obtener_enlace_siguiente(soup):
    return soup.find('a', string=re.compile('Página siguiente'))

# Función para extraer el contenido de una página dada
def extraer_contenido(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer el título principal de la página
    titulo_principal = soup.find('h1').text.strip() if soup.find('h1') else 'Sin Título'

    # Inicializar una lista para almacenar los subtítulos y sus contenidos asociados
    subtitulos_y_contenidos = []

    # Extraer los subtítulos (h2, h3, h4) y sus párrafos <p> asociados
    for header in soup.find_all(['h2', 'h3', 'h4']):
        subtitulo = header.text.strip()
        contenido_asociado = []
        
        # Buscar los párrafos <p> que estén después de este subtítulo
        siguiente_elemento = header.find_next_sibling()
        while siguiente_elemento and siguiente_elemento.name == 'p':
            contenido_asociado.append(siguiente_elemento.text.strip())
            siguiente_elemento = siguiente_elemento.find_next_sibling()

        # Combinar el subtítulo con su contenido en una sola entrada
        subtitulos_y_contenidos.append(f"{subtitulo}: {' '.join(contenido_asociado)}")

    # Combinar subtítulos y sus contenidos en una sola cadena
    contenido_organizado = ' | '.join(subtitulos_y_contenidos)

    return titulo_principal, contenido_organizado

# Empezar a iterar por todas las páginas
url = base_url
limite_paginas = 100000000  # Ajustar límite si es necesario
contador = 0

while url and contador < limite_paginas:
    # Hacer una solicitud HTTP a la página actual
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Obtener y almacenar todos los enlaces de la página actual
    enlaces_pagina = obtener_enlaces_pagina(soup)
    todos_los_enlaces.extend(enlaces_pagina)

    # Recorrer los enlaces obtenidos y extraer el contenido de cada página
    for enlace in enlaces_pagina:
        if enlace not in enlaces_visitados:
            try:
                titulo, contenido_organizado = extraer_contenido(enlace)
                titulos.append(titulo)
                todos_subtitulos_y_contenidos.append(contenido_organizado)
                enlaces_visitados.append(enlace)
                print(f'Página {contador + 1}: {titulo} - {enlace}')
                contador += 1
                if contador >= limite_paginas:
                    break
            except Exception as e:
                print(f'Error al extraer contenido de {enlace}: {e}')
            # Pausa para evitar sobrecargar el servidor
            time.sleep(1)
    
    # Buscar el enlace a la siguiente página
    enlace_siguiente = obtener_enlace_siguiente(soup)
    
    if enlace_siguiente:
        # Extraer el href (URL relativa) del enlace "Página siguiente"
        href_siguiente = enlace_siguiente['href']
        url = 'https://onepiece.fandom.com' + href_siguiente
        print(f'Moviéndose a la siguiente página: {url}')
    else:
        # No se encontró "Página siguiente", detener la iteración
        print('No se encontró más el enlace "Página siguiente".')
        url = None

# Eliminar duplicados de enlaces
todos_los_enlaces = list(set(todos_los_enlaces))

# Crear un dataframe de pandas con los datos extraídos
df = pd.DataFrame({
    'Título': titulos,
    'Subtítulos y Contenidos': todos_subtitulos_y_contenidos,
    'URL': enlaces_visitados
})

# Guardar los datos en un archivo CSV
df.to_csv('onepiece_wiki_paginas.csv', index=False, encoding='utf-8')

print(f"Se guardaron {len(enlaces_visitados)} enlaces en el archivo onepiece_wiki_paginas.csv")
