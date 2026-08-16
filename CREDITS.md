# Откуда что взято

Личная страница-открытка. Часть ассетов — чужие, поэтому вот честный список.

## Код

| Что | Откуда | Лицензия |
|---|---|---|
| Кот, который бегает за кнопкой «Нет» (спрайт `oneko.gif` + логика движения) | [adryd325/oneko.js](https://github.com/adryd325/oneko.js) | MIT © adryd. Спрайт — классический Neko из X11 |

Логика погони переписана: оригинал бегает за курсором, здесь — за убегающей кнопкой.

## Картинки

| Файл | Откуда | Примечание |
|---|---|---|
| `assets/cats/oneko.gif` | [adryd325/oneko.js](https://github.com/adryd325/oneko.js) | MIT |
| `assets/cats/cat-beg.gif`, `cat-cry.gif` | [CodeKageHQ/Ask-out-your-Valentine](https://github.com/CodeKageHQ/Ask-out-your-Valentine) | стикеры Mochi Peach Cat, автор рисунков неизвестен |
| `assets/cats/cat-happy.gif`, `cat-love.gif` | [Tenor](https://tenor.com/search/mochimochi-gifs) | стикеры Mochi Peach Cat |
| `assets/cats/cat-dance.gif`, `cat-pixel-heart.gif` | [tashkirrr/Will-You-Be-My-Love-](https://github.com/tashkirrr/Will-You-Be-My-Love-) | пиксель-арт, автор неизвестен |

**Важно:** у стикеров Mochi Peach Cat и пиксель-котов нет явной лицензии — это фанатские
работы, разошедшиеся по сети. Для личной странички-подарка это нормально, для коммерческого
проекта их использовать нельзя.

## Шрифты

Все три — [Google Fonts](https://fonts.google.com), лицензия SIL Open Font License 1.1,
вшиты в `index.html` в base64 (подмножества «кириллица + латиница»).

| Шрифт | Роль |
|---|---|
| **Unbounded** | крупные заголовки |
| **Press Start 2P** | пиксельные подписи, чипы, номера пунктов, бегущая строка |
| **Onest** | основной текст |

Сначала в роли пиксельного шрифта стоял **Pixelify Sans** — пришлось заменить: в нём
физически отсутствуют глифы **О** (U+041E) и **П** (U+041F), и русский текст рассыпался
на два шрифта прямо посреди слова. У Press Start 2P кириллица полная, включая строчные.

## Что изучено, но не использовано

Исходники похожих проектов скачаны и разобраны — оттуда взяты идеи и часть картинок,
но код написан свой:

- [aditisins/be-my-valentine](https://github.com/aditisins/be-my-valentine)
- [byquangthanh/valentine.github.io](https://github.com/byquangthanh/valentine.github.io)
- [dikshikaaa/Valentines-Day](https://github.com/dikshikaaa/Valentines-Day)
- [tashkirrr/Will-You-Be-My-Love-](https://github.com/tashkirrr/Will-You-Be-My-Love-)
- [CodeKageHQ/Ask-out-your-Valentine](https://github.com/CodeKageHQ/Ask-out-your-Valentine)

Во всех пяти «Нет» убегает по одной и той же наивной схеме: случайная точка на экране без
проверки границ, поэтому кнопка регулярно улетает за экран, наезжает на «Да» или на телефоне
успевает поймать тап. Здесь это сделано аккуратнее — см. `README.md`.
