import json

with open('assistant_content.txt', 'r', encoding='utf-8') as f:
    assistant_content = f.read()

data = {
    'messages': [
        {
            'role': 'user',
            'content': 'Design a highly complex IEC 61131-3 PLC program for an Extreme Ultraviolet (EUV) Laser Lithography Wafer Stage controller. The system must implement nanometer-precision linear motor positioning, active vibration cancellation using piezo actuators, and strict safety interlocks for the vacuum chamber pressure.'
        },
        {
            'role': 'assistant',
            'content': assistant_content
        }
    ]
}

with open(r'data\evol_instruct_dataset.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\n')
