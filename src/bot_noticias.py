#!/ust/bin/env python3
#-*- coding: utf-8 -*-

from bot import BotTelegram

# Import KEYS API
from config.keys import API_NEWS_KEY
# Import NEWSAPI
from newsapi import NewsApiClient

# Import acortador de URL

from pyshorteners import Shortener

# Init NEWSAPI
newsapi = NewsApiClient(api_key=API_NEWS_KEY)

# Init shortener
shortener = Shortener()
tinyurl = shortener.tinyurl.short

class BotNoticias(BotTelegram):
    """Clase que hereda de BotTelegram, añadiendo los métodos para un bot de noticias Argentinas"""
    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)

    def start(self, update, context):
        """ Esta función realiza una presentación cuando se ejecuta el comando '/start'."""
        self.logger.info('He recibido el comando start')
        context.bot.send_message(
            chat_id = update.message.chat_id,
            text = "Bienvenido al Bot de Noticias de Argentina, puedes usar '/ayuda' \npara ver los comandos"
        )

    def ayuda(self, update, context):
        """ Muestra los comandos más importantes """
        self.logger.info('He recibido el comando ayuda')
        context.bot.send_message(
            chat_id = update.message.chat_id,
            text = """Los comandos que pueden ayudarte son:
        /seccion - Busca las noticias por sección
        /clima - Te proporciona los dos climáticos en argentina (Próximamente)
        /top5 - Devuelve las 5 noticias más relevantes del momento
        
        Además, escribiendo palabras claves, recibes una noticia relacionada a ese palabra. """)

    def top_noticias(self, update, context):
        """ Devuelve las 5 noticias más importantes del momento en Argentina"""
        self.logger.info('He recibido el comando top5')
        
        top5_noticias = newsapi.get_top_headlines(
                                        language='es',
                                        country='ar',
                                        page_size=5)
        for articulo in top5_noticias['articles']:  
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = tinyurl(articulo['url']))
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Título: {} \nAutor: {}".format(articulo['title'], articulo['author']))
        
    def noticia_por_tema(self, update, context):
        """Devuelve las 5 noticias más relevantes para el tema que se elija"""
        self.logger.info('He recibido el comando top_tema')

        if not context.args:
            context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Las secciones disponibles son 'entretenimiento', 'ciencia', 'deportes', 'tecnología, 'salud'")
            return None
        elif context.args[0].lower() == 'entretenimiento':
            tema = 'entertainment'
        elif context.args[0].lower() == 'ciencia':
            tema = 'science'
        elif context.args[0].lower() == 'deportes':
            tema = 'sports'
        elif context.args[0].lower() == 'salud':
            tema = 'health'
        elif context.args[0].lower() in ['tecnología', 'tecnologia']:
            tema = 'technology'

        try:
            top5_noticias_tema = newsapi.get_top_headlines(
                                            language='es',
                                            country='ar',
                                            page_size=5,
                                            category=tema)
            for articulo in top5_noticias_tema['articles']:
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Título: {} \nAutor: {} \n {}".format(articulo['title'], articulo['author'], articulo['description']))
                context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = tinyurl(articulo['url']))
        except:
            context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Lo siento, no reconozco esa sección.")
        
    def noticia_por_mensaje(self, update, context):
        """ Devuelve al usuario una noticia relacionadas con el texto que escriba, si las encuentra. """
        self.logger.info('He recibido un mensaje')

        # Recolecta una noticia mediante la api
        mensaje = update.message.text.lower()
        noticias_mensaje = newsapi.get_everything(
                                        q=mensaje,
                                        language='es',
                                        page_size=5,
                                        )

        if noticias_mensaje['articles']:
            for articulo in noticias_mensaje['articles']:
                    context.bot.send_message(
                        chat_id = update.message.chat_id,
                        text = tinyurl(articulo['url']))
                    context.bot.send_message(
                        chat_id = update.message.chat_id,
                        text = "Título: {} \nAutor: {}".format(articulo['title'], articulo['author']))
        else:
            context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = "Lo siento, no pude encontrar noticias relacionadas a '{}'.".format(mensaje))