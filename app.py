import gradio as gr
import requests
import json
import datetime
from fpdf import FPDF

# --- CONFIGURATION ---
# ✅ FIXED: Using 'qwen2.5:1.5b' (The Nano Model).
# It is fast, smart, and fits perfectly in your laptop's RAM.
MODEL_NAME = "qwen2.5:1.5b" 
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# --- PART 1: THE BRAIN (Cybersecurity Logic) ---
def analyze_log(log_entry):
    if not log_entry or len(log_entry.strip()) < 5:
        return "[SYSTEM WARNING] Log entry is too short."

    # ✅ UPDATED PROMPT: Rules to stop the model from guessing "Brute Force" for everything
    system_prompt = """
    You are a Cyber Security Analyst. 
    Analyze the server log below and classify the attack correctly.
    
    RULES FOR CLASSIFICATION:
    - If you see '<script>', label as: Cross-Site Scripting (XSS)
    - If you see '../', label as: Path Traversal
    - If you see 'UNION' or 'SELECT', label as: SQL Injection
    - If you see '; cat' or '; whoami', label as: Command Injection
    - If you see many failed logins, label as: Brute Force
    
    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    THREAT LEVEL: [High / Critical / Medium / Low]
    ATTACK VECTOR: [Use one of the labels above]
    ANALYSIS: [Explain specifically what the attacker is trying to steal]
    REMEDIATION: [Specific technical fix]
    """
    
    final_prompt = f"{system_prompt}\n\nLOG:\n{log_entry}"
    payload = {"model": MODEL_NAME, "prompt": final_prompt, "stream": False}

    try:
        print(f"📡 Sending log to {MODEL_NAME}...")
        
        # Timeout set to 120s (Your safety net for slower laptops)
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            return response.json().get("response", "❌ Error: Empty response.")
        elif response.status_code == 404:
            return f"❌ Error: Model '{MODEL_NAME}' not found. Keep the terminal window open!"
        else:
            return f"❌ HTTP Error {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "❌ TIMEOUT: Model took too long (>120s)."
    except requests.exceptions.ConnectionError:
        return "❌ CONNECTION ERROR: Ollama is not reachable. Is the black terminal window open?"
    except Exception as e:
        return f"❌ INTERNAL ERROR: {str(e)}"

# --- PART 2: PDF GENERATOR ---
def export_to_pdf(log_data, report_text):
    if not report_text or "❌" in report_text or "[SYSTEM WARNING]" in report_text:
        return None
        
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="SENTINEL AI - INCIDENT REPORT", ln=True, align='C')
    pdf.ln(10)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {timestamp}", ln=True)
    pdf.cell(200, 10, txt=f"Analyst AI: {MODEL_NAME}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. SUSPICIOUS LOG ENTRY", ln=True)
    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 5, txt=log_data)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. INTELLIGENCE ANALYSIS", ln=True)
    pdf.set_font("Arial", size=11)
    
    # Fix encoding issues for PDF
    safe_text = report_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, txt=safe_text)
    
    filename = f"Incident_Report_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# --- PART 3: THE UI ---
custom_css = """
body {background-color: #0b0f19;}
.gradio-container {font-family: 'Courier New', monospace;}
"""

with gr.Blocks(theme=gr.themes.Default(), css=custom_css) as demo:
    gr.Markdown("# 🛡️ SENTINEL: AI THREAT HUNTER")
    
    with gr.Row():
        with gr.Column(scale=1):
            log_input = gr.Textbox(label="Raw Server Log", placeholder="Paste log here...", lines=8)
            with gr.Row():
                clear_btn = gr.ClearButton([log_input])
                scan_btn = gr.Button("🚨 INITIATE SCAN", variant="primary")
        
        with gr.Column(scale=1):
            report_output = gr.Textbox(label="Intelligence Output", lines=12, interactive=False)
            pdf_btn = gr.Button("📄 Download Official PDF Report")
            pdf_file = gr.File(label="Download", interactive=False)

    scan_btn.click(fn=analyze_log, inputs=log_input, outputs=report_output)
    pdf_btn.click(fn=export_to_pdf, inputs=[log_input, report_output], outputs=pdf_file)

if __name__ == "__main__":
    demo.launch()