import os
import json
import time
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

def get_search_videos(query, limit=10):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            if 'entries' in result:
                return [(entry['id'], entry.get('title', '')) for entry in result['entries']]
    except Exception as e:
        print(f"Error extracting search {query}: {e}")
    return []

def scrape_youtube_transcripts(queries, output_file="data/youtube_transcripts_raw.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Scraping YouTube transcripts for {len(queries)} search queries...")
    total_records = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for query in queries:
            print(f"\nProcessing query: {query}")
            videos = get_search_videos(query, limit=10)
            print(f"Found {len(videos)} videos.")
            
            for video_id, title in videos:
                try:
                    # Clean title for windows console printing
                    safe_title = title.encode('ascii', 'ignore').decode()
                    
                    api = YouTubeTranscriptApi()
                    transcript_list = api.list(video_id)
                    # Try to find a transcript (en) or grab whatever is generated
                    try:
                        transcript = transcript_list.find_transcript(['en']).fetch()
                    except:
                        # Fallback to whatever first transcript exists
                        transcript = [t for t in transcript_list][0].fetch()
                        
                    # Combine the text
                    full_text = " ".join([t['text'] for t in transcript]).replace('\n', ' ')
                    
                    if len(full_text) > 200:
                        record = {
                            "messages": [
                                {"role": "user", "content": f"Explain the industrial automation concepts covered in the tutorial titled: '{title}'"},
                                {"role": "assistant", "content": full_text}
                            ]
                        }
                        f.write(json.dumps(record) + "\n")
                        total_records += 1
                        print(f"  [+] Downloaded transcript for: {safe_title}")
                except Exception as e:
                    safe_title = title.encode('ascii', 'ignore').decode() if 'title' in locals() else 'Unknown'
                    print(f"  [-] Skipped {safe_title}: No transcript available or error ({type(e).__name__}).")
                time.sleep(1.5) # Rate limit protection
                
    print(f"\nSaved to {output_file} with {total_records} transcript records.")

if __name__ == "__main__":
    target_queries = [
        "Siemens TIA Portal Structured Text tutorial",
        "Beckhoff TwinCAT 3 tutorial",
        "PID Control PLC tutorial"
    ]
    scrape_youtube_transcripts(target_queries)
