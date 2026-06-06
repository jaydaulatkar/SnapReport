import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

# Enterprise Layout Engine Modules
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(title="SnapReport MVP Pipeline")

# --- Enterprise Configuration Keys ---
# Paste your actual OpenAI key here if available, or set it via terminal env vars.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_ACTUAL_OPENAI_KEY_HERE")

# Initialize OpenAI Client Gateway
client = OpenAI(api_key=OPENAI_API_KEY if "YOUR_ACTUAL" not in OPENAI_API_KEY else "mock_key")

# --- MVP LOCAL REGISTRY DATASET (20 CORE TARGET MARKETS) ---
MOCK_MARKET_REGISTRY = {
    
    "90210": {"city": "Beverly Hills, CA", "median_price": "$5,700,000", "days_on_market": 75, "inventory_months": 5.4, "trend": "Strong Seller Advantage"},
    "94103": {"city": "San Francisco, CA", "median_price": "$1,360,000", "days_on_market": 14, "inventory_months": 1.8, "trend": "High-Velocity Corridors"},
    "75001": {"city": "Dallas, TX", "median_price": "$375,000", "days_on_market": 82, "inventory_months": 10.1, "trend": "Buyer-Leaning Correction"},
    "10001": {"city": "New York, NY", "median_price": "$1,850,000", "days_on_market": 94, "inventory_months": 6.2, "trend": "Stable Metropolitan Baseline"},
    "90028": {"city": "Hollywood, CA", "median_price": "$985,000", "days_on_market": 45, "inventory_months": 3.1, "trend": "Moderate Luxury Equilibrium"},
    "33139": {"city": "Miami Beach, FL", "median_price": "$2,450,000", "days_on_market": 68, "inventory_months": 4.8, "trend": "Accelerating Capital Inflow"},
    "60611": {"city": "Chicago, IL", "median_price": "$710,000", "days_on_market": 52, "inventory_months": 2.9, "trend": "Balanced Core Supply"},
    "78701": {"city": "Austin, TX", "median_price": "$494,000", "days_on_market": 89, "inventory_months": 7.5, "trend": "Post-Boom Supply Correction"},
    "98101": {"city": "Seattle, WA", "median_price": "$875,000", "days_on_market": 21, "inventory_months": 1.5, "trend": "Aggressive Tech In-Migration"},
    "02108": {"city": "Boston, MA", "median_price": "$1,650,000", "days_on_market": 33, "inventory_months": 2.1, "trend": "Constrained Historical Supply"},
    "80202": {"city": "Denver, CO", "median_price": "$645,000", "days_on_market": 38, "inventory_months": 2.6, "trend": "Steady Mountain Demographics"},
    "85251": {"city": "Scottsdale, AZ", "median_price": "$820,000", "days_on_market": 41, "inventory_months": 3.4, "trend": "Sunbelt Expansion Vectors"},
    "20001": {"city": "Washington, DC", "median_price": "$795,000", "days_on_market": 49, "inventory_months": 2.8, "trend": "Resilient Institutional Baseline"},
    "30303": {"city": "Atlanta, GA", "median_price": "$415,000", "days_on_market": 43, "inventory_months": 3.2, "trend": "Regional Growth Absorption"},
    "37203": {"city": "Nashville, TN", "median_price": "$585,000", "days_on_market": 56, "inventory_months": 4.1, "trend": "Decentralized Corporate Inflow"},
    "89109": {"city": "Las Vegas, NV", "median_price": "$510,000", "days_on_market": 37, "inventory_months": 2.5, "trend": "High-Yield Speculative Velocity"},
    "92101": {"city": "San Diego, CA", "median_price": "$925,000", "days_on_market": 28, "inventory_months": 1.9, "trend": "Extreme Coastal Density"},
    "70112": {"city": "New Orleans, LA", "median_price": "$390,000", "days_on_market": 71, "inventory_months": 5.9, "trend": "Tourism-Adjacent Stabilization"},
    "19103": {"city": "Philadelphia, PA", "median_price": "$465,000", "days_on_market": 61, "inventory_months": 4.0, "trend": "Industrial Core Consolidation"},
    "94016": {"city": "Daly City, CA", "median_price": "$1,150,000", "days_on_market": 18, "inventory_months": 1.4, "trend": "Metropolitan Spillover Demand"},
    "43215": {"city": "Columbus, OH", "median_price": "$385,000", "days_on_market": 24, "inventory_months": 1.7, "trend": "High Midwest Affordability Advantage"},
    "46204": {"city": "Indianapolis, IN", "median_price": "$320,000", "days_on_market": 29, "inventory_months": 2.0, "trend": "Steady Industrial In-Migration"},
    "63101": {"city": "St. Louis, MO", "median_price": "$245,000", "days_on_market": 44, "inventory_months": 3.1, "trend": "Balanced Secondary Market"},
    "55401": {"city": "Minneapolis, MN", "median_price": "$410,000", "days_on_market": 35, "inventory_months": 2.3, "trend": "Stable Corporate Base Corridor"},
    "64105": {"city": "Kansas City, MO", "median_price": "$295,000", "days_on_market": 22, "inventory_months": 1.6, "trend": "Accelerating Logistics Hub Growth"},
    "84101": {"city": "Salt Lake City, UT", "median_price": "$560,000", "days_on_market": 42, "inventory_months": 3.2, "trend": "Mountain Tech Belt Expansion"},
    "97201": {"city": "Portland, OR", "median_price": "$590,000", "days_on_market": 48, "inventory_months": 3.5, "trend": "Moderate Pacific Northwest Equilibrium"},
    "85003": {"city": "Phoenix, AZ", "median_price": "$455,000", "days_on_market": 39, "inventory_months": 2.9, "trend": "Sunbelt Inflow Consolidation"},
    "73102": {"city": "Oklahoma City, OK", "median_price": "$265,000", "days_on_market": 31, "inventory_months": 2.2, "trend": "Low-Friction Energy Corridor"},
    "77002": {"city": "Houston, TX", "median_price": "$340,000", "days_on_market": 54, "inventory_months": 4.5, "trend": "High-Volume Supply Equilibrium"},
    "32801": {"city": "Orlando, FL", "median_price": "$425,000", "days_on_market": 47, "inventory_months": 3.8, "trend": "Tourism-Driven Inflow Dynamics"},
    "27601": {"city": "Raleigh, NC", "median_price": "$495,000", "days_on_market": 26, "inventory_months": 1.9, "trend": "Research Triangle Tech Advantage"},
    "29401": {"city": "Charleston, SC", "median_price": "$975,000", "days_on_market": 58, "inventory_months": 4.2, "trend": "Historical Coastal Premium Market"},
    "33602": {"city": "Tampa, FL", "median_price": "$460,000", "days_on_market": 36, "inventory_months": 3.0, "trend": "Sunbelt Migration Resilience"},
    "19106": {"city": "Philadelphia, PA", "median_price": "$515,000", "days_on_market": 40, "inventory_months": 2.7, "trend": "Stable Historic Urban Core"},
    "07030": {"city": "Hoboken, NJ", "median_price": "$895,000", "days_on_market": 19, "inventory_months": 1.3, "trend": "Metropolitan Spillover Footprint"},
    "21201": {"city": "Baltimore, MD", "median_price": "$235,000", "days_on_market": 51, "inventory_months": 3.6, "trend": "Mid-Atlantic Value Corridor"},
    "95113": {"city": "San Jose, CA", "median_price": "$1,450,000", "days_on_market": 11, "inventory_months": 1.1, "trend": "Aggressive Silicon Valley Constraints"},
    "90401": {"city": "Santa Monica, CA", "median_price": "$1,890,000", "days_on_market": 63, "inventory_months": 4.9, "trend": "Coastal Luxury Resilience"},
    "80903": {"city": "Colorado Springs, CO", "median_price": "$430,000", "days_on_market": 33, "inventory_months": 2.4, "trend": "Steady Mountain Region Absorption"}
}

