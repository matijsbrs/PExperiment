Goodmorning GPT, 
I need python script that can open a markdown file and convert it into a JSON string.

I included a markdown example between the XML tags: <Example:Markdown> the file is named: 'tutorial.md'
The markdown document should be converted into a json string as in the XML tags: <Result:JSON>

<Example:Markdown>
---
tags:
- computers
- hardware
- guide
related:
- hardware.md
- linux.md
author: copilot
date: 11-6-2024
---
# Title of document
Here is the text of the first chapter

## Summary
This contains the summary of the document

## Preparations
Prepare information here

### Powering down the computer
Before doing work on the computer make sure it's powered down.

    1. Open a shell
    2. type: 'sudo poweroff'
    3. wait for the computer to shutdown

### Hardware
Add the hardware to the pc

## Testing
Before shipping the computer please test it

### Starting
Follow the folling steps:

    1. Power on
    2. Check for smoke

## Package
return to sender
</Example:Markdown>

<Result:JSON>
{'chapters': [
    {'chapter' : 
        {'name': 'Title of document'},
        {'source':
            {'type': 'file'},
            {'name': 'tutorial.md'},
            {'tags': 
                ['computers','hardware','guide']
            },
            {'related':
                ['hardware.md','linux.md']
            },
            {'author' : 'copilot'},
            {'date': '11-6-2024'}
        }
        {'index': '1'},
        {'content': """Here is the text of the first chapter"""}
    },
    {'chapter' : 
        {'name': 'summary'},
        {'index': '1.1'},
        {'content': """This contains the summary of the document"""}
    }, 
    {'chapter' : 
        {'name': 'Preparations'},
        {'index': '1.2'},
        {'content': """Prepare information here"""}
    }, 
    {'chapter' : 
        {'name': 'Powering down the computer'},
        {'index': '1.2.1'},
        {'content': """
        Before doing work on the computer make sure it's powered down.

            1. Open a shell
            2. type: 'sudo poweroff'
            3. wait for the computer to shutdown"""}
    }, 
    {'chapter' : 
        {'name': 'Hardware'},
        {'index': '1.2.2'},
        {'content': """Add the hardware to the pc"""}
    }, 
    {'chapter' : 
        {'name': 'Testing'},
        {'index': '1.3'},
        {'content': """Before shipping the computer please test it"""}
    }, 
    {'chapter' : 
        {'name': 'Testing'},
        {'index': '1.3.1'},
        {'content': """
        Follow the folling steps:

            1. Power on
            2. Check for smoke"""}
    }, 
    {'chapter' : 
        {'name': 'Package'},
        {'index': '1.4'},
        {'content': """return to sender"""}
    }
    ]  
}
</Result:JSON>