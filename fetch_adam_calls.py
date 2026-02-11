#!/usr/bin/env python3
"""Fetch all HubSpot calls for Adam Jackson and extract action items."""

import os
import requests
import json
import re
from datetime import datetime
from html.parser import HTMLParser

API_TOKEN = os.environ.get("HUBSPOT_API_TOKEN", "")
OWNER_ID = "87407439"
BASE_URL = "https://api.hubapi.com/crm/v3/objects/calls/search"

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_html(html):
    if not html:
        return ""
    s = HTMLStripper()
    s.feed(html)
    return s.get_data().strip()

def fetch_all_calls():
    """Fetch all calls with pagination."""
    all_calls = []
    after = None
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    while True:
        payload = {
            "filterGroups": [{
                "filters": [
                    {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                    {"propertyName": "hs_timestamp", "operator": "GTE", "value": "1736976000000"}
                ]
            }],
            "properties": ["hs_call_title", "hs_call_body", "hs_timestamp", "hs_call_disposition"],
            "limit": 100,
            "sorts": [{"propertyName": "hs_timestamp", "direction": "DESCENDING"}]
        }
        
        if after:
            payload["after"] = after
        
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        calls = data.get("results", [])
        all_calls.extend(calls)
        print(f"Fetched {len(calls)} calls, total: {len(all_calls)}")
        
        paging = data.get("paging", {})
        if "next" in paging:
            after = paging["next"]["after"]
        else:
            break
    
    return all_calls

def has_meaningful_notes(call):
    """Check if call has actual notes (not null, not just voicemail/no answer)."""
    body = call.get("properties", {}).get("hs_call_body")
    if not body:
        return False
    
    # Strip HTML and clean
    text = strip_html(body).lower().strip()
    
    # Skip if empty or just generic notes
    if not text or len(text) < 5:
        return False
    
    # Skip common non-actionable notes
    skip_patterns = [
        r"^no answer",
        r"^voicemail",
        r"^left voicemail",
        r"^vm$",
        r"^hung up$",
        r"^number cannot be completed",
        r"^misdial",
        r"^called the wrong",
        r"^busy$",
        r"^not interested$",
        r"^not interested/unqualified$",
    ]
    
    for pattern in skip_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return False
    
    return True

def extract_action_items(call):
    """Extract action items, follow-ups, and tasks from call notes."""
    props = call.get("properties", {})
    body = props.get("hs_call_body", "")
    timestamp = props.get("hs_timestamp", "")
    title = props.get("hs_call_title", "")
    
    # Parse date
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        date_str = dt.strftime("%Y-%m-%d")
    except:
        date_str = timestamp[:10] if timestamp else "Unknown"
    
    # Extract contact name from title
    contact = "Unknown"
    if "Call with " in title:
        contact = title.replace("Call with ", "").strip()
    
    # Clean body text
    text = strip_html(body)
    
    # Look for action items
    actions = []
    
    # Keywords that indicate action items
    action_patterns = [
        r"@\w+[^\n]*",
        r"(?:needs?|need)\s+(?:an?\s+)?email[^\n]*",
        r"(?:send|shoot)\s+(?:him|her|them)\s+an?\s+email[^\n]*",
        r"follow\s*up[^\n]*",
        r"call\s+(?:him|her|them)\s+back[^\n]*",
        r"try\s+again[^\n]*",
        r"will\s+(?:call|email|reach\s+out)[^\n]*",
        r"referring\s+(?:me|us)\s+to[^\n]*",
        r"contact:\s*[^\n]+",
        r"\d{3}-\d{3}-\d{4}",  # Phone numbers
        r"\S+@\S+\.\S+",  # Email addresses
        r"(?:dm|decision\s+maker)[^\n]*",
        r"set\s+(?:a\s+)?follow\s*up[^\n]*",
        r"(?:he|she)\s+(?:said|would|will|agreed)[^\n]*",
    ]
    
    for pattern in action_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            action = match.group(0).strip()
            if action and len(action) > 3:
                actions.append(action)
    
    # If no specific actions found but there are notes, include a summary
    if not actions and text:
        # Get first 2-3 sentences as context
        sentences = re.split(r'[.!?]+', text)
        summary = '. '.join([s.strip() for s in sentences[:2] if s.strip()])
        if summary:
            actions.append(summary[:200] + "..." if len(summary) > 200 else summary)
    
    return {
        "date": date_str,
        "contact": contact,
        "actions": actions,
        "full_notes": text[:500] if text else ""
    }

def main():
    print("Fetching all calls from HubSpot...")
    calls = fetch_all_calls()
    print(f"\nTotal calls fetched: {len(calls)}")
    
    # Filter for calls with meaningful notes
    meaningful_calls = [c for c in calls if has_meaningful_notes(c)]
    print(f"Calls with meaningful notes: {len(meaningful_calls)}")
    
    # Extract action items
    results = []
    for call in meaningful_calls:
        result = extract_action_items(call)
        if result["actions"]:
            results.append(result)
    
    # Sort by date
    results.sort(key=lambda x: x["date"], reverse=True)
    
    # Output formatted results
    print("\n" + "="*80)
    print("ACTION ITEMS FROM ADAM JACKSON'S CALL NOTES")
    print("Period: Jan 15 - Feb 10, 2026")
    print("="*80 + "\n")
    
    for item in results:
        print(f"📅 {item['date']} | 👤 {item['contact']}")
        for action in item['actions']:
            print(f"   • {action}")
        print()
    
    # Also save to file
    with open("/Users/nico-yardlogix/.openclaw/workspace/adam_call_tasks.md", "w") as f:
        f.write("# Action Items from Adam Jackson's Call Notes\n\n")
        f.write("**Period:** Jan 15 - Feb 10, 2026\n")
        f.write(f"**Total Calls:** {len(calls)}\n")
        f.write(f"**Calls with Notes:** {len(meaningful_calls)}\n")
        f.write(f"**Tasks/Action Items Found:** {len(results)}\n\n")
        f.write("---\n\n")
        
        current_date = None
        for item in results:
            if item['date'] != current_date:
                current_date = item['date']
                f.write(f"\n## {current_date}\n\n")
            
            f.write(f"### {item['contact']}\n\n")
            for action in item['actions']:
                f.write(f"- {action}\n")
            if item['full_notes'] and len(item['full_notes']) > 50:
                f.write(f"\n> _{item['full_notes'][:300]}{'...' if len(item['full_notes']) > 300 else ''}_\n")
            f.write("\n")
    
    print(f"\n✅ Results saved to: adam_call_tasks.md")
    return results

if __name__ == "__main__":
    main()
