# SnapReport

**Automated Real Estate Market Intelligence & Predictive Pipeline**

SnapReport Pro is a lightweight, asynchronous FastAPI web application designed to instantly compile and deliver enterprise-grade real estate market reports. Built as a Minimum Viable Product (MVP), it combines market data analytics with AI-powered insights to empower real estate agents with professional, data-driven neighborhood intelligence.

---

## 🎯 Core Features

### Asynchronous Gateway
- Built on **FastAPI/ASGI** standards for rapid, non-blocking network request handling
- Automatic Pydantic data validation for robust API contracts

### Decoupled Data Registry
- O(1) local staging matrix with 40+ primary tier-1 markets
- Immediate data retrieval without external API bottlenecks during MVP validation
- Extensible market data architecture

### Dynamic Layout Engine
- **ReportLab** powered PDF generation with pixel-perfect document compilation
- Custom Flowable typography, branded color palettes, and grid matrices
- Professional multi-section report layouts

### "Traffic Light" Market Signal System
- Visual condition indicators based on Days on Market (DOM) velocity:
  - 🟢 **Green**: DOM < 30 days (Strongly Favorable)
  - 🟡 **Yellow**: DOM 30-60 days (Moderately Favorable)
  - 🔴 **Red**: DOM > 60 days (Buyer-Leaning)

### Resilient AI Narrative Circuit
- Interfaces with **OpenAI (gpt-4o-mini)** for context-aware market analysis
- Generates sophisticated 3-sentence market advisories tailored to each neighborhood
- Includes automatic fallback narrative for API unavailability

### Market Coverage
Supports 40+ target markets across major US real estate corridors:
- West Coast, Northeast, Southeast, Midwest, Southwest, and Mountain regions

---

## 🚀 Installation & Deployment

### Prerequisites

- Python 3.9+
- FastAPI, Uvicorn, Pydantic
- OpenAI SDK
- ReportLab

### Setup Instructions

**1. Clone the Repository**
```bash
git clone https://github.com/jaydaulatkar/SnapReport.git
cd SnapReport
```

**2. Install Dependencies**
```bash
pip install fastapi uvicorn pydantic openai reportlab matplotlib
```

**3. Configure Environment**

Set your OpenAI API key (optional; defaults to fallback narrative if not configured):
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**4. Run the Server**

Start the Uvicorn ASGI server:
```bash
uvicorn snap_report_pro_v2:app --reload
```

Access the web interface at: `http://localhost:8000`

---

## 📋 API Reference

### Generate Market Report

**Endpoint**: `POST /api/generate-report`

**Request Body**:
```json
{
  "zip_code": "90210",
  "agent_name": "Jay Daulatkar"
}
```

**Response**:
- PDF file download: `Market_Report_{zip_code}.pdf`
- Content-Type: `application/pdf`

**Example**:
```bash
curl -X POST http://localhost:8000/api/generate-report \
  -H "Content-Type: application/json" \
  -d '{"zip_code": "94103", "agent_name": "Your Name"}' \
  -o report.pdf
```

### Web Portal

**Endpoint**: `GET /`

Interactive dashboard for agents to:
1. Input target ZIP code
2. Enter agent professional identity
3. Generate and download reports instantly

---

## 📊 Report Structure

Each generated report includes:

### 1. Market Signal Badge
Visual indicator based on DOM velocity with color-coded condition status

### 2. Market Indicators Table
- Median market valuation
- Average days on market (DOM)
- Months supply of inventory
- Market momentum trend

### 3. Expert Market Narrative Analysis
AI-generated contextual market advisory providing sophisticated, actionable insights

### 4. Strategic Homeowner Action Plan
Recommendations covering:
- Pricing calibration strategies
- Inventory scarcity indexing
- Modern buyer match optimization

### 5. Call-to-Action Section
Partnership and listing opportunity prompts with direct engagement links

### 6. Professional Signature Block
Agent branding and Snaphomz partnership identification

---

## 🔧 Configuration

### Environment Variables

```bash
# Required (optional with fallback)
OPENAI_API_KEY=your_api_key_here

# Infrastructure Hooks
S3_BUCKET=snaphomz-reports
SENDGRID_EMAIL=lead_distribution_node@snaphomz.com
```

### Branding Customization

Edit color constants in the code:
- **Primary**: `#0f172a` (Slate 900)
- **Accent**: `#0284c7` (Sky 600)
- **Success**: `#059669` (Emerald Green)
- **Warning**: `#d97706` (Amber)
- **Error**: `#dc2626` (Red)

### Adding New Markets

Edit `MOCK_MARKET_REGISTRY` dictionary:
```python
"12345": {
    "city": "City, State",
    "median_price": "$XXX,XXX",
    "days_on_market": XX,
    "inventory_months": X.X,
    "trend": "Market Trend Description"
}
```

---

## 🔌 Integration Architecture

### AWS S3 Integration
```python
upload_to_s3(file_path, bucket_name="snaphomz-reports")
```
Simulates archiving generated PDFs to cloud storage.

### SendGrid Email Delivery
```python
dispatch_via_sendgrid(recipient_email, file_path)
```
Queues reports for automated email distribution.

---

## 🤖 AI Integration

### OpenAI Configuration
- **Model**: `gpt-4o-mini`
- **Max Tokens**: 180
- **Context**: Real estate market analysis terminology and metrics

### Narrative Fallback
Automatic fallback ensures service continuity if OpenAI API is unavailable or throttled.

---

## 📈 Market Signal Intelligence

The "Traffic Light" system evaluates market conditions based on Days on Market (DOM):

| Condition | DOM Range | Signal | Implication |
|-----------|-----------|--------|------------|
| Strong Seller Advantage | < 30 days | 🟢 Green | High buyer competition, strong pricing leverage |
| Balanced Market | 30–60 days | 🟡 Yellow | Strategic pricing critical, moderate seller leverage |
| Buyer-Leaning Correction | > 60 days | 🔴 Red | Extended timelines, buyer negotiation advantage |

---

## 🚀 Future Scope: Machine Learning Forecasting

To maintain MVP execution constraints and zero-latency performance, the current predictive analytics relies on a standard linear projection. The architecture is deliberately decoupled to support seamless ML integration:

### Planned Enhancements
- **Advanced Time-Series Models**: Facebook Prophet, XGBoost, ARIMA
- **Data Scaling**: 5-to-10 year MLS dataset expansion (vs. current 6-month window)
- **Multivariate Forecasting**: Seasonal cycles, interest rate impacts, neighborhood demographics
- **Institutional-Grade Forecasting**: Unparalleled predictive equity insights for clients

---

## 📁 Project Structure

```
snap_report_pro_v2.py
├── Market Data Registry (40+ ZIP codes)
├── API Routes
│   ├── POST /api/generate-report
│   └── GET /
├── PDF Generation Pipeline
│   ├── ReportLab styling
│   ├── Market signal badges
│   └── Layout components
├── AI Integration
│   └── OpenAI GPT-4o-mini narratives
└── Distribution Hooks
    ├── AWS S3 archiving
    └── SendGrid email dispatch
```

---

## 🛠️ Development

### Extending Report Sections

Modify the `story` list in `generate_market_report()` to add custom sections using ReportLab Flowables.

### Customizing Styles

Adjust `ParagraphStyle` definitions to modify fonts, colors, spacing, and typography.

---

## 📞 Support

For issues or feature requests, please open an issue in the repository.

---

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ReportLab Documentation](https://www.reportlab.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

## 👤 Author

**Jay Daulatkar**

---
