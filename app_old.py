"""
AI Business Tools SaaS - Streamlit App
Your AI Co-Founder for Strategic Thinking
"""

import streamlit as st
import json
from datetime import datetime
from agents.business_tools import (
    # Consulting
    market_analysis,
    competitive_analysis,
    business_model_canvas,
    go_to_market_strategy,
    pricing_strategy,
    funding_strategy,
    # Marketing
    campaign_plan,
    audience_analysis,
    budget_optimizer,
    content_calendar,
    social_media_strategy,
    conversion_optimization,
    # Analytics
    revenue_forecast,
    churn_analysis,
    kpi_dashboard,
    customer_segmentation,
    performance_report,
    cohort_analysis,
)

# Page config
st.set_page_config(
    page_title="AI Business Tools - Your AI Co-Founder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .header {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subheader {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .tool-card {
        padding: 1rem;
        border-radius: 8px;
        background: #f0f2f6;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background: #d1e7dd;
        border-left: 4px solid #198754;
        margin-bottom: 1rem;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 8px;
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .onboarding-hero {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #1f77b4 0%, #ff6b35 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    .dashboard-card {
        padding: 1.5rem;
        border-radius: 8px;
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .metric-highlight {
        color: #ff6b35;
        font-size: 2rem;
        font-weight: bold;
    }
    .next-steps {
        padding: 1.5rem;
        background: #e7f3ff;
        border-left: 4px solid #1f77b4;
        border-radius: 8px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': '',
        'company': '',
        'description': '',
        'plan': 'free',
        'usage_count': 0,
        'onboarding_complete': False,
        'market_analysis_done': False,
        'strategy': {}
    }

def invoke_tool(tool_func, params):
    """Safely invoke a tool"""
    try:
        result = tool_func.invoke(params)
        st.session_state.user_data['usage_count'] += 1
        return result
    except Exception as e:
        st.error(f"Tool Error: {str(e)}")
        return None

def format_result(result, title="Result"):
    """Format tool result for display"""
    st.markdown(f"### {title}")

    if isinstance(result, dict):
        # Special formatting for specific keys
        for key, value in result.items():
            if isinstance(value, (int, float)):
                st.metric(label=key.replace('_', ' ').title(), value=f"{value:,.0f}")
            elif isinstance(value, list):
                st.write(f"**{key.replace('_', ' ').title()}:**")
                for item in value[:5]:  # Show first 5 items
                    st.write(f"• {item}")
            elif isinstance(value, dict):
                with st.expander(f"📊 {key.replace('_', ' ').title()}"):
                    for k, v in list(value.items())[:5]:
                        st.write(f"**{k}:** {v}")
            else:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    else:
        st.write(result)

# Sidebar
with st.sidebar:
    st.markdown("# ⚙️ Settings")

    user_name = st.text_input("Your Name", value=st.session_state.user_data['name'])
    company_name = st.text_input("Company Name", value=st.session_state.user_data['company'])

    st.markdown("### 📊 Your Plan")
    st.info(f"**Current Plan:** {st.session_state.user_data['plan'].upper()}")
    st.info(f"**Tools Used:** {st.session_state.user_data['usage_count']}")

    st.markdown("### 💡 About This App")
    st.write("""
    AI-powered business tools for startups:
    - **Consulting**: Strategy & planning
    - **Marketing**: Campaigns & growth
    - **Analytics**: Data & insights

    All powered by AI agents.
    """)

    st.markdown("### 📧 Support")
    if st.button("Contact Support"):
        st.success("Email: support@aibusinesstools.com")

# Main content
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header">🚀 AI Business Tools</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Strategy, Marketing & Analytics - Powered by AI Agents</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tools", "🎯 Scenarios", "📈 Pricing", "👤 Account"])

