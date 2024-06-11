import json
import re

def parse_markdown(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    json_structure = {'document': {'filename': filename}, 'chapters': []}
    current_chapter = None
    current_index = []
    index_map = {1: '1'}

    for line in lines:
        if line.startswith('# '):
            current_chapter = {'chapter': {'name': line[2:].strip(), 'index': '1', 'content': ''}}
            current_index = [1]
            json_structure['chapters'].append(current_chapter)
        elif line.startswith('## '):
            current_chapter = {'chapter': {'name': line[3:].strip(), 'index': '1.{}'.format(len(current_index) + 1), 'content': ''}}
            current_index = [1, len(current_index) + 1]
            json_structure['chapters'].append(current_chapter)
        elif line.startswith('### '):
            current_chapter = {'chapter': {'name': line[4:].strip(), 'index': '1.{}.{}'.format(current_index[1], len(current_index) + 1), 'content': ''}}
            current_index = [1, current_index[1], len(current_index) + 1]
            json_structure['chapters'].append(current_chapter)
        elif line.strip():
            if current_chapter and 'content' in current_chapter['chapter']:
                current_chapter['chapter']['content'] += line
        else:
            if current_chapter:
                current_chapter['chapter']['content'] = current_chapter['chapter']['content'].strip()

    return json.dumps(json_structure, indent=4)

# Save this script as markdown_to_json.py and run the following code:
if __name__ == "__main__":
    json_output = parse_markdown('demo.md')
    print(json_output)
