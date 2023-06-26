import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import time

"""
Este código procesa una página web específica y extrae las noticias de ella. 
Primero, se realiza una solicitud HTTP y se verifica si la respuesta tiene un código de estado 200, 
lo que significa que la solicitud fue exitosa. Si es así, se decodifica el contenido HTML 
y se utiliza la biblioteca BeautifulSoup para analizar el contenido 
y encontrar los elementos HTML que contienen las noticias. Luego, se extraen los títulos 
y los enlaces de cada noticia y se agregan a una lista llamada "blocks_news". 
Este código es útil para extraer información de una página web específica y puede ser modificado para adaptarse 
a diferentes páginas web.
"""
def proces_html_tn(termino):
    response = requests.get('https://tn.com.ar/ultimas-noticias/')
    response.raise_for_status() # Manejo de excepciones en caso de fallo en la solicitud
    html_content = response.content.decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    bloques = soup.select('h2.card__headline') # Selección más eficiente de los elementos relevantes
    for news in bloques:
        titulo = news.find('a', title=True).get("title")
        link = 'https://tn.com.ar' + news.find('a', href=True).get("href")
        if termino in titulo:
            blocks_news.append({'medio': 'Todo Noticias', 'titulo': titulo, 'link': link}) # Agregar los títulos y enlaces directamente a la lista

def proces_html_ib(termino):
    response = requests.get('https://www.infobae.com/ultimas-noticias/')
    response.raise_for_status() # Manejo de excepciones en caso de fallo en la solicitud
    html_content = response.content.decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    bloque = soup.find_all('a', class_='d23-feed-list-card')
    for enlaces in bloque:
        link = 'https://www.infobae.com' + enlaces['href']
        sopita = enlaces.find('h2')
        titulo = sopita.text.strip()
        if termino in titulo:
            blocks_news.append({'medio': 'Infobae', 'titulo': titulo, 'link': link}) # Agregar los títulos y enlaces directamente a la lista
  
def proces_html_ln(termino):
    response = requests.get('https://www.lanacion.com.ar/ultimas-noticias/')
    response.raise_for_status() # Manejo de excepciones en caso de fallo en la solicitud
    html_content = response.content.decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    bloques = soup.select('section.mod-description') # Selección más eficiente de los elementos relevantes
    for news in bloques:     
        titulo = news.find('a', class_='com-link').text
        link = 'https://www.lanacion.com.ar' + news.find('a', class_='com-link')['href']
        if termino in titulo:
            blocks_news.append({'medio': 'La Nación', 'titulo': titulo, 'link': link}) # Agregar los títulos y enlaces directamente a la lista

def proces_html_a24(termino):
    response = requests.get('https://www.a24.com/ultimas-noticias')
    response.raise_for_status() # Manejo de excepciones en caso de fallo en la solicitud
    html_content = response.content.decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    bloques = soup.select('a.news-link') # Selección más eficiente de los elementos relevantes
    for news in bloques:     
        titulo = news.find('h2', class_='news-title').text
        link = news['href']

        if termino in titulo:
            blocks_news.append({'medio': 'A24', 'titulo': titulo, 'link': link}) # Agregar los títulos y enlaces directamente a la lista

# Definir variables
blocks_news = []
busqueda = " "
proces_html_ib(busqueda)
proces_html_tn(busqueda)
proces_html_ln(busqueda)
proces_html_a24(busqueda)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filtro = request.form['filtro']
        filtered_news = []
        for item_news in blocks_news:
            if filtro.lower() in item_news['titulo'].lower():
                filtered_news.append(item_news)
        return render_template('index.html', blocks_news=filtered_news, filtro=filtro)
    else:
        return render_template('index.html', blocks_news=blocks_news)


if __name__ == '__main__':
    app.run(debug=True)