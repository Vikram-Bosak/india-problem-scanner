import os
import datetime
from scraper import scan_all
from llm_analyzer import analyze_problems
from emailer import send_email
from dotenv import load_dotenv

# Set timezone for IST
# On Linux, we can set the TZ environment variable
os.environ['TZ'] = 'Asia/Kolkata'

# Only load .env if not in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    load_dotenv()

def run_daily_agent():
    print(f"--- India Problem Scanner Agent Started: {datetime.datetime.now()} ---")
    
    # 1. SCAN
    print("Step 1: Scanning news and portals...")
    scanned_data = scan_all()
    
    if not scanned_data:
        print("No news data found during scan.")
        return

    # 2 & 3 & 4. ANALYZE, SELECT, DEEP ANALYSIS
    print(f"Step 2-4: Analyzing {len(scanned_data)} items with LLM...")
    report_body = analyze_problems(scanned_data)
    
    if "ERROR" in report_body:
        print(f"Analysis failed: {report_body}")
        return

    # 5. EMAIL FORMAT & SEND
    print("Step 5: Formatting and Sending daily email...")
    date_str = datetime.datetime.now().strftime("%d %B %Y")
    
    from emailer import format_as_html
    html_report = format_as_html(report_body, date_str)
    
    subject = f"🚀 दैनिक स्टार्टअप अवसर (Daily Startup Opportunities) - {date_str}"
    
    recipient = os.getenv("RECIPIENT_EMAIL", "test@example.com")
    success = send_email(subject, html_report, recipient)
    
    if success:
        print("Daily report successfully delivered.")
    else:
        print("Report delivery failed.")

if __name__ == "__main__":
    run_daily_agent()
