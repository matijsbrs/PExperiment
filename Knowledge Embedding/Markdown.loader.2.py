import json
import re
import yaml

def parse_markdown(filename, path=''):
    with open(filename, 'r') as file:
        content = file.read()
    
    metadata, markdown_content = content.split('---\n', 2)[1:]
    metadata = yaml.safe_load(metadata)
    
    source_info = {
        'source': {
            'type': 'file',
            'path': path,
            'name': filename,
            'tags': metadata.get('tags', []),
            'related': metadata.get('related', []),
            'author': metadata.get('author', ''),
            'date': metadata.get('date', '')
        }
    }
    
    json_structure = {
        'chapters': []
    }
    
    lines = markdown_content.split('\n')
    current_chapter = None
    current_index = []
    
    for line in lines:
        if line.startswith('# '):
            current_chapter = {
                'chapter': {
                    'name': line[2:].strip(),
                    'index': '1',
                    'content': ''
                },
                **source_info
            }
            current_index = [1]
            json_structure['chapters'].append(current_chapter)
        elif line.startswith('## '):
            current_chapter = {
                'chapter': {
                    'name': line[3:].strip(),
                    'index': f'1.{len(current_index) + 1}',
                    'content': ''
                },
                **source_info
            }
            current_index = [1, len(current_index) + 1]
            json_structure['chapters'].append(current_chapter)
        elif line.startswith('### '):
            current_chapter = {
                'chapter': {
                    'name': line[4:].strip(),
                    'index': f'1.{current_index[1]}.{len(current_index) + 1}',
                    'content': ''
                },
                **source_info
            }
            current_index = [1, current_index[1], len(current_index) + 1]
            json_structure['chapters'].append(current_chapter)
        elif line.startswith('#### '):
            current_chapter = {
                'chapter': {
                    'name': line[5:].strip(),
                    'index': f'1.{current_index[1]}.{current_index[2]}.{len(current_index)}',
                    'content': ''
                },
                **source_info
            }
            current_index = [1, current_index[1], current_index[2], len(current_index)]
            json_structure['chapters'].append(current_chapter)
        elif line.startswith('##### '):
            current_chapter = {
                'chapter': {
                    'name': line[6:].strip(),
                    'index': f'1.{current_index[1]}.{current_index[2]}.{current_index[3]}.{len(current_index)}',
                    'content': ''
                },
                **source_info
            }
            current_index = [1, current_index[1], current_index[2], current_index[3], len(current_index)]
            json_structure['chapters'].append(current_chapter)
            current_index = [1, current_index[1], len(current_index) + 1]
            json_structure['chapters'].append(current_chapter)
        elif line.strip():
            if current_chapter and 'content' in current_chapter['chapter']:
                current_chapter['chapter']['content'] += line + '\n'
        else:
            if current_chapter:
                current_chapter['chapter']['content'] = current_chapter['chapter']['content'].strip()
    
    return json.dumps(json_structure, indent=4)

# # Save this script as markdown_to_json.py and run the following code:
# if __name__ == "__main__":
#     json_output = parse_markdown('demo.md')
#     print(json_output)
