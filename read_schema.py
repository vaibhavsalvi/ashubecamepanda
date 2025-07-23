import json

def read_schema_from_file(schema_file):
    """
    Reads a database schema from a JSON file.
    The JSON should be a dict with table/function/procedure names as keys and column/parameter details as values.
    """
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    return schema

if __name__ == "__main__":
    schema_file = input("Enter the path to your schema JSON file: ")
    schema = read_schema_from_file(schema_file)
    print("\nLoaded schema details:")
    for name, details in schema.items():
        print(f"- {name}: {details}")
