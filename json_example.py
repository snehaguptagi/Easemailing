import json

# Sample data
sample_data = {
    "name": "Sneha",
    "project": "LAM Model"
}

# Convert Python object to JSON string
json_string = json.dumps(sample_data)
print("JSON String:", json_string)

# Write the JSON string to a file
with open('data.json', 'w') as json_file:
    json_file.write(json_string)

# Now read the JSON file back
with open('data.json', 'r') as json_file:
    loaded_data = json.load(json_file)

# Print the loaded data
print("Loaded Data:", loaded_data)
