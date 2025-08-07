from flask import Flask, render_template, request, send_file,jsonify
from api_handler import get_flight_data, get_chatgpt_summary
from collections import Counter
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Get filters from query string
    selected_city = request.args.get('city')
    selected_airline = request.args.get('airline')
    selected_date = request.args.get('date') 

    # Fetch flight data
    flights = get_flight_data(limit=50)

    # Create filter options
    cities = sorted(set(f['departure']['airport'] for f in flights if f['departure']['airport']))
    airlines = sorted(set(f['airline']['name'] for f in flights if f['airline']['name']))

    # Apply filters if selected
    if selected_city:
        flights = [f for f in flights if f['departure']['airport'] == selected_city]
    if selected_airline:
        flights = [f for f in flights if f['airline']['name'] == selected_airline]
    if selected_date:
        flights = [
            f for f in flights
            if f['departure']['scheduled'] and f['departure']['scheduled'][:10] == selected_date
        ]
    # Count top routes
    route_list = [f"{f['departure']['airport']} → {f['arrival']['airport']}"
                  for f in flights if f['departure']['airport'] and f['arrival']['airport']]
    route_counter = Counter(route_list)
    top_routes = route_counter.most_common(5)

    labels = [r[0] for r in top_routes]
    values = [r[1] for r in top_routes]
    airline_list = [f['airline']['name'] for f in flights if f['airline']['name']]
    airline_counter = Counter(airline_list)
    airline_labels = list(airline_counter.keys())
    airline_values = list(airline_counter.values())
    summary = get_chatgpt_summary(flights)

    return render_template('index.html',
                           flights=flights,
                           top_routes=top_routes,
                           labels=labels,
                           values=values,
                           cities=cities,
                           airlines=airlines,
                           selected_city=selected_city,
                           selected_airline=selected_airline,
                           selected_date=selected_date,
                           summary=summary,
                           airline_labels=airline_labels,
                       airline_values=airline_values)
@app.route('/download', methods=['GET'])
def download_csv():
    selected_city = request.args.get('city')
    selected_airline = request.args.get('airline')
    selected_date = request.args.get('date')

    flights = get_flight_data(limit=50)

    # Apply same filters
    if selected_city:
        flights = [f for f in flights if f['departure']['airport'] == selected_city]
    if selected_airline:
        flights = [f for f in flights if f['airline']['name'] == selected_airline]
    if selected_date:
        flights = [
            f for f in flights
            if f['departure']['scheduled'] and f['departure']['scheduled'][:10] == selected_date
        ]

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Airline', 'From', 'To', 'Status', 'Date'])

    for f in flights:
        writer.writerow([
            f.get('airline', {}).get('name', ''),
            f.get('departure', {}).get('airport', ''),
            f.get('arrival', {}).get('airport', ''),
            f.get('flight_status', ''),
            f.get('departure', {}).get('scheduled', '')
        ])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='filtered_flights.csv'
    )
@app.route('/ask', methods=['POST'])
def ask():
    from api_handler import ask_flight_bot

    flights = get_flight_data(limit=50)

    question = request.json.get('question')
    if not question:
        return jsonify({"answer": "Please enter a question."})

    answer = ask_flight_bot(question, flights)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
