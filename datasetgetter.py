import requests
import time
#####################
global data_set
data_set = []
#####################

# Monday.com API Key
apiKey = "secret api key here"
IDS = "1234567890" # Board ID


apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}
print("#####################################################################################################")
print("\nLoading data ...\n")
start_time = time.time()

query = '{boards(ids: %s){items_page {cursor items {column_values {column {title} text}}}}}'%(IDS)
query_data = {'query' : query}
request_data = requests.post(url=apiUrl, json=query_data, headers=headers)
json_data = request_data.json()
data_in_json = json_data["data"]["boards"][0]['items_page']
cursor = data_in_json['cursor']
data_items = data_in_json['items']
for user_json in data_items:
    new_data_row = {}
    data = user_json['column_values']
    for row in data:
        cell_title = row['column']['title']
        cell_value = row['text'] 
        if cell_value == '' or cell_value =='0' or cell_value == 'None' or cell_value == "null" or cell_value == None or "None" in cell_value:
            cell_value = "NULL"
        new_data_row[cell_title] = cell_value
    data_set.append(new_data_row)

while cursor:
    next_query = '{next_items_page(cursor: "%s") {cursor items {column_values {column {title}text}}}}'%(cursor)
    next_query_data = {'query' : next_query}
    next_request_data = requests.post(url=apiUrl, json=next_query_data, headers=headers)
    next_json_data = next_request_data.json()
    next_data_in_json = next_json_data["data"]["next_items_page"]
    cursor = ""
    cursor = next_data_in_json['cursor']
    next_data_items = next_data_in_json['items']
    for next_user_json in next_data_items:
        new_next_data_row = {}
        next_data = next_user_json['column_values']
        for row in next_data:
            cell_title = row['column']['title']
            cell_value = row['text'] 
            if cell_value == '' or cell_value =='0' or cell_value == 'None' or cell_value == "null" or cell_value == None or "None" in cell_value:
                cell_value = "NULL"
            new_next_data_row[cell_title] = cell_value
        data_set.append(new_next_data_row)
print("#####################################################################################################")
end_time = time.time()
duration = end_time - start_time
print("\nData loaded in : {:.2f} sec\n".format(duration))
print("#####################################################################################################")