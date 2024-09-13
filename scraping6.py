import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# URL de la página inicial
url = 'https://onepiece.fandom.com/es/wiki/Especial:Todas'

# Inicializar una lista para almacenar los enlaces
todos_los_enlaces = []

# Función para obtener todos los enlaces de la página actual
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

# Empezar a iterar por todas las páginas
while url:
    # Hacer una solicitud HTTP a la página actual
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Obtener y almacenar todos los enlaces de la página actual
    enlaces_pagina = obtener_enlaces_pagina(soup)
    todos_los_enlaces.extend(enlaces_pagina)
    
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

# Guardar los enlaces en un archivo CSV usando pandas
df = pd.DataFrame(todos_los_enlaces, columns=['Enlace'])
df.to_csv('enlaces_onepiece.csv', index=False, encoding='utf-8')

print(f'Se guardaron {len(todos_los_enlaces)} enlaces en el archivo enlaces_onepiece.csv')