class ReportRequest(BaseModel):
    zip_code: str
    agent_name: str


# INFRASTRUCTURE WORKFLOW HOOKS (AWS S3 & SendGrid Simulation Traces)
def upload_to_s3(file_path: str, bucket_name: str = "snaphomz-reports"):
    """AWS S3 Storage Pipeline - Simulates immediate local file archiving link"""
    print(f"[S3 Upload Lifecycle Triggered]: Asset {file_path} archived in bucket '{bucket_name}'.")

def dispatch_via_sendgrid(recipient_email: str, file_path: str):
    """SendGrid Email Delivery Engine Hook"""
    print(f"[SendGrid Dispatch Lifecycle Triggered]: Distribution queued for delivery to {recipient_email}.")


# CORE PROCESSING PIPELINE & ASSET COMPILATION ROUTE
@app.post("/api/generate-report")
async def generate_market_report(request: ReportRequest):
    zip_code = request.zip_code.strip()
    agent_name = request.agent_name.strip()
    
    # Strict MVP Registry Fallback Matching Core O(1) Data Layer
    if zip_code in MOCK_MARKET_REGISTRY:
        stats = MOCK_MARKET_REGISTRY[zip_code]
    else:
        # Dynamic generation safeguard for out-of-bounds user entries
        stats = {
            "city": f"Regional Territory Vector ({zip_code})",
            "median_price": "$425,000",
            "days_on_market": 42,
            "inventory_months": 3.0,
            "trend": "Standard Nationwide Equilibrium"
        }

    # Fire Intelligence Narrative Loop
    narrative = ""
    if "YOUR_ACTUAL" not in OPENAI_API_KEY and os.environ.get("OPENAI_API_KEY"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are an elite, senior real estate data analyst writing a bespoke, high-context market advisory "
                            "narrative for an agent's neighborhood client base. Your goal is to interpret raw figures into "
                            "actionable economic insights. Use these underlying metric definitions to anchor your analysis:\n\n"
                            "- Median Market Valuation: The exact statistical middle baseline of local property values. Treat this "
                            "as the regional equity anchor. If it is high or expanding, focus on wealth preservation and equity realization.\n"
                            "- Average Days on Market (DOM): The absolute market velocity thermometer, tracking the time from MLS listing to contract. "
                            "A low DOM (under 30 days) indicates rapid turnover, intense buyer competition, and strong seller pricing leverage. "
                            "A high DOM (over 60 days) signals a cooling trend, inventory stagnation, and a clear shift toward buyer negotiation leverage.\n\n"
                            "Instructions:\n"
                            "1. Write a precisely bounded 3-sentence narrative analysis.\n"
                            "2. Avoid repeating the raw data points back-to-back mechanically; instead, translate *what* the relationship "
                            "between the velocity (DOM) and the value (Median Price) implies for a homeowner looking to sell.\n"
                            "3. Keep the tone sophisticated, authoritative, insightful, and crisp."
                        )
                    },
                    {
                        "role": "user", 
                        "content": (
                            f"Generate the expert narrative for the {stats['city']} footprint (ZIP Code: {zip_code}).\n"
                            f"Current Data Profile:\n"
                            f"- Median Market Valuation: {stats['median_price']}\n"
                            f"- Average Days on Market: {stats['days_on_market']} Days\n"
                            f"- Identified Market Momentum: {stats['trend']}"
                        )
                    }
                ],
                max_tokens=180
            )
            narrative = response.choices[0].message.content.strip()
        except Exception:
            pass

    # High-Yield Local Fallback Narrative if OpenAI Key is missing or throttles
    if not narrative:
        narrative = f"The residential market profile across the {stats['city']} footprint currently shows robust transaction patterns matching a trend of {stats['trend']}. With local properties establishing an average staying velocity of {stats['days_on_market']} days, listing liquidity remains consistently competitive. Homeowners tracking equity levels near the regional median price index of {stats['median_price']} are in an exceptionally strong position to coordinate custom selling strategies."

    output_filename = f"Market_Report_{zip_code}.pdf"

    try:
        # Initialize ReportLab flowable template container
        doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
        story = []
        
        styles = getSampleStyleSheet()
        
        # Establishing Branding Palette and Typography Classes
        PRIMARY_COLOR = colors.HexColor("#0f172a")  # Slate 900
        ACCENT_COLOR = colors.HexColor("#0284c7")   # Sky 600
        TEXT_COLOR = colors.HexColor("#334155")     # Slate 700
        
        title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, textColor=PRIMARY_COLOR, spaceAfter=4)
        subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#64748b"), spaceAfter=15)
        section_heading = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=PRIMARY_COLOR, spaceBefore=18, spaceAfter=8)
        
        label_style = ParagraphStyle('TableLabel', fontName='Helvetica-Bold', fontSize=11, textColor=PRIMARY_COLOR)
        val_style = ParagraphStyle('TableVal', fontName='Helvetica', fontSize=11, textColor=TEXT_COLOR)
        body_style = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=10, leading=15, textColor=TEXT_COLOR)
        
        bullet_label = ParagraphStyle('BulletLabel', fontName='Helvetica-Bold', fontSize=10, textColor=ACCENT_COLOR)
        bullet_text = ParagraphStyle('BulletText', fontName='Helvetica', fontSize=10, leading=14, textColor=TEXT_COLOR)
        
        cta_title = ParagraphStyle('CTATitle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#065f46"))
        cta_body = ParagraphStyle('CTABody', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#047857"))
        branding_style = ParagraphStyle('BrandFooter', fontName='Helvetica-BoldOblique', fontSize=11, textColor=colors.HexColor("#059669"))

        # --- DRAWING LAYOUT COMPONENTS ---
        # Document Title Header Block
        story.append(Paragraph("SNAPHOMZ LOCAL MARKET INTELLIGENCE", title_style))
        story.append(Paragraph(f"Data Compiled for Zip Code: {zip_code} ({stats['city']})", subtitle_style))
        
        # Cyan geometric horizontal rule separator
        divider = Table([[""]], colWidths=[540], rowHeights=[2])
        divider.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), ACCENT_COLOR)]))
        story.append(divider)
        story.append(Spacer(1, 10))

        # --- NEW PRODUCT FEATURE: THE "TRAFFIC LIGHT" MARKET ACTION BADGE ---
        # 1. Evaluate the velocity to determine the signal
        dom_value = int(stats['days_on_market'])
        
        if dom_value < 30:
            status_text = "STRONGLY FAVORABLE: EXCELLENT CONDITIONS TO LIST & SELL"
            text_color = colors.HexColor("#059669") # Emerald Green
            bg_color = colors.HexColor("#d1fae5")
            border_color = colors.HexColor("#34d399")
        elif dom_value <= 60:
            status_text = "MODERATELY FAVORABLE: STRATEGIC PRICING REQUIRED"
            text_color = colors.HexColor("#d97706") # Amber Yellow
            bg_color = colors.HexColor("#fef3c7")
            border_color = colors.HexColor("#fbbf24")
        else:
            status_text = "BUYER LEANING: EXPECT LONGER HOLD TIMES & NEGOTIATIONS"
            text_color = colors.HexColor("#dc2626") # Red
            bg_color = colors.HexColor("#fee2e2")
            border_color = colors.HexColor("#f87171")

        # 2. Build the visual Flowable badge
        status_style = ParagraphStyle('Status', fontName='Helvetica-Bold', fontSize=12, textColor=text_color, alignment=1)
        status_badge = Table([[Paragraph(f"INSTANT MARKET SIGNAL: {status_text}", status_style)]], colWidths=[540])
        status_badge.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1.5, border_color),
        ]))
        
        # 3. Inject it into the document layout right before the data grid
        story.append(status_badge)
        story.append(Spacer(1, 15))
        # --------------------------------------------------------------------

        # SECTION 1: Fixed Layout Metric Data Table
        story.append(Paragraph("Current Market Indicators", section_heading))
        grid_data = [
            [Paragraph("Median Market Valuation:", label_style), Paragraph(stats['median_price'], val_style)],
            [Paragraph("Average Days on Market:", label_style), Paragraph(f"{stats['days_on_market']} Days", val_style)],
            [Paragraph("Months Supply of Inventory:", label_style), Paragraph(f"{stats['inventory_months']} Months", val_style)],
            [Paragraph("Identified Market Momentum:", label_style), Paragraph(stats['trend'], val_style)]
        ]
        metric_table = Table(grid_data, colWidths=[200, 340])
        metric_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ]))
        story.append(metric_table)

        # SECTION 2: AI Analytical Assessment Text Block
        story.append(Paragraph("Expert Market Narrative Analysis", section_heading))
        story.append(Paragraph(narrative, body_style))
        story.append(Spacer(1, 10))

        # SECTION 3: Actionable Strategic Advisory Points
        story.append(Paragraph("Strategic Homeowner Action Plan", section_heading))
        bullet_points = [
            ("• Pricing Calibration:", f"With local inventory averaging a velocity of {stats['days_on_market']} days, aligning your listing strategy precisely with neighborhood comp bounds is critical to maximize upfront buyer leverage."),
            ("• Scarcity Indexing:", f"The recorded {stats['inventory_months']} months supply means market availability remains highly constrained. Showcasing pristine interior layouts will command premium transaction offers."),
            ("• Match Optimization:", "Over 90% of prospective buyers utilize modern lifestyle search profiles. Partner with your Snaphomz professional to verify complete visual data tracking before listing optimization.")
        ]
        bullet_data = []
        for b_title, b_text in bullet_points:
            bullet_data.append([Paragraph(b_title, bullet_label), Paragraph(b_text, bullet_text)])
        bullet_table = Table(bullet_data, colWidths=[120, 420])
        bullet_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(bullet_table)
        story.append(Spacer(1, 15))

        # SECTION 4: THE REVENUE FUNNEL (Mint-Emerald CTA Box with Active Hyperlink)
        cta_data = [[
            Paragraph("Ready to Unlock Realized Home Equity?", cta_title),
            Paragraph("POWERED BY SNAPHOMZ", branding_style)
        ], [
            Paragraph(f"Discover exactly how your property profile stacks up against local comps. Scan your partner agent portal or access your core dashboard link to list your property seamlessly across the Snaphomz network.", cta_body),
            Paragraph(f"<a href='https://snaphomz.com/list?referrer={agent_name.replace(' ', '_')}' color='#047857'><b>snaphomz.com/list</b></a>", cta_body)
        ]]
        cta_table = Table(cta_data, colWidths=[380, 160])
        cta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ecfdf5")),
            ('PADDING', (0,0), (-1,-1), 12),
            ('ALIGN', (1,0), (1,1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#a7f3d0")),
        ]))
        story.append(cta_table)
        story.append(Spacer(1, 20))

        # SECTION 5: Branded Professional Identity Signature Block
        footer_data = [[
            Paragraph(f"Presented Professionally by: {agent_name}<br/><font size=9 color='#64748b'>Your authorized Snaphomz Partner across the local market footprint.</font>", body_style),
            Paragraph("PARTNER AGENT HUB", ParagraphStyle('FooterHub', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#475569")))
        ]]
        footer_table = Table(footer_data, colWidths=[380, 160])
        footer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('PADDING', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ]))
        story.append(footer_table)

        # Trigger internal canvas compilation engine pass to disk
        doc.build(story)
        
        # Invoke background distribution and storage hooks safely
        upload_to_s3(output_filename)
        dispatch_via_sendgrid("lead_distribution_node@snaphomz.com", output_filename)

        # Stream raw completed asset bytes back to open user portal link immediately
        return FileResponse(path=output_filename, filename=output_filename, media_type='application/pdf')

    except Exception as compilation_error:
        print(f"[ReportLab Core Failure] Crash avoided: {compilation_error}")
        raise HTTPException(status_code=500, detail=f"PDF Compilation Anomaly: {str(compilation_error)}")


