# API_MONITOR

Obsah
[O čem to je](#ocemtoje)  <br>
 
Co dela <br>
Kratky navod na spusteni <br>
Instalace <br>
Kde bezi <br>
RestApi<br>
Architektura<br>
Mozna vylepseni <br>
Poznamky<br>



# GitHub Event Monitor

## O čem to je :*


Tato aplikace monitoruje veřejné události z GitHubu 
(pomocí [https://api.github.com/events](https://api.github.com/events)), 
 metriky prostřednictvím REST API.

 
*Co aplikace dělá*

- Pravidelně získává data z GitHubu (každou minutu)
- Sleduje tyto události:
  - `WatchEvent` (kdyz nekdo sleduje repozitář)
  - `PullRequestEvent` (kdyz nekdo otevře nebo pracuje na PR)
  - `IssuesEvent` (práce s issues)
- Ukládá je do paměti a poskytuje metriky pomocí vlastního API


*Kratky navod na instalaci a spusteni* 

1. Instalace závislostí a spusteni :
```
pip install flask requests pandas matplotlib
python ukol2.py
```

* 2. Aplikace bezi na:
```
http://127.0.0.1:5000/
```

# REST API Endpointy

obecne:
GET /metrics/event_count?offset=X
Vrací počet událostí podle typu z posledních X minut

 - Výchozí offset je 10, pokud není zadán


Příklad odpovědi:

http://127.0.0.1:5000/metrics/event_count?offset=10

```
{
    "IssuesEvent": 1,
    "PullRequestEvent": 10,
    "WatchEvent": 5
}

```
* GET /metrics/avg_pull_time

Vrací průměrný čas (v sekundách) mezi PullRequestEvent událostmi.

Příklad odpovědi:

http://127.0.0.1:5000/metrics/avg_pull_time
```

{
    "average_pull_request_time": 15.039884150028229
}

```

* GET /metrics/event_chart?offset=X 

Vrací graf (obrázek) s počtem událostí podle typu z posledních X minut

![ukol1](https://github.com/user-attachments/assets/5355e4ec-1e77-4647-973f-5b124d183980)





# Architektura C4

[ Uživatelský prohlížeč / Postman ] - > [ Flask API ] -> [ GitHub Event Fetcher ] ->[ In-memory úložiště ]


Mozna vylepseni:
           
Pozn,
In memory /ev. by se dal aplikovat databaze apod, v nasem pripade memory pocitace/


# Testovano v Postmann i v prohlizeci

Status OK ... vystup v json , screenshot grafu prilozen.


  
