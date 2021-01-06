<!-- ![stronghold logo](img/stronghold-logo-left.png) -->

<!-- [![Downloads](http://pepy.tech/badge/stronghold)](http://pepy.tech/count/stronghold) -->

`foerderportal-scraper` Automatisiert Verbundprojekt Daten des Förderkatalogs der Bundesregierung herunterladen.

![GIF demo](./demo.gif)

csvedit.py zur Erstellung von Target / Node Tabellen für bspw. Gephi

**Usage**
---

```
usage: crawler.py [-h] -s [STADT [STADT ...]]
                  [-b [BUNDESLAND [BUNDESLAND ...]]] [-l LAUFZEIT] [-lfd]
                  [-t THREADS]
arguments:
  -h, --help            show this help message and exit
  -s [STADT [STADT ...]], --stadt [STADT [STADT ...]]
                        Stadt/Gemeinde
  -b [BUNDESLAND [BUNDESLAND ...]], --bundesland [BUNDESLAND [BUNDESLAND ...]]
                        Bundesland
  -l LAUFZEIT, --laufzeit LAUFZEIT
                        Laufzeit von
  -lfd, --lfdvorhaben   Nur lfd. Vorhaben
  -t THREADS, --threads THREADS
                        Parallele Threads

```

**Installation**
---
Benötigt Geckodriver und Firefox
1. Download [`Geckodriver`](https://github.com/mozilla/geckodriver/releases)
    + `In den selben Ordner wie die crawler.py verschieben`

2. Crawler Starten

3. Nach dem Crawlen : csvedit.py Starten (erstellt kartesisches Produkt aller im ordner Output liegenden Datensätze)
