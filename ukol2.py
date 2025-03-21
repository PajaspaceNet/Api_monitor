import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request, send_file
import io

app = Flask(__name__)

github_api_url = "https://api.github.com/events"
events_store = []  # Ukládáme události jako seznam slovníků


# Funkce pro stažení dat z GitHub API
def fetch_github_events():
    global events_store
    response = requests.get(github_api_url)
    if response.status_code == 200:
        data = response.json()
        # Filtrování pouze požadovaných událostí
        filtered_events = [event for event in data if
                           event['type'] in ['WatchEvent', 'PullRequestEvent', 'IssuesEvent']]
        for event in filtered_events:
            event['timestamp'] = time.time()  # Přidáme čas stažení
        events_store.extend(filtered_events)
    else:
        print("Chyba při získávání dat z GitHub API")


# Endpoint: Průměrný čas mezi pull requesty
@app.route("/metrics/avg_pull_time", methods=["GET"])
def avg_pull_time():
    pull_requests = [event for event in events_store if event['type'] == 'PullRequestEvent']
    if len(pull_requests) < 2:
        return jsonify({"message": "Nedostatek dat pro výpočet"})

    timestamps = sorted([event['timestamp'] for event in pull_requests])
    diffs = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
    avg_time = sum(diffs) / len(diffs)
    return jsonify({"average_pull_request_time": avg_time})


# Endpoint: Počet událostí v posledních X minutách
@app.route("/metrics/event_count", methods=["GET"])
def event_count():
    offset = int(request.args.get("offset", 10))  # Výchozí hodnota 10 minut
    current_time = time.time()
    event_types = {}

    for event in events_store:
        if (current_time - event['timestamp']) <= (offset * 60):  # Převod minut na sekundy
            event_types[event['type']] = event_types.get(event['type'], 0) + 1

    return jsonify(event_types)


# Endpoint: Graf událostí
@app.route("/metrics/event_chart", methods=["GET"])
def event_chart():
    offset = int(request.args.get("offset", 10))  # Výchozí hodnota 10 minut
    current_time = time.time()
    event_types = {}

    for event in events_store:
        if (current_time - event['timestamp']) <= (offset * 60):
            event_types[event['type']] = event_types.get(event['type'], 0) + 1

    if not event_types:
        return jsonify({"message": "Žádná data k zobrazení"})

    # Vytvoření grafu
    plt.figure(figsize=(6, 4))
    plt.bar(event_types.keys(), event_types.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Typ události")
    plt.ylabel("Počet")
    plt.title(f"GitHub události za posledních {offset} minut")

    # Uložení grafu do paměti
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


# Spouštění periodického získávání dat
def run_fetch_loop(interval=60):
    while True:
        fetch_github_events()
        time.sleep(interval)  # Stáhneme data každou minutu


if __name__ == "__main__":
    from threading import Thread

    fetch_thread = Thread(target=run_fetch_loop, daemon=True)
    fetch_thread.start()
    app.run(debug=True)
