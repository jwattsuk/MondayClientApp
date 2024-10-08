from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

def read_api_token(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Set up your API token and endpoint
API_TOKEN = read_api_token('api_token.txt')
API_URL = 'https://api.monday.com/v2'

headers = {
    'Authorization': API_TOKEN,
    'Content-Type': 'application/json'
}

# Define a query to get data from Monday.com board 1642180441
query = '{boards(ids: 1642180441) { name id description items_page { items { name column_values (ids: ["single_select__1", "location__1", "color30__1", "dup__of_mentor__1", "date0__1", "text__1"]) { column { title } text } } } } }'

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

    return render_template('participants_grid.html', participants=participants)

if __name__ == '__main__':
    app.run(debug=True)