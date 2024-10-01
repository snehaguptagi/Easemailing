import json

sample_data = {
    "name": "Sneha",
    "project": "LAM Model"
}

# Convert Python object to JSON string
json_string = json.dumps(sample_data)
print(json_string)