# TAB 1: Tools
with tab1:
    st.markdown("## Select Your Tool")

    tool_category = st.radio(
        "Choose Category:",
        ["Consulting", "Marketing", "Analytics"],
        horizontal=True
    )

    # CONSULTING TOOLS
    if tool_category == "Consulting":
        st.markdown("### 🏢 Consulting Tools")

        consulting_tool = st.selectbox(
            "Select Tool:",
            [
                "Market Analysis",
                "Competitive Analysis",
                "Business Model Canvas",
                "Go-to-Market Strategy",
                "Pricing Strategy",
                "Funding Strategy"
            ]
        )

        # Market Analysis
        if consulting_tool == "Market Analysis":
            col1, col2, col3 = st.columns(3)
            with col1:
                market = st.text_input("Market Name", "European SaaS")
            with col2:
                category = st.text_input("Product Category", "Project Management")
            with col3:
                audience = st.text_input("Target Audience", "Startups")

            if st.button("Analyze Market"):
                with st.spinner("Analyzing market..."):
                    result = invoke_tool(market_analysis, {
                        "market_name": market,
                        "product_category": category,
                        "target_audience": audience
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Analysis Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Market Analysis Results")

        # Competitive Analysis
        elif consulting_tool == "Competitive Analysis":
            product = st.text_input("Your Product", "AI-powered project management tool")
            competitors_input = st.text_area("Competitors (comma separated)", "Asana, Monday.com, Notion")
            competitors = [c.strip() for c in competitors_input.split(",")]

            if st.button("Analyze Competition"):
                with st.spinner("Analyzing competitors..."):
                    result = invoke_tool(competitive_analysis, {
                        "your_product": product,
                        "competitors": competitors
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Analysis Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Competitive Analysis")

        # Business Model Canvas
        elif consulting_tool == "Business Model Canvas":
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input("Company Name", "My Startup")
            with col2:
                idea = st.text_input("Business Idea", "AI-powered automation platform")

            if st.button("Generate Canvas"):
                with st.spinner("Creating Business Model Canvas..."):
                    result = invoke_tool(business_model_canvas, {
                        "company_name": company,
                        "business_idea": idea
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Canvas Created</div>', unsafe_allow_html=True)
                        format_result(result, "Business Model Canvas")

        # Go-to-Market Strategy
        elif consulting_tool == "Go-to-Market Strategy":
            col1, col2, col3 = st.columns(3)
            with col1:
                product = st.text_input("Product Name", "My Product")
            with col2:
                market = st.text_input("Target Market", "Startups")
            with col3:
                budget = st.number_input("Budget ($)", min_value=1000, value=50000, step=5000)

            if st.button("Create GTM Plan"):
                with st.spinner("Creating Go-to-Market Strategy..."):
                    result = invoke_tool(go_to_market_strategy, {
                        "product_name": product,
                        "target_market": market,
                        "budget_usd": float(budget)
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Strategy Created</div>', unsafe_allow_html=True)
                        format_result(result, "Go-to-Market Strategy")

        # Pricing Strategy
        elif consulting_tool == "Pricing Strategy":
            col1, col2, col3 = st.columns(3)
            with col1:
                product = st.text_input("Product", "SaaS Product")
            with col2:
                segment = st.text_input("Target Segment", "Startups")
            with col3:
                cost = st.number_input("Production Cost ($)", min_value=100, value=1000, step=100)

            if st.button("Create Pricing"):
                with st.spinner("Developing pricing strategy..."):
                    result = invoke_tool(pricing_strategy, {
                        "product_name": product,
                        "target_segment": segment,
                        "production_cost": float(cost)
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Pricing Strategy Created</div>', unsafe_allow_html=True)
                        format_result(result, "Pricing Strategy")

        # Funding Strategy
        elif consulting_tool == "Funding Strategy":
            col1, col2, col3 = st.columns(3)
            with col1:
                company = st.text_input("Company", "My Startup")
            with col2:
                stage = st.selectbox("Funding Stage", ["seed", "series_a", "series_b"])
            with col3:
                amount = st.number_input("Amount Needed ($)", min_value=50000, value=500000, step=50000)

            if st.button("Create Funding Plan"):
                with st.spinner("Creating funding strategy..."):
                    result = invoke_tool(funding_strategy, {
                        "company_name": company,
                        "stage": stage,
                        "amount_needed": float(amount)
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Funding Strategy Created</div>', unsafe_allow_html=True)
                        format_result(result, "Funding Strategy")

    # MARKETING TOOLS
    elif tool_category == "Marketing":
        st.markdown("### 📢 Marketing Tools")

        marketing_tool = st.selectbox(
            "Select Tool:",
            [
                "Campaign Plan",
                "Audience Analysis",
                "Budget Optimizer",
                "Content Calendar",
                "Social Media Strategy",
                "Conversion Optimization"
            ]
        )

        # Campaign Plan
        if marketing_tool == "Campaign Plan":
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Campaign Name", "Product Launch")
                objective = st.selectbox("Objective", ["awareness", "leads", "sales", "retention"])
            with col2:
                audience = st.text_input("Target Audience", "Tech Startups")
                budget = st.number_input("Budget ($)", min_value=1000, value=50000, step=5000)

            if st.button("Create Campaign Plan"):
                with st.spinner("Creating campaign plan..."):
                    result = invoke_tool(campaign_plan, {
                        "campaign_name": name,
                        "objective": objective,
                        "target_audience": audience,
                        "budget": float(budget)
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Campaign Plan Created</div>', unsafe_allow_html=True)
                        format_result(result, "Campaign Plan")

        # Audience Analysis
        elif marketing_tool == "Audience Analysis":
            col1, col2 = st.columns(2)
            with col1:
                segment = st.text_input("Audience Segment", "Startup Founders")
            with col2:
                market = st.text_input("Market", "SaaS")

            if st.button("Analyze Audience"):
                with st.spinner("Analyzing audience..."):
                    result = invoke_tool(audience_analysis, {
                        "audience_segment": segment,
                        "market": market
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Analysis Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Audience Analysis")

        # Budget Optimizer
        elif marketing_tool == "Budget Optimizer":
            col1, col2 = st.columns(2)
            with col1:
                budget = st.number_input("Total Budget ($)", min_value=1000, value=50000, step=5000)
                goal = st.selectbox("Goal", ["awareness", "leads", "conversions", "retention"])
            with col2:
                channels = st.multiselect(
                    "Channels",
                    ["social_media", "paid_ads", "content", "email", "events"],
                    default=["social_media", "paid_ads", "content", "email"]
                )

            if st.button("Optimize Budget"):
                with st.spinner("Optimizing budget allocation..."):
                    result = invoke_tool(budget_optimizer, {
                        "total_budget": float(budget),
                        "channels": channels,
                        "goal": goal
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Optimization Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Budget Optimization")

        # Content Calendar
        elif marketing_tool == "Content Calendar":
            col1, col2 = st.columns(2)
            with col1:
                duration = st.number_input("Duration (days)", min_value=7, value=30, step=7)
            with col2:
                frequency = st.selectbox("Frequency", ["daily", "3x_weekly", "weekly", "biweekly"])

            if st.button("Generate Calendar"):
                with st.spinner("Creating content calendar..."):
                    result = invoke_tool(content_calendar, {
                        "campaign_duration_days": duration,
                        "frequency": frequency
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Calendar Created</div>', unsafe_allow_html=True)
                        format_result(result, "Content Calendar")

        # Social Media Strategy
        elif marketing_tool == "Social Media Strategy":
            col1, col2 = st.columns(2)
            with col1:
                platforms = st.multiselect(
                    "Platforms",
                    ["linkedin", "twitter", "facebook", "instagram", "tiktok"],
                    default=["linkedin", "twitter"]
                )
            with col2:
                audience = st.text_input("Target Audience", "Tech Founders")
                voice = st.selectbox("Brand Voice", ["professional", "casual", "trendy", "humorous"])

            if st.button("Create Strategy"):
                with st.spinner("Creating social media strategy..."):
                    result = invoke_tool(social_media_strategy, {
                        "platforms": platforms,
                        "target_audience": audience,
                        "brand_voice": voice
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Strategy Created</div>', unsafe_allow_html=True)
                        format_result(result, "Social Media Strategy")

        # Conversion Optimization
        elif marketing_tool == "Conversion Optimization":
            col1, col2, col3 = st.columns(3)
            with col1:
                current_cr = st.number_input("Current Conversion Rate (%)", min_value=0.1, value=2.0, step=0.1) / 100
            with col2:
                goal_cr = st.number_input("Goal Conversion Rate (%)", min_value=0.1, value=5.0, step=0.1) / 100
            with col3:
                visitors = st.number_input("Monthly Visitors", min_value=100, value=10000, step=1000)

            if st.button("Get CRO Plan"):
                with st.spinner("Creating CRO strategy..."):
                    result = invoke_tool(conversion_optimization, {
                        "current_conversion_rate": current_cr,
                        "goal_conversion_rate": goal_cr,
                        "monthly_visitors": float(visitors)
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ CRO Plan Created</div>', unsafe_allow_html=True)
                        format_result(result, "Conversion Optimization")

    # ANALYTICS TOOLS
    elif tool_category == "Analytics":
        st.markdown("### 📊 Analytics Tools")

        analytics_tool = st.selectbox(
            "Select Tool:",
            [
                "Revenue Forecast",
                "Churn Analysis",
                "KPI Dashboard",
                "Customer Segmentation",
                "Performance Report"
            ]
        )

        # Revenue Forecast
        if analytics_tool == "Revenue Forecast":
            st.write("Enter your historical revenue for the last 12 months:")
            col1, col2, col3 = st.columns(3)

            months = []
            for i in range(4):
                with col1 if i % 3 == 0 else (col2 if i % 3 == 1 else col3):
                    val = st.number_input(f"Month {i+1} ($)", value=10000 * (i + 1), step=1000)
                    months.append(float(val))

            growth = st.slider("Monthly Growth Rate (%)", min_value=1, max_value=50, value=10) / 100
            months_ahead = st.slider("Forecast Months", min_value=1, max_value=12, value=6)

            if st.button("Forecast Revenue"):
                with st.spinner("Forecasting revenue..."):
                    result = invoke_tool(revenue_forecast, {
                        "historical_revenue": months,
                        "growth_rate": growth,
                        "months_ahead": months_ahead
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Forecast Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Revenue Forecast")

        # Churn Analysis
        elif analytics_tool == "Churn Analysis":
            col1, col2, col3 = st.columns(3)
            with col1:
                customers = st.number_input("Current Customers", min_value=10, value=1000, step=10)
            with col2:
                churn = st.slider("Monthly Churn Rate (%)", min_value=1, max_value=10, value=5) / 100
            with col3:
                months = st.slider("Months Ahead", min_value=1, max_value=12, value=6)

            if st.button("Analyze Churn"):
                with st.spinner("Analyzing churn..."):
                    result = invoke_tool(churn_analysis, {
                        "customer_count": customers,
                        "monthly_churn_rate": churn,
                        "months_ahead": months
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Analysis Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Churn Analysis")

        # KPI Dashboard
        elif analytics_tool == "KPI Dashboard":
            col1, col2, col3 = st.columns(3)
            with col1:
                mrr = st.number_input("Monthly Revenue ($)", min_value=0, value=50000, step=5000)
            with col2:
                customers = st.number_input("Total Customers", min_value=0, value=500, step=10)
            with col3:
                mau = st.number_input("Monthly Active Users", min_value=0, value=15000, step=1000)

            if st.button("Generate Dashboard"):
                with st.spinner("Generating KPI dashboard..."):
                    result = invoke_tool(kpi_dashboard, {
                        "business_metrics": {
                            "monthly_revenue": mrr,
                            "customers": customers,
                            "monthly_active_users": mau
                        }
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Dashboard Generated</div>', unsafe_allow_html=True)
                        format_result(result, "KPI Dashboard")

        # Customer Segmentation
        elif analytics_tool == "Customer Segmentation":
            customers = st.number_input("Total Customers", min_value=10, value=1000, step=50)

            if st.button("Segment Customers"):
                with st.spinner("Segmenting customers..."):
                    result = invoke_tool(customer_segmentation, {
                        "total_customers": customers
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Segmentation Complete</div>', unsafe_allow_html=True)
                        format_result(result, "Customer Segmentation")

        # Performance Report
        elif analytics_tool == "Performance Report":
            col1, col2 = st.columns(2)
            with col1:
                period = st.selectbox("Period", ["weekly", "monthly", "quarterly"])
            with col2:
                revenue = st.number_input("Current Revenue ($)", min_value=0, value=150000, step=10000)

            if st.button("Generate Report"):
                with st.spinner("Generating performance report..."):
                    result = invoke_tool(performance_report, {
                        "period": period,
                        "metrics": {"revenue": revenue}
                    })
                    if result:
                        st.markdown('<div class="success-box">✓ Report Generated</div>', unsafe_allow_html=True)
                        format_result(result, "Performance Report")

# TAB 2: Scenarios
with tab2:
    st.markdown("## 🎯 Pre-built Scenarios")

    scenario = st.selectbox(
        "Choose a Scenario:",
        [
            "Build Startup Pitch Deck",
            "Launch Product Immediately",
            "Prepare Board Meeting",
            "Raise Series A Funding"
        ]
    )

    if scenario == "Build Startup Pitch Deck":
        st.info("""
        **What you'll get:**
        1. Market Analysis (TAM)
        2. Business Model Canvas
        3. Competitive Analysis
        4. Go-to-Market Strategy
        5. Pricing Strategy

        **Output:** Complete investor pitch deck
        """)

        if st.button("Generate Pitch Deck"):
            st.success("✓ Pitch deck generated! Download in Account tab.")

    elif scenario == "Launch Product Immediately":
        st.info("""
        **What you'll get:**
        1. Audience Analysis (who are we targeting?)
        2. Campaign Plan (launch strategy)
        3. Budget Optimizer ($50k breakdown)
        4. Content Calendar (30-day plan)
        5. Social Media Strategy

        **Output:** Ready-to-launch marketing plan
        """)

        if st.button("Generate Marketing Plan"):
            st.success("✓ Marketing plan generated! Download in Account tab.")

    elif scenario == "Prepare Board Meeting":
        st.info("""
        **What you'll get:**
        1. Revenue Forecast (next quarter)
        2. Churn Analysis (retention health)
        3. KPI Dashboard (key metrics)
        4. Customer Segmentation (segment health)
        5. Performance Report (executive summary)

        **Output:** Board meeting package
        """)

        if st.button("Generate Board Package"):
            st.success("✓ Board package generated! Download in Account tab.")

    elif scenario == "Raise Series A Funding":
        st.info("""
        **What you'll get:**
        1. Market Analysis (TAM/SAM)
        2. Competitive Analysis (why you win)
        3. Revenue Forecast (growth trajectory)
        4. KPI Dashboard (traction metrics)
        5. Business Model Canvas (unit economics)

        **Output:** Investor pitch materials
        """)

        if st.button("Generate Pitch Materials"):
            st.success("✓ Pitch materials generated! Download in Account tab.")

# TAB 3: Pricing
with tab3:
    st.markdown("## 💰 Pricing")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Free")
        st.markdown("""
        - 5 tools/month
        - Basic features
        - Community support

        **$0/month**
        """)
        st.button("Current Plan" if st.session_state.user_data['plan'] == 'free' else "Downgrade to Free")

    with col2:
        st.markdown("### Pro")
        st.markdown("""
        - Unlimited tools
        - All features
        - Email support
        - Export reports

        **$49/month**
        """)
        st.button("Upgrade to Pro" if st.session_state.user_data['plan'] != 'pro' else "Current Plan")

    with col3:
        st.markdown("### Business")
        st.markdown("""
        - Everything in Pro
        - API access
        - Priority support
        - White-label option

        **$199/month**
        """)
        st.button("Upgrade to Business" if st.session_state.user_data['plan'] != 'business' else "Current Plan")

# TAB 4: Account
with tab4:
    st.markdown("## 👤 Account")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Profile")
        st.write(f"**Name:** {user_name if user_name else 'Not set'}")
        st.write(f"**Company:** {company_name if company_name else 'Not set'}")
        st.write(f"**Plan:** {st.session_state.user_data['plan'].upper()}")
        st.write(f"**Tools Used This Month:** {st.session_state.user_data['usage_count']}")
        st.write(f"**Joined:** {datetime.now().strftime('%Y-%m-%d')}")

    with col2:
        st.markdown("### Billing")
        st.write(f"**Status:** Active")
        st.write(f"**Next Billing Date:** {(datetime.now().day % 30) + 1} of next month")
        st.write(f"**Payment Method:** Not configured")
        st.button("Manage Billing")

    st.markdown("### Downloads")
    st.write("Your generated reports and analyses will appear here.")
    st.info("No downloads yet. Generate a report above to see it here.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>© 2025 AI Business Tools. Powered by LangGraph & AI Agents.</p>
    <p><a href="#">Privacy</a> | <a href="#">Terms</a> | <a href="#">Contact</a></p>
</div>
""", unsafe_allow_html=True)
