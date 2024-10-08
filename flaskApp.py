from flask import Flask, render_template_string, jsonify
import json
import requests

app = Flask(__name__)

# Sample JSON data
data = json.loads(b'{"data":{"boards":[{"name":"Participants (task 1)","id":"1642180441","description":null,"items_page":{"items":[{"name":"Paola","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"Hackney, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"John McCrea","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"The Green, London W5 5DA, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Jerry","column_values":[{"column":{"title":"Area"},"text":null},{"column":{"title":"Postcode/Address"},"text":"The Green, London W5 5DA, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"Yes"},{"column":{"title":"Delivery instructions"},"text":"leave in porch"},{"column":{"title":"Bag delivery date"},"text":"2024-06-21"},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Marius Nedelciu","column_values":[{"column":{"title":"Area"},"text":"Sheffield"},{"column":{"title":"Postcode/Address"},"text":"11-12 Rear of Green flat h, Bowerston, OH, USA"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Sarah","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"13 Derwent Road, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Mason","column_values":[{"column":{"title":"Area"},"text":"Merton"},{"column":{"title":"Postcode/Address"},"text":"3 Derwent Road, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"Yes"},{"column":{"title":"Delivery instructions"},"text":"deliver to neighbour at no. 5"},{"column":{"title":"Bag delivery date"},"text":"2024-09-04"},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Alexandra Marinescu","column_values":[{"column":{"title":"Area"},"text":"Sheffield"},{"column":{"title":"Postcode/Address"},"text":"The Green, London W5 5DA, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Jason Penny","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"Hackney, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"No"},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Chris Barlow","column_values":[{"column":{"title":"Area"},"text":"Islington"},{"column":{"title":"Postcode/Address"},"text":"Hackney, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"No"},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Paula Jones","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"Hackney, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"No"},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Jerry Dash","column_values":[{"column":{"title":"Area"},"text":"Newham"},{"column":{"title":"Postcode/Address"},"text":"Hackney, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"No"},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Mason Alexander Park","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"The Green, London W5 5DA, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":"No"},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Paula","column_values":[{"column":{"title":"Area"},"text":"Reigate"},{"column":{"title":"Postcode/Address"},"text":"London E1 6AW, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":"2024-08-20"},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Sarah Bell","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"Hackney, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Cristiana","column_values":[{"column":{"title":"Area"},"text":"Islington"},{"column":{"title":"Postcode/Address"},"text":"Islington, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]},{"name":"Simon","column_values":[{"column":{"title":"Area"},"text":"Hackney"},{"column":{"title":"Postcode/Address"},"text":"Islington, London, UK"},{"column":{"title":"Do you have diabetes (any type)?"},"text":null},{"column":{"title":"Delivery instructions"},"text":""},{"column":{"title":"Bag delivery date"},"text":""},{"column":{"title":"Deliverer"},"text":null}]}]}}]},"account_id":19996352}')

# HTML template to render the grid
template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>

<h2>Participants Grid</h2>

<table>
    <tr>
        <th>Name</th>
        <th>Area</th>
        <th>Postcode/Address</th>
        <th>Do you have diabetes (any type)?</th>
        <th>Delivery instructions</th>
        <th>Bag delivery date</th>
        <th>Deliverer</th>
    </tr>
    {% for participant in participants %}
    <tr>
        <td>{{ participant.name }}</td>
        <td>{{ participant.area }}</td>
        <td>{{ participant.address }}</td>
        <td>{{ participant.diabetes }}</td>
        <td>{{ participant.instructions }}</td>
        <td>{{ participant.delivery_date }}</td>
        <td>{{ participant.deliverer }}</td>
    </tr>
    {% endfor %}
</table>

</body>
</html>
"""

def read_api_token(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Set up your API token and endpoint
API_TOKEN = read_api_token('api_token.txt')
print(f"API Token: {API_TOKEN}")
API_URL = 'https://api.monday.com/v2'

headers = {
    'Authorization': API_TOKEN,
    'Content-Type': 'application/json'
}

# Define a query to get data from Monday.com board 1642180441
query = '{boards(ids: 1642180441) { name id description items_page { items { name column_values (ids: ["single_select__1", "location__1", "color30__1", "dup__of_mentor__1", "date0__1", "text__1"]) { column { title } text } } } } }'

#columns_query = '{boards(ids: 1642180441) { name id description items_page { items { name column_values { id value } } } } }'

def get_board_data():
    """Fetch data from Monday.com board using GraphQL query."""
    data = {
        'query': query
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run: {response.status_code}, {response.text}")

@app.route('/')
def home():
    # Prepare the data for rendering
    participants = []
    board_data = get_board_data()
    board_items = board_data['data']['boards'][0]['items_page']['items']
    
    for item in board_items:
        participant = {
            'name': item['name'],
            'area': next((cv['text'] for cv in item['column_values'] if cv['column']['title'] == 'Area'), ''),
            'address': next((cv['text'] for cv in item['column_values'] if cv['column']['title'] == 'Postcode/Address'), ''),
            'diabetes': next((cv['text'] for cv in item['column_values'] if cv['column']['title'] == 'Do you have diabetes (any type)?'), ''),
            'instructions': next((cv['text'] for cv in item['column_values'] if cv['column']['title'] == 'Delivery instructions'), ''),
            'delivery_date': next((cv['text'] for cv in item['column_values'] if cv['column']['title'] == 'Bag delivery date'), ''),
            'deliverer': next((cv['text'] for cv in item['column_values'] if cv['column']['title'] == 'Deliverer'), '')
        }
        participants.append(participant)

    return render_template_string(template, participants=participants)

if __name__ == '__main__':
    app.run(debug=True)
