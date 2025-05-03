#!/usr/bin/env python
# AD_gen/ad_generator.py

import sys, os, re, io, psycopg2, openai
from dotenv import load_dotenv

# Make stdout UTF-8 safe on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Load environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_top_trends(limit=5):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    with conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT topic, summary
            FROM google_trends_now
            ORDER BY scraped_date DESC, id ASC
            LIMIT %s
            """,
            (limit,)
        )
        return cur.fetchall()

def _simple_hashtags(text, max_tags=3):
    words = []
    for w in re.findall(r"\b\w{4,}\b", text.lower()):
        if w not in words:
            words.append(w)
        if len(words) >= max_tags:
            break
    return " ".join(f"#{w.capitalize()}" for w in words)

def generate_ads(product, description, trends, tone="casual", want_tags=False):
    tone_map = {
        "casual": "a regular tone",
        "formal": "a professional, formal tone",
        "gen-z": "an enthusiastic Gen-Z tone (slang welcome!)",
    }
    tone_phrase = tone_map.get(tone.lower(), tone_map["casual"])

    prompt = (
        f"You are a world-class copywriter.\n"
        f"Write each ad in **{tone_phrase}**.\n"
        f"The client sells **{product}**.\n"
        f"Description: {description}\n\n"
        "For each trend below, deliver ONE punchy social-media style ad (≤25 words):\n\n"
    )
    for i, (topic, summary) in enumerate(trends, 1):
        prompt += f"{i}. Trend: {topic}\n   Summary: {summary}\n   Ad:\n"
    prompt += "\nGenerate all ads now."

    # 1) Try new ChatCompletion
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Produce short, trend-based ad copy."},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=500,
            temperature=0.8,
        )
        raw = resp.choices[0].message.content

    # 2) Fallback to classic Completion if needed
    except AttributeError:
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.8,
        )
        raw = resp.choices[0].text

    ads = []
    for line in raw.splitlines():
        txt = line.strip()
        if not txt:
            continue
        txt = re.sub(r"^\s*\d+[\.)]\s*", "", txt)
        if want_tags:
            txt += "  " + _simple_hashtags(txt)
        ads.append(txt)
    return ads

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python ad_generator.py <product> <description> <tone> <yes|no>")
        sys.exit(1)

    product, desc, tone_arg, flag = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    include_tags = flag.lower() in {"yes","true","1","y"}

    print(f"[ad_generator] args → product={product!r}, desc={desc!r}, tone={tone_arg!r}, tags={include_tags}")
    trends = fetch_top_trends()
    print(f"[ad_generator] fetched trends = {trends!r}")

    try:
        for ad in generate_ads(product, desc, trends, tone_arg, include_tags):
            print(ad)
        sys.exit(0)
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)