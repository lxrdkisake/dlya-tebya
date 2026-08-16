"""Сборка: src/page.html + встроенные шрифты -> index.html (один самодостаточный файл).

Запуск:  python build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src", "page.html")
FONTS = os.path.join(ROOT, "assets", "fonts", "fonts.css")
OUT = os.path.join(ROOT, "index.html")

html = open(SRC, encoding="utf-8").read()
fonts = open(FONTS, encoding="utf-8").read()

if "/*__FONTS__*/" not in html:
    raise SystemExit("В src/page.html нет маркера /*__FONTS__*/")

html = html.replace("/*__FONTS__*/", fonts)

# Никаких внешних запросов быть не должно (страница обязана работать офлайн)
external = re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', html)
if external:
    raise SystemExit("Найдены внешние ссылки: " + ", ".join(external))

open(OUT, "w", encoding="utf-8").write(html)
print(f"OK -> {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB)")