# MONOLITHIC DASHBOARD INTERFACE ROUTE (HTML UI Embed)
@app.get("/", response_class=HTMLResponse)
async def serve_portal():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Snaphomz - SnapReport MVP Studio</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-center p-4">
        <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl">
            <h1 class="text-2xl font-bold text-emerald-400 mb-1 text-center">SnapReport Studio</h1>
            <p class="text-xs text-slate-400 text-center mb-6">Automated MVP market insights built using ReportLab & OpenAI</p>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Target ZIP Code</label>
                    <input type="text" id="zip_code" value="90210" class="w-full bg-slate-800 border border-slate-700 rounded p-2.5 text-sm focus:outline-none focus:border-emerald-500 text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Agent Professional Identity</label>
                    <input type="text" id="agent_name" value="Jay Daulatkar" class="w-full bg-slate-800 border border-slate-700 rounded p-2.5 text-sm focus:outline-none focus:border-emerald-500 text-white">
                </div>
                <button onclick="compileReport()" id="action-btn" class="w-full bg-emerald-600 hover:bg-emerald-500 font-bold py-2.5 rounded text-sm transition-all text-white">
                    Compile Standard Corporate PDF Report
                </button>
            </div>
        </div>

        <script>
            async function compileReport() {
                const btn = document.getElementById('action-btn');
                const zipInput = document.getElementById('zip_code').value.trim();
                const agentInput = document.getElementById('agent_name').value.trim();

                if(!zipInput || !agentInput) {
                    alert("Please provide both parameter sets to build the report profile.");
                    return;
                }

                btn.disabled = true;
                btn.innerText = "Querying Local Registry & Structuring Flowables...";

                try {
                    const response = await fetch('/api/generate-report', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ zip_code: zipInput, agent_name: agentInput })
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const downloadUrl = window.URL.createObjectURL(blob);
                        const downloadAnchor = document.createElement('a');
                        downloadAnchor.href = downloadUrl;
                        downloadAnchor.download = `Market_Report_MVP_${zipInput}.pdf`;
                        document.body.appendChild(downloadAnchor);
                        downloadAnchor.click();
                        downloadAnchor.remove();
                    } else {
                        alert("The report compiler hit an unhandled engine compilation exception.");
                    }
                } catch (e) {
                    alert("Network transport layer execution error.");
                } finally {
                    btn.disabled = false;
                    btn.innerText = "Compile Standard Corporate PDF Report";
                }
            }
        </script>
    </body>
    </html>
    """