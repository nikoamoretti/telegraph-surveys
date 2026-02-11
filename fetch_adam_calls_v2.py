#!/usr/bin/env python3
"""Fetch all HubSpot calls for Adam Jackson and extract action items - v2."""

import os
import requests
import json
import re
from datetime import datetime
from html import unescape

API_TOKEN = os.environ.get("HUBSPOT_API_TOKEN", "")
OWNER_ID = "87407439"
BASE_URL = "https://api.hubapi.com/crm/v3/objects/calls/search"

def strip_html(html):
    """Remove HTML tags and decode entities."""
    if not html:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Decode HTML entities
    text = unescape(text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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
        print(f"Fetched {len(calls)} calls, total: {len(all_calls)}", file=__import__('sys').stderr)
        
        paging = data.get("paging", {})
        if "next" in paging:
            after = paging["next"]["after"]
        else:
            break
    
    return all_calls

def has_meaningful_notes(call):
    """Check if call has actual notes with potential action items."""
    body = call.get("properties", {}).get("hs_call_body")
    if not body:
        return False
    
    text = strip_html(body).lower().strip()
    
    # Must have some content
    if len(text) < 10:
        return False
    
    # Skip purely informational notes without action items
    non_action_patterns = [
        r"^(?:no answer|voicemail|left voicemail|vm|hung up|busy|wrong number|misdial|number cannot be completed)",
        r"^(?:not interested|unqualified|doesn'?t ship on rail|supplies to rail)",
        r"^mailbox (?:is full|hasn'?t been set up)",
        r"^rings? then dead air",
        r"^rang once",
        r"^(?:he|she) said (?:no|they have|all of)",
    ]
    
    for pattern in non_action_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return False
    
    return True

def extract_key_info(call):
    """Extract key action items and contact info from call notes."""
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
    
    # Initialize result
    result = {
        "date": date_str,
        "contact": contact,
        "emails": [],
        "phones": [],
        "mentions": [],
        "action_items": [],
        "follow_ups": [],
        "notes": text
    }
    
    # Extract emails
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    result["emails"] = list(set(emails))
    
    # Extract phone numbers (various formats)
    phone_patterns = [
        r'\b\d{3}-\d{3}-\d{4}\b',
        r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',
        r'\b\d{3}\.\d{3}\.\d{4}\b',
        r'\b\d{10}\b',
    ]
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        result["phones"].extend(phones)
    result["phones"] = list(set(result["phones"]))
    
    # Find mentions (@Nicolas, etc.)
    mentions = re.findall(r'@\w+(?:\s+\w+)*', text)
    result["mentions"] = mentions
    
    # Look for action item keywords and phrases
    action_keywords = [
        (r"needs?\s+(?:an?\s+)?email", "Needs email"),
        (r"send\s+(?:him|her|them)\s+(?:an?\s+)?email", "Send email"),
        (r"@Nicolas\s+Amoretti[^.]*", "Nico action"),
        (r"(?:ask|asking)\s+for\s+(?:an?\s+)?email", "Asked for email"),
        (r"follow\s*up\s+(?:set|needed|to|scheduled)", "Follow-up needed"),
        (r"call\s+(?:him|her|them)\s+back", "Call back"),
        (r"try\s+again", "Try again"),
        (r"will\s+(?:call|email|reach\s+out|try)", "Will follow up"),
        (r"referring\s+(?:me|us)\s+to", "Referral"),
        (r"contact:\s*([^,\n.]+)", "Contact info"),
        (r"DM[^.]*\d{3}", "DM with phone"),
        (r"booked\s+for", "Meeting booked"),
        (r"set\s+(?:a\s+)?meeting", "Meeting set"),
        (r"(?:he|she)\s+(?:agreed|said\s+(?:yes|to)|would)", "Positive response"),
    ]
    
    for pattern, label in action_keywords:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            snippet = match.group(0).strip()
            # Get surrounding context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            result["action_items"].append({
                "type": label,
                "snippet": snippet,
                "context": context
            })
    
    return result

def main():
    print("Fetching all calls from HubSpot...", file=__import__('sys').stderr)
    calls = fetch_all_calls()
    print(f"\nTotal calls fetched: {len(calls)}", file=__import__('sys').stderr)
    
    # Filter for calls with meaningful notes
    meaningful_calls = [c for c in calls if has_meaningful_notes(c)]
    print(f"Calls with actionable notes: {len(meaningful_calls)}", file=__import__('sys').stderr)
    
    # Extract info from each call
    results = []
    for call in meaningful_calls:
        result = extract_key_info(call)
        # Only include if there are actual action items or contact info
        if result["action_items"] or result["emails"] or result["mentions"]:
            results.append(result)
    
    # Sort by date
    results.sort(key=lambda x: x["date"], reverse=True)
    
    # Generate output
    output = []
    output.append("# Action Items from Adam Jackson's Call Notes\n")
    output.append("**Period:** January 15 - February 10, 2026\n")
    output.append(f"**Total Calls:** {len(calls)}\n")
    output.append(f"**Calls with Actionable Notes:** {len(meaningful_calls)}\n")
    output.append(f"**Tasks/Action Items Found:** {len(results)}\n")
    output.append("\n---\n")
    
    current_date = None
    for item in results:
        if item['date'] != current_date:
            current_date = item['date']
            output.append(f"\n## {current_date}\n")
        
        output.append(f"\n### {item['contact']}\n")
        
        # Add contact info
        if item['emails']:
            output.append(f"📧 **Emails:** {', '.join(item['emails'])}\n")
        if item['phones']:
            output.append(f"📞 **Phones:** {', '.join(item['phones'])}\n")
        if item['mentions']:
            output.append(f"👤 **Mentions:** {', '.join(item['mentions'])}\n")
        
        # Add action items
        if item['action_items']:
            output.append("\n**Action Items:**\n")
            seen = set()
            for action in item['action_items']:
                key = action['context'][:50]
                if key not in seen:
                    seen.add(key)
                    output.append(f"- [{action['type']}] {action['context']}\n")
        
        # Add notes summary
        if len(item['notes']) > 100:
            summary = item['notes'][:300] + "..." if len(item['notes']) > 300 else item['notes']
            output.append(f"\n> _{summary}_\n")
        
        output.append("\n")
    
    # Save to file
    output_text = ''.join(output)
    with open("/Users/nico-yardlogix/.openclaw/workspace/adam_call_tasks.md", "w") as f:
        f.write(output_text)
    
    # Also print to console
    print(output_text)
    print(f"\n✅ Results saved to: adam_call_tasks.md", file=__import__('sys').stderr)
    
    return results

if __name__ == "__main__":
    main()
