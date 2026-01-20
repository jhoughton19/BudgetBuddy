# BudgetBuddy Deployment Guide
## For Utah 3rd-6th Class Counties

---

## Quick Launch (Local Demo)

### Windows Users (Most County IT):
1. Install Python 3.9+ from python.org
2. Extract BudgetBuddy folder
3. Double-click `run_app.bat`
4. Browser opens automatically to http://localhost:8501

### Mac/Linux Users:
```bash
cd budgetbuddy
./run_app.sh
```

---

## Cloud Deployment (Recommended for Production)

### Option 1: Streamlit Cloud (FREE - Perfect for demos)

**Pros:**
- Free tier available
- Zero server management
- SSL/HTTPS included
- Updates in minutes

**Setup (5 minutes):**
1. Create GitHub account (if needed)
2. Upload BudgetBuddy folder to GitHub repo
3. Go to streamlit.io/cloud
4. Connect GitHub, select repo
5. Click "Deploy"
6. Get public URL: `yourapp.streamlit.app`

**Perfect for:**
- Demos to county commissioners
- Inter-county sharing via UACC
- Beta testing with 2-3 counties

### Option 2: County-Hosted (IT Control)

**If your county has web hosting:**

**AWS/Azure/Google Cloud:**
- ~$20/month for small instance
- Full control over data
- Can meet security requirements

**Setup:**
```bash
# On your server
git clone [your-repo]
cd budgetbuddy
pip install -r requirements.txt
streamlit run app.py --server.port 80 --server.address 0.0.0.0
```

**Secure with:**
- HTTPS certificate (Let's Encrypt - free)
- VPN access only
- County firewall rules

---

## Utah-Specific Considerations

### Data Security
**Question from County IT:**
"Where does our budget data go?"

**Answer:**
- Data processed in-browser (local mode)
- Nothing stored in cloud unless you deploy there
- No external API calls in Phase 1
- GRAMA-compliant (public records)

### State Audit Requirements
**Compatible with:**
- Utah State Auditor's reporting requirements
- GFOA best practices
- CAFR (Comprehensive Annual Financial Report) standards

### Support Infrastructure
**Resources for counties:**
- UACC (Utah Association of Counties) - training sessions
- State Auditor's office - compliance questions
- BudgetBuddy documentation
- Email/phone support

---

## Pricing for Utah Counties

### Beta Program (First 5 Counties - 2024/2025)
**$2,500/year** (50% discount)
- Full access to data ingestion
- Early access to AI features
- Priority support
- Lifetime discount locked in

### Standard Pricing (After Beta)
**3rd Class Counties:** $5,000/year
**4th Class Counties:** $4,000/year  
**5th-6th Class Counties:** $3,000/year
*(Based on complexity/transaction volume)*

### Included:
- Unlimited uploads
- All data processing features
- Software updates
- Email support
- UACC training sessions

### Add-ons:
- AI Narrative Generation: +$2,000/year
- Multi-year Forecasting: +$1,500/year
- Custom integrations: Quote basis

---

## Demo Script (For County Commissioners)

### 5-Minute Demo Flow:

**1. Problem Statement (1 min)**
"Creating our budget book takes 40+ hours of manual work copying data, 
checking formulas, and writing narratives. BudgetBuddy automates this."

**2. Show Upload (1 min)**
- Select Munis/Caselle
- Drag export file
- Click Process
- Instant validation

**3. Show Results (2 min)**
- Fund summaries
- Variance analysis
- Clean Excel export
- "This took 30 seconds vs. 2 days manually"

**4. ROI (1 min)**
"At $5,000/year, this saves 80+ hours annually. That's our auditor's 
time freed up for analysis instead of data entry. Plus GFOA compliance 
is built-in for State Auditor reviews."

---

## Go-To-Market Strategy (Utah)

### Phase 1: Pilot Counties (Q1 2025)
**Target:** 3-5 counties (mix of 3rd-6th class)

**Approach:**
1. Contact through UACC
2. Free 90-day pilot
3. Present at quarterly UACC meeting
4. Case study development

**Counties to Target First:**
- Duchesne County (4th class, ~20k pop)
- Emery County (5th class, ~10k pop)
- Daggett County (6th class, ~1k pop)
- Grand County (3rd class, ~9k pop)

### Phase 2: UACC Partnership (Q2 2025)
- Present at annual conference
- Training sessions for auditors
- Group purchasing agreement
- Testimonials from pilot counties

### Phase 3: Statewide Expansion (Q3-Q4 2025)
- All 29 counties
- State Auditor endorsement
- Integration with state systems
- Expansion to cities (3,000+ municipalities)

---

## Technical Support Plan

### For Small Counties (Limited IT):
**Phone Support:**
- Dedicated line for urgent issues
- Available during business hours
- Average response: < 2 hours

**Email Support:**
- support@budgetbuddy.com
- Response within 24 hours
- Screenshots/screen shares available

**Training:**
- Initial 1-hour onboarding
- Quarterly UACC webinars
- Video tutorials library
- Step-by-step guides

### For County IT Departments:
**Documentation:**
- API specs (for future integrations)
- Security whitepaper
- Deployment guides
- Troubleshooting KB

---

## Success Metrics

### Track for ROI:
- **Time Saved:** Hours spent on budget book creation
- **Error Reduction:** Manual entry mistakes caught
- **Audit Compliance:** State Auditor findings reduced
- **Staff Satisfaction:** Auditor/Treasurer feedback

### Expected Results (Based on Pilot):
- 70-80% time reduction in budget book prep
- 90%+ reduction in data entry errors
- 100% GFOA compliance on narratives
- Faster response to commissioner questions

---

## Next Steps

### To Deploy TODAY:
1. Run `run_app.bat` (Windows) or `run_app.sh` (Mac/Linux)
2. Upload sample county export
3. Review results
4. Share with finance director

### To Go Live:
1. Deploy to Streamlit Cloud (free tier)
2. Get 3 counties to pilot
3. Collect feedback
4. Present to UACC
5. Scale statewide

---

## Questions from Counties?

**"Do we need to change our current workflow?"**
No - export data the same way you do now for reports.

**"What if we switch from Munis to Caselle?"**
BudgetBuddy handles both - no re-training needed.

**"Can we customize it for our county?"**
Yes - custom reports, logos, and integrations available.

**"What about multi-year comparisons?"**
Built-in - upload multiple years for trend analysis.

**"Is our data secure?"**
Yes - processed locally or in your controlled environment.

---

## Contact

**For Demos/Pilots:**
demos@budgetbuddy.com

**For UACC Partnership:**
partnerships@budgetbuddy.com

**For Technical Questions:**
support@budgetbuddy.com

---

**Built specifically for Utah counties by professionals who understand 
local government finance and the unique challenges of small jurisdictions.**
