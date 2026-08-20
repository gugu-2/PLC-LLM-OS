import urllib.request
import json

def search_hf(type, query):
    url = f'https://huggingface.co/api/{type}?search={query}&limit=20&sort=downloads&direction=-1'
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error searching {type} for {query}: {e}")
        return []

print('--- MODELS ---')
for q in ['PLC', 'IEC 61131-3', 'Structured Text']:
    res = search_hf('models', q.replace(' ', '+'))
    if res:
        print(f'\nQuery: {q}')
        for m in res[:10]:
            print(f"- {m.get('id', 'N/A')} (Downloads: {m.get('downloads', 0)}, Likes: {m.get('likes', 0)})")

print('\n--- DATASETS ---')
for q in ['PLC', 'IEC 61131-3', 'Structured Text']:
    res = search_hf('datasets', q.replace(' ', '+'))
    if res:
        print(f'\nQuery: {q}')
        for d in res[:10]:
            print(f"- {d.get('id', 'N/A')} (Downloads: {d.get('downloads', 0)}, Likes: {d.get('likes', 0)})")
