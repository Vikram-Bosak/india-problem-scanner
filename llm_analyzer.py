import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def analyze_problems(scanned_data):
    """
    Sends the scanned news headlines to NVIDIA Nemotron via OpenAI client to rank and analyze the Top 5 problems.
    """
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1")
    model = os.getenv("LLM_MODEL", "nvidia/nemotron-3-super-120b-a12b")

    if not api_key or "your_" in api_key:
        print("NOTE: LLM API Key not found. Using MOCK report for testing.")
        return """
📅 DATE: 20 March 2026
🌡️ INDIA MOOD: Testing Mode - The agent is verifying email delivery.

🔥 PROBLEM #1: युवा बेरोजगारी (Youth Unemployment)
... [MOCK CONTENT] ...
"""

    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )
    
    # Flatten the news data into a string
    news_context = "\n".join([f"- {d['title']} (Source: {d['source']})" for d in scanned_data])
    
    prompt = f"""
    You are the 'INDIA PROBLEM SCANNER AGENT' 🇮🇳. 
    Your mission is to find 5 critical problems in India TODAY that can be solved by a Tech Startup (AI, Mobile App, or Web Platform).
    Current Date: 20 March 2026
    
    INPUT DATA (Scanned Headlines):
    {news_context}
    
    ANALYSIS CRITERIA:
    1. **Scale**: Affects millions of common people.
    2. **Solvability**: Can be fixed using code/AI/SaaS (ignore purely political or religious issues).
    3. **Gap**: Current Government or NGO solutions are either too slow, corrupt, or inefficient.
    4. **Monetizable**: Has a clear market size and revenue potential.
    
    TASK: Provide a detailed analysis of the TOP 5 problems.
    You MUST return the output as a JSON LIST of 5 objects. Each object must have:
    - title: [देवरनागरी लिपि में हिंदी + English Mix]
    - description: Deep explanation of the problem in Devanagari (at least 3-4 sentences). Use simple daily words.
    - impact: Data/numbers in Devanagari.
    - why_failed: Clear reason in Devanagari.
    - startup_idea: Name.
    - tech_solution: How it works (Deep detail in Devanagari + English technical terms).
    - features: MUST BE A LIST OF STRINGS (at least 4-5 core features).
    - scalability: Growth plan.
    - market_size: Revenue potential.
    - is_real_problem: 2 sentences validation in Devanagari.

    LANGUAGE RULE: 
    1. STRICTLY use 'Ekdam Aasaan Bolchaal ki Hindi' (Very simple daily Hindi).
       - Examples: 'Flight cancel hona' (not रद्दीकरण), 'Pareshaani' (not असुविधा), 'Sahi time pe jaankari' (not वास्तविक समय सूचना), 'Option milna' (not वैकल्पिक विकल्प).
    2. All Hindi MUST be in DEVANAGARI SCRIPT (हिंदी लिपि).
    3. Use English only for tech terms (AI, App, Startup).
    4. Write like you are explaining to a 10th-standard student in simple words.
    
    RETURN ONLY THE JSON BLOCK. NO MARKDOWN AROUND IT.
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        top_p=0.95,
        max_tokens=16384,
        stream=False  # Switch to False for JSON stability
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    # Mock for local logic check
    mock_data = [{"title": "Heatwave in India", "source": "TOI"}]
    # print(analyze_problems(mock_data))
    print("NVIDIA-based Analyzer ready.")

if __name__ == "__main__":
    # Mock data for testing
    mock_data = [{"title": "Rising heatwaves in Delhi", "source": "TOI"}, {"title": "Youth unemployment hits new high", "source": "NDTV"}]
    # print(analyze_problems(mock_data))
    print("Analyzer ready. (Run with valid API key to test)")
