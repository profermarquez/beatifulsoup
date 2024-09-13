import requests
from bs4 import BeautifulSoup
import re

# URL de la página inicial
url = 'https://onepiece.fandom.com/es/wiki/Especial:Todas'

# Hacer una solicitud HTTP a la página
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar el enlace que contiene "Página siguiente" en cualquier parte del texto usando una expresión regular
enlace_siguiente = soup.find('a', string=re.compile('Página siguiente'))

if enlace_siguiente:
    # Extraer el href (URL relativa) del enlace
    href_siguiente = enlace_siguiente['href']
    full_url = 'https://onepiece.fandom.com' + href_siguiente
    print(f'El enlace "Página siguiente" apunta a: {full_url}')

    # Hacer una nueva solicitud HTTP a la siguiente página
    siguiente_pagina = requests.get(full_url)
    siguiente_soup = BeautifulSoup(siguiente_pagina.content, 'html.parser')
    
    # Aquí puedes continuar procesando la siguiente página
    print("Contenido de la siguiente página obtenido exitosamente.")
else:
    print('No se encontró el enlace "Página siguiente".')


