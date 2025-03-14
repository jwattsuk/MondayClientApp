import requests
import json
from prettytable import PrettyTable

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
query = '{boards(ids: 1642180441) { name id description items_page { items { name column_values (ids: ["single_select__1", "location__1", "color30__1", "dup__of_mentor__1", "date0__1", "text__1", "link_to_volunteers__1"]) { id column { title } text } } } } }'

query2 = """
{
    boards(ids: 1642180441) { 
        name id description items_page { 
            items { 
                name column_values (ids: ["single_select__1", "location__1", "color30__1", "dup__of_mentor__1", "date0__1", "text__1", "link_to_volunteers__1"]) { 
                    id column { 
                        title 
                    } 
                    text 
                }
            } 
        } 
    } 
}
"""

columns_query = '{boards(ids: 1521055645) { name id description items_page { items { name column_values { id value } } } } }'

boards_query = """ {
  boards {
    id
    name
    state
  }
}"""

participant_board_all_cols = """
{
    boards(ids: 1705846327) { 
        name id description items_page { 
            items { 
                name column_values { 
                    id column { 
                        title 
                    } 
                    text
                }
            } 
        } 
    } 
}
"""

query3 = "{ boards(ids: 1705846327) { name id description items_page { items { name column_values { id column { title } text } } } } }"

# single_select__1 == Area
# status__1 == Participant Stage
# date01__1 == Bag Delivery (date)
participant_board_all_cols_filter = """
query {
  items_page_by_column_values(
    limit: 500,
    board_id: 1521055645,
    columns: [
      {
        column_id: "single_select__1",
        column_values: ["Hackney"]
      },
      {
        column_id: "status__1",
        column_values: ["Registration", "Start data and assessment", "Mentor group and bag delivery", "Course in progress"]
      },
      {
        column_id: "date0__1",
        column_values: [""]
      }      
    ]
  ) {
    items { 
                name column_values { 
                    id column { 
                        title 
                    } 
                    text 
                }
            }
  }
}
"""

delivery_report = """
{boards(ids: 1705846327) 
    { name id description items_page  ( query_params: 
        {rules: [{column_id: \"status__1\", compare_value: [8]} 
            {column_id: \"status_17__1\", compare_value: 13}], operator: and}) 
                { cursor  items 
                    { name column_values 
                        { column { title } text  }  
                        linked_items_deliverer: column_values(ids: \"board_relation__1\") {   value   }    
                        linked_items_course: column_values(ids: \"link_to_courses__1\") {   value   }     
                        linked_items_mentor: column_values(ids: \"link_to_volunteers__1\") {   value    }         } } } }
"""

delivery_report2 = """
{boards(ids: 1705846327) 
    { name id description items_page  
                { cursor  items 
                    { name column_values 
                        { column { title } text  }  
                        linked_items_deliverer: column_values(ids: \"board_relation__1\") {   value   }    
                        linked_items_course: column_values(ids: \"link_to_courses__1\") {   value   }     
                        linked_items_mentor: column_values(ids: \"link_to_volunteers__1\") {   value    }         } } } }
"""

query_with_values = """
{
  boards(ids: 1705846327) {
    name
    id
    description
    items_page  {
      items {
        name
        column_values {
          column {
            title
          }
          id
          value
          text
        }
      }
    }
  }
}
"""

def get_board_data():
    """Fetch data from Monday.com board using GraphQL query."""
    data = {
        #'query': query2
        'query': delivery_report2
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run: {response.status_code}, {response.text}")

def print_table(data):
    # Create a table with headings
    table = PrettyTable(["Name", "Area", "Postcode/Address", "Diabetes", "Delivery Instructions", "Bag Delivery Date", "Deliverer"])

    # Extract items from JSON
    items = data['data']['boards'][0]['items_page']['items']

    # Loop through each item to retrieve 'name', 'Area', and 'Postcode/Address'
    for item in items:
        name = item['name']
        area = None
        postcode_address = None
        diabetes = None
        delivery_instructions = None
        delivery_date = None
        deliverer = None
        
        # Get column values for Area and Postcode/Address
        for column_value in item['column_values']:
            if column_value['column']['title'] == 'Area':
                area = column_value['text']
            if column_value['column']['title'] == 'Postcode/Address':
                postcode_address = column_value['text']
            if column_value['column']['title'] == 'Do you have diabetes (any type)?':
                diabetes = column_value['text']
            if column_value['column']['title'] == 'Delivery instructions':
                delivery_instructions = column_value['text']                
            if column_value['column']['title'] == 'Bag delivery date':
                delivery_date = column_value['text']
            if column_value['column']['title'] == 'Deliverer':
                deliverer = column_value['text']

        # Add a row to the table
        table.add_row([name, area, postcode_address, diabetes, delivery_instructions, delivery_date, deliverer])

    # Print the table
    print(table)

if __name__ == "__main__":
    try:
        board_data = get_board_data()
        #print(json.dumps(board_data, indent=4))
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(board_data, f, ensure_ascii=False, indent=4)
        #data_dict = json.loads(board_data)
        #print_table(board_data)
    except Exception as e:
        print(f"Error: {e}")
