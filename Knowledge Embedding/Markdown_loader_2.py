from icecream import ic
import json
import re
import yaml
import re

def parse_markdown_v2(filename, path=''):
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

def parse_markdown(filename, path=''):
    with open(filename, 'r') as file:
        content = file.read()
    
    # check if the file has metadata using regex pattern '---'
    if re.search(r'^---$', content, re.MULTILINE):
        metadata, markdown_content = content.split('---\n', 2)[1:]
        metadata = yaml.safe_load(metadata)
    else:
        metadata = { 'tags': [], 'related': [], 'author': '', 'date': ''}
        markdown_content = content
       
    source_info = {
        'source': {
            'type': 'file',
            'name': filename,
            'path': path,
            'tags': metadata.get('tags', []),
            'related': metadata.get('related', []),
            'author': metadata.get('author', ''),
            'date': metadata.get('date', '')
        }
    }
    
    json_structure = {'chapters': []}
    lines = markdown_content.split('\n')
    current_chapter = None
    current_index = []

    header_patterns = [
        (r'^# ', 1),
        (r'^## ', 2),
        (r'^### ', 3),
        (r'^#### ', 4),
        (r'^##### ', 5)
    ]

    def get_index(level):
        prefix = '.'
        return prefix.join(str(i) for i in current_index[:level]) + f'.{len(current_index) + 1}'
        

    for line in lines:
        for pattern, level in header_patterns:
            if re.match(pattern, line):
                current_chapter = {
                    'chapter': {
                        'name': line[len(pattern)-1:].strip(),
                        'index': get_index(level).removeprefix('.'),
                        'content': ''
                    },
                    **source_info
                }
                current_index = current_index[:level-1] + [len(current_index) + 1]
                json_structure['chapters'].append(current_chapter)
                break
        else:
            if line.strip():
                if current_chapter and 'content' in current_chapter['chapter']:
                    current_chapter['chapter']['content'] += line + '\n'
            else:
                if current_chapter:
                    current_chapter['chapter']['content'] = current_chapter['chapter']['content'].strip()
    return json_structure
    # return json.dumps(json_structure, indent=4)


# Save this script as markdown_to_json.py and run the following code:

if __name__ == "__main__":
    json_output = json.dumps(parse_markdown('demo.md'), indent=4)
    # print(json_output)
    print("-----------------")
    ic(json_output)
