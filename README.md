# Requerimientos
pip install requests beautifulsoup4 pandas


Prompt:

de este sitio: https://onepiece.fandom.com/es/wiki/Tony_Tony_Chopper/Habilidades_y_poderes#Arm_Point , quiero almacenar en csv toda la información del mismo, estructurando el csv con los titulos <h1><h2><h3> <ul> de cada campo como el nombre de cada campo, y las etiquetas <p> <div> <li> todas las que se encuentra anidadas como el contenido del campo (solo el texto) sin los enlaces url. Luego borrar los espacios en blancos, tabulados, campos Unknown y palabras repetidas. se realizaria la extracción utilizando python y BeautifulSoup y pandas, mostrame el codigo completo. La extracción se realiza hasta encontrar el campo "Enlaces externos, id="Enlaces_externos"