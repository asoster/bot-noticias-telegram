#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Import KEYS API
from config.keys import TOKEN_TELEGRAM
from bot_noticias import BotNoticias

if __name__ == '__main__':
    noticias_bot = BotNoticias("noticias_argentina_bot", TOKEN_TELEGRAM)
    noticias_bot.esperar_comando("start", noticias_bot.start)
    noticias_bot.esperar_comando("ayuda", noticias_bot.ayuda)
    noticias_bot.esperar_comando("top5", noticias_bot.top_noticias)
    noticias_bot.esperar_comando("seccion", noticias_bot.seccion)
    noticias_bot.esperar_comando("tt", noticias_bot.trend_topics)
    noticias_bot.contestar_mensaje(noticias_bot.noticia_por_mensaje)
    noticias_bot.contestar_consulta(noticias_bot.noticia_por_tema)