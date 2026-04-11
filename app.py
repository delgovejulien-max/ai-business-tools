"""
AI Business Tools SaaS - Streamlit App
Your AI Co-Founder for Strategic Thinking
Guided Onboarding - Week 1 Critical Improvement
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
from export_tools import (
    export_strategy_to_json,
    export_strategy_to_csv,
    create_strategy_summary_text,
    create_html_report,
    create_shareable_link_data
)

# Optional: Metrics tracking
try:
    from metrics_tracker import MetricsDatabase
    metrics_db = MetricsDatabase()
    METRICS_ENABLED = True
except:
    METRICS_ENABLED = False

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
    .onboarding-hero {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #1f77b4 0%, #ff6b35 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    .onboarding-hero h1 {
        margin: 0;
        font-size: 2.5rem;
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
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background: #d1e7dd;
        border-left: 4px solid #198754;
        margin-bottom: 1rem;
    }
    .tool-category-header {
        color: #1f77b4;
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .tool-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .tool-button {
        padding: 1rem;
        border-radius: 8px;
        background: #f0f2f6;
        border: 2px solid #e0e0e0;
        cursor: pointer;
        text-align: left;
        transition: all 0.3s;
    }
    .tool-button:hover {
        border-color: #1f77b4;
        background: #e7f3ff;
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
        'tools_used_this_month': 0,  # Free limit: 1 tool/month
        'free_tools_limit': 1,  # REVENUE DECISION: Limit free tier
        'onboarding_complete': False,
        'market_analysis_done': False,
        'strategy': {},
        'tools_used': [],
        'show_upgrade_prompt': False,
        'signup_date': datetime.now().isoformat(),  # TRIGGER #4: Day 7 email
        'last_visit': datetime.now().isoformat(),
    }

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'dashboard'  # 'onboarding', 'dashboard', 'tools'

def check_free_tier_limit():
    """Check if free user has hit tool limit"""
    if st.session_state.user_data['plan'] == 'free':
        if st.session_state.user_data['tools_used_this_month'] >= st.session_state.user_data['free_tools_limit']:
            return True
    return False

def days_since_signup():
    """Calculate days since user signed up (TRIGGER #4)"""
    try:
        signup = datetime.fromisoformat(st.session_state.user_data['signup_date'])
        days = (datetime.now() - signup).days
        return days
    except:
        return 0

def should_show_day7_trigger():
    """Show day 7 email reminder"""
    if st.session_state.user_data['plan'] == 'free':
        days = days_since_signup()
        return days >= 7 and days <= 10  # Show for a few days
    return False

def log_conversion(source_trigger):
    """Log conversion event for measurement"""
    if METRICS_ENABLED:
        try:
            metrics_db.log_conversion(
                user_id=st.session_state.user_data.get('company', 'unknown'),
                conversion_source=source_trigger,
                plan=st.session_state.user_data['plan'],
                revenue=29  # PRO plan cost
            )
        except:
            pass

def invoke_tool(tool_func, params):
    """Safely invoke a tool with revenue checks"""
    # Check free tier limit
    if check_free_tier_limit():
        st.markdown("""
        <div style="padding: 1.5rem; background: linear-gradient(135deg, #ff6b35 0%, #1f77b4 100%); color: white; border-radius: 8px; margin: 1rem 0;">
        <h3>You've Used Your Free Tool</h3>
        <p>Your 1 free analysis per month is complete. Unlock unlimited tools with PRO.</p>
        <p><strong>PRO Plan ($29/month)</strong></p>
        <ul>
        <li>Unlimited tool access</li>
        <li>PDF, Excel, JSON exports</li>
        <li>Shareable analysis links</li>
        <li>Team collaboration (up to 3 people)</li>
        <li>AI recommendations</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        return None

    try:
        result = tool_func.invoke(params)
        st.session_state.user_data['usage_count'] += 1
        st.session_state.user_data['tools_used_this_month'] += 1
        return result
    except Exception as e:
        st.error(f"Tool Error: {str(e)}")
        return None

def format_result(result, title="Result"):
    """Format tool result for display"""
    st.markdown(f"### {title}")

    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, (int, float)):
                st.metric(label=key.replace('_', ' ').title(), value=f"{value:,.0f}")
            elif isinstance(value, list):
                st.write(f"**{key.replace('_', ' ').title()}:**")
                for item in value[:5]:
                    st.write(f"+ {item}")
            elif isinstance(value, dict):
                with st.expander(f"[+] {key.replace('_', ' ').title()}"):
                    for k, v in list(value.items())[:5]:
                        st.write(f"**{k}:** {v}")
            else:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    else:
        st.write(result)

def show_onboarding():
    """Guided 2-minute onboarding flow"""
    st.markdown('<div class="onboarding-hero"><h1>Weeks of Strategic Planning<br>in Just 60 Seconds</h1><p>Describe your business. We analyze it instantly.</p></div>', unsafe_allow_html=True)

    st.markdown("## Tell Us About Your Startup")
    st.write("In the next 60 seconds, you'll get instant insights on your market, growth potential, and opportunities.")

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company Name", placeholder="e.g., TechFlow", key="onboard_company")
    with col2:
        founder = st.text_input("Your Name", placeholder="Your name", key="onboard_founder")

    description = st.text_area(
        "What does your startup do?",
        placeholder="e.g., We build AI-powered project management tools for remote teams",
        height=100,
        key="onboard_desc"
    )

    if st.button("Analyze My Market (60 seconds)", key="onboarding_analyze", type="primary"):
        if description.strip():
            with st.spinner("Analyzing your market..."):
                try:
                    result = invoke_tool(market_analysis, {
                        "market_name": company if company else "Your Market",
                        "product_category": description[:60],
                        "target_audience": "Founders & Teams"
                    })

                    if result:
                        st.session_state.user_data['company'] = company
                        st.session_state.user_data['name'] = founder
                        st.session_state.user_data['description'] = description
                        st.session_state.user_data['market_analysis_done'] = True
                        st.session_state.user_data['strategy'] = result
                        st.session_state.user_data['onboarding_complete'] = True
                        st.session_state.view_mode = 'dashboard'

                        st.markdown('<div class="success-box">✓ Market analysis complete! Your strategy dashboard is ready.</div>', unsafe_allow_html=True)
                        st.rerun()
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
        else:
            st.warning("Please describe your business to continue")

def show_dashboard():
    """Your Strategy persistent dashboard"""
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"# {st.session_state.user_data.get('company', 'Your Company')}")
        st.markdown(f"*{st.session_state.user_data.get('description', '')}*")

    with col2:
        plan_badge = st.session_state.user_data['plan'].upper()
        badge_color = "#ff6b35" if plan_badge == "FREE" else "#1f77b4"
        st.markdown(f"<span style='color: {badge_color};'>### Plan: {plan_badge}</span>", unsafe_allow_html=True)

    with col3:
        tools_used = st.session_state.user_data['usage_count']
        free_limit = 1 if st.session_state.user_data['plan'] == 'free' else 999
        st.markdown(f"### Tools This Month: `{tools_used}/{free_limit}`")

    st.divider()

    # Strategy Summary - Key Metrics
    st.markdown("## Your Market Analysis")

    strategy = st.session_state.user_data.get('strategy', {})
    metrics_cols = st.columns(4)

    if 'tam' in strategy:
        with metrics_cols[0]:
            tam_val = strategy['tam']
            tam_display = f"${tam_val:,.0f}M" if isinstance(tam_val, (int, float)) else str(tam_val)
            st.metric("Market Size (TAM)", tam_display)

    if 'growth_rate' in strategy:
        with metrics_cols[1]:
            growth = strategy['growth_rate']
            growth_display = f"{growth}%" if isinstance(growth, str) else f"{growth:.0f}%"
            st.metric("Annual Growth", growth_display)

    if 'market_segments' in strategy:
        with metrics_cols[2]:
            segments = strategy.get('market_segments', [])
            segment_count = len(segments) if isinstance(segments, list) else 1
            st.metric("Market Segments", segment_count)

    if 'investment_needed' in strategy:
        with metrics_cols[3]:
            inv = strategy['investment_needed']
            inv_display = f"${inv:,.0f}M" if isinstance(inv, (int, float)) else str(inv)
            st.metric("Funding Needed", inv_display)

    # UPGRADE TRIGGER #2: Team Invite (after strategy)
    if st.session_state.user_data['plan'] == 'free' and st.session_state.user_data['market_analysis_done']:
        st.markdown("""
        <div style="padding: 1.5rem; background: #f0f2f6; border-left: 4px solid #ff6b35; border-radius: 8px; margin: 1.5rem 0;">
        <h3>Invite Your Co-Founder</h3>
        <p>Share this analysis with your team and review together.</p>
        <p><strong>Unlock with PRO:</strong> Invite up to 3 co-founders, real-time collaboration, comments</p>
        </div>
        """, unsafe_allow_html=True)

        col_team1, col_team2 = st.columns(2)
        with col_team1:
            if st.button("Upgrade to PRO (7-day free trial)", key="upgrade_team_trigger", type="primary"):
                st.session_state.user_data['plan'] = 'pro'
                st.session_state.user_data['tools_used_this_month'] = 0
                log_conversion("team_invite_trigger")
                st.success("PRO Trial activated! You can now invite co-founders.")
                st.rerun()

    # Quick Actions
    st.markdown("## Next Steps")
    st.write("Complete your strategy in 5 minutes with these recommended tools:")

    action_cols = st.columns(3)

    with action_cols[0]:
        if st.button("Analyze Competitors", key="btn_competitors"):
            st.session_state.view_mode = 'tools'
            st.session_state.selected_tool = 'Competitive Analysis'
            st.rerun()

    with action_cols[1]:
        if st.button("Define Pricing", key="btn_pricing"):
            st.session_state.view_mode = 'tools'
            st.session_state.selected_tool = 'Pricing Strategy'
            st.rerun()

    with action_cols[2]:
        if st.button("Plan Launch", key="btn_launch"):
            st.session_state.view_mode = 'tools'
            st.session_state.selected_tool = 'Go-to-Market Strategy'
            st.rerun()

    st.divider()

    # UPGRADE TRIGGER #4: Day 7 Email (Reminder)
    if should_show_day7_trigger():
        st.markdown("""
        <div style="padding: 1.5rem; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 8px; margin-bottom: 1rem;">
        <h3>Ready to Go Further?</h3>
        <p>You've explored your market. Now it's time to build your complete strategy.</p>
        <p><strong>PRO gives you:</strong> All tools, exports, team collaboration, and AI recommendations</p>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Special offer: Try PRO free for 7 days, then $29/month</p>
        </div>
        """, unsafe_allow_html=True)

    # UPGRADE TRIGGER #1: Export Features
    if st.session_state.user_data['plan'] == 'free':
        st.markdown("""
        <div style="padding: 1.5rem; background: linear-gradient(135deg, #1f77b4 0%, #ff6b35 100%); color: white; border-radius: 8px; margin-bottom: 1rem;">
        <h3>Upgrade to PRO - $29/month</h3>
        <p><strong>Get PDF, Excel, and share links for your strategy</strong></p>
        <p>Share with investors, team, and co-founders. Export in any format.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start PRO Free Trial (7 days)", key="upgrade_export_trigger", type="primary"):
            st.session_state.user_data['plan'] = 'pro'
            st.session_state.user_data['tools_used_this_month'] = 0
            log_conversion("export_feature_trigger")
            st.success("PRO Trial activated! You now have access to all export features.")
            st.rerun()
    else:
        # PRO/TEAM/ENTERPRISE - Show exports
        st.markdown("## Export Your Strategy")
        st.write("Share your analysis with investors, team, or keep for your records:")

        export_cols = st.columns(4)

        with export_cols[0]:
            if st.button("Export as PDF", key="export_pdf"):
                html_report = create_html_report(
                    st.session_state.user_data.get('company', 'Strategy'),
                    st.session_state.user_data.get('description', ''),
                    st.session_state.user_data.get('name', ''),
                    st.session_state.user_data.get('strategy', {})
                )
                st.download_button(
                    label="Download PDF",
                    data=html_report,
                    file_name=f"{st.session_state.user_data.get('company', 'strategy')}_analysis.html",
                    mime="text/html"
                )

        with export_cols[1]:
            if st.button("Export as JSON", key="export_json"):
                json_data = export_strategy_to_json(
                    st.session_state.user_data.get('strategy', {}),
                    st.session_state.user_data.get('company', '')
                )
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"{st.session_state.user_data.get('company', 'strategy')}_analysis.json",
                    mime="application/json"
                )

        with export_cols[2]:
            if st.button("Export as CSV", key="export_csv"):
                csv_data = export_strategy_to_csv(
                    st.session_state.user_data.get('strategy', {}),
                    st.session_state.user_data.get('company', '')
                )
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"{st.session_state.user_data.get('company', 'strategy')}_analysis.csv",
                    mime="text/csv"
                )

        with export_cols[3]:
            if st.button("Get Share Link", key="share_link"):
                share_data = create_shareable_link_data(
                    st.session_state.user_data.get('company', ''),
                    st.session_state.user_data.get('strategy', {})
                )
                st.success(f"Share ID: `{share_data['share_id']}`")
                st.write("Share this ID with others to show your analysis")

    st.divider()

    # Insights from analysis
    if 'opportunities' in strategy or 'market_segments' in strategy:
        st.markdown("## Market Opportunities")

        insights_cols = st.columns(3)

        with insights_cols[0]:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.write("**Top Opportunities**")
            opps = strategy.get('opportunities', [])
            if isinstance(opps, list):
                for opp in opps[:2]:
                    st.write(f"+ {opp}")
            st.markdown('</div>', unsafe_allow_html=True)

        with insights_cols[1]:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.write("**Market Segments**")
            segs = strategy.get('market_segments', [])
            if isinstance(segs, list):
                for seg in segs[:2]:
                    st.write(f"+ {seg}")
            st.markdown('</div>', unsafe_allow_html=True)

        with insights_cols[2]:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.write("**Key Challenges**")
            st.write("+ Building market awareness")
            st.write("+ Establishing product-market fit")
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # View all tools
    if st.button("View All 18 Tools", key="btn_all_tools"):
        st.session_state.view_mode = 'tools'
        st.rerun()

def show_tools():
    """All 18 tools organized by category"""
    st.markdown("## All Tools")
    st.write("Explore all 18 tools to build your complete strategy")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back to Dashboard"):
            st.session_state.view_mode = 'dashboard'
            st.rerun()

    st.divider()

    # CONSULTING TOOLS
    st.markdown("### Consulting Tools")
    st.write("Strategy & planning for your business")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Market Analysis",
        "Competitive Analysis",
        "Business Model",
        "Go-to-Market",
        "Pricing",
        "Funding"
    ])

    # Market Analysis
    with tab1:
        st.subheader("Market Analysis")
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
    with tab2:
        st.subheader("Competitive Analysis")
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
    with tab3:
        st.subheader("Business Model Canvas")
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

    # Go-to-Market
    with tab4:
        st.subheader("Go-to-Market Strategy")
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
    with tab5:
        st.subheader("Pricing Strategy")
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
    with tab6:
        st.subheader("Funding Strategy")
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

    st.divider()

    # MARKETING TOOLS
    st.markdown("### Marketing Tools")
    st.write("Campaigns, audience insights, and growth strategies")

    tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
        "Campaign Plan",
        "Audience",
        "Budget",
        "Content",
        "Social Media",
        "CRO"
    ])

    # Campaign Plan
    with tab7:
        st.subheader("Campaign Plan")
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
    with tab8:
        st.subheader("Audience Analysis")
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
    with tab9:
        st.subheader("Budget Optimizer")
        total_budget = st.number_input("Total Budget ($)", min_value=1000, value=50000)
        focus = st.selectbox("Marketing Focus", ["awareness", "conversion", "retention"])

        if st.button("Optimize Budget"):
            with st.spinner("Optimizing budget allocation..."):
                result = invoke_tool(budget_optimizer, {
                    "total_budget": float(total_budget),
                    "focus_area": focus
                })
                if result:
                    st.markdown('<div class="success-box">✓ Budget Plan Created</div>', unsafe_allow_html=True)
                    format_result(result, "Budget Allocation")

    # Content Calendar
    with tab10:
        st.subheader("Content Calendar")
        topic = st.text_input("Content Topic", "AI for Startups")
        platforms = st.multiselect("Platforms", ["Twitter", "LinkedIn", "Blog", "YouTube"], default=["Twitter"])

        if st.button("Create Content Plan"):
            with st.spinner("Creating 90-day content calendar..."):
                result = invoke_tool(content_calendar, {
                    "content_topic": topic,
                    "platforms": platforms
                })
                if result:
                    st.markdown('<div class="success-box">✓ Content Calendar Created</div>', unsafe_allow_html=True)
                    format_result(result, "90-Day Content Calendar")

    # Social Media Strategy
    with tab11:
        st.subheader("Social Media Strategy")
        platform = st.selectbox("Primary Platform", ["Twitter", "LinkedIn", "Facebook", "Instagram"])
        goal = st.text_input("Goal", "Increase brand awareness among founders")

        if st.button("Create Social Strategy"):
            with st.spinner("Creating social media strategy..."):
                result = invoke_tool(social_media_strategy, {
                    "platform": platform,
                    "goal": goal
                })
                if result:
                    st.markdown('<div class="success-box">✓ Strategy Created</div>', unsafe_allow_html=True)
                    format_result(result, "Social Media Strategy")

    # Conversion Optimization
    with tab12:
        st.subheader("Conversion Optimization")
        current_rate = st.number_input("Current Conversion Rate (%)", min_value=0.1, value=2.0, step=0.1)
        traffic = st.number_input("Monthly Traffic", min_value=100, value=10000)

        if st.button("Create CRO Plan"):
            with st.spinner("Creating optimization roadmap..."):
                result = invoke_tool(conversion_optimization, {
                    "current_rate": float(current_rate),
                    "monthly_traffic": int(traffic)
                })
                if result:
                    st.markdown('<div class="success-box">✓ CRO Roadmap Created</div>', unsafe_allow_html=True)
                    format_result(result, "Conversion Optimization Plan")

    st.divider()

    # ANALYTICS TOOLS
    st.markdown("### Analytics Tools")
    st.write("Data insights and performance metrics")

    tab13, tab14, tab15, tab16, tab17, tab18 = st.tabs([
        "Revenue Forecast",
        "Churn",
        "KPI",
        "Segmentation",
        "Performance",
        "Cohort"
    ])

    # Revenue Forecast
    with tab13:
        st.subheader("Revenue Forecast")
        current_revenue = st.number_input("Current MRR ($)", min_value=0, value=10000)
        growth_rate = st.number_input("Monthly Growth (%)", min_value=0.0, value=10.0, step=0.5)

        if st.button("Forecast Revenue"):
            with st.spinner("Generating 12-month forecast..."):
                result = invoke_tool(revenue_forecast, {
                    "current_mrr": float(current_revenue),
                    "monthly_growth_rate": float(growth_rate)
                })
                if result:
                    st.markdown('<div class="success-box">✓ Forecast Complete</div>', unsafe_allow_html=True)
                    format_result(result, "12-Month Revenue Forecast")

    # Churn Analysis
    with tab14:
        st.subheader("Churn Analysis")
        customers = st.number_input("Total Customers", min_value=10, value=100)
        churn_rate = st.number_input("Monthly Churn Rate (%)", min_value=0.0, value=5.0, step=0.5)

        if st.button("Analyze Churn"):
            with st.spinner("Analyzing churn patterns..."):
                result = invoke_tool(churn_analysis, {
                    "total_customers": int(customers),
                    "monthly_churn_rate": float(churn_rate)
                })
                if result:
                    st.markdown('<div class="success-box">✓ Analysis Complete</div>', unsafe_allow_html=True)
                    format_result(result, "Churn Analysis")

    # KPI Dashboard
    with tab15:
        st.subheader("KPI Dashboard")
        business_type = st.selectbox("Business Type", ["SaaS", "E-commerce", "Marketplace", "Creator"])

        if st.button("Generate KPI Dashboard"):
            with st.spinner("Generating KPI dashboard..."):
                result = invoke_tool(kpi_dashboard, {
                    "business_type": business_type
                })
                if result:
                    st.markdown('<div class="success-box">✓ Dashboard Generated</div>', unsafe_allow_html=True)
                    format_result(result, "KPI Dashboard")

    # Customer Segmentation
    with tab16:
        st.subheader("Customer Segmentation")
        total_customers = st.number_input("Total Customers", min_value=10, value=500)
        avg_customer_value = st.number_input("Avg Customer Value ($)", min_value=100, value=5000)

        if st.button("Segment Customers"):
            with st.spinner("Segmenting customer base..."):
                result = invoke_tool(customer_segmentation, {
                    "total_customers": int(total_customers),
                    "average_customer_value": float(avg_customer_value)
                })
                if result:
                    st.markdown('<div class="success-box">✓ Segmentation Complete</div>', unsafe_allow_html=True)
                    format_result(result, "Customer Segments")

    # Performance Report
    with tab17:
        st.subheader("Performance Report")
        metric_type = st.selectbox("Report Type", ["Monthly", "Quarterly", "Annual"])

        if st.button("Generate Report"):
            with st.spinner("Generating performance report..."):
                result = invoke_tool(performance_report, {
                    "report_type": metric_type
                })
                if result:
                    st.markdown('<div class="success-box">✓ Report Generated</div>', unsafe_allow_html=True)
                    format_result(result, "Performance Report")

    # Cohort Analysis
    with tab18:
        st.subheader("Cohort Analysis")
        cohort_period = st.selectbox("Cohort Period", ["Weekly", "Monthly", "Quarterly"])

        if st.button("Analyze Cohorts"):
            with st.spinner("Analyzing cohort retention..."):
                result = invoke_tool(cohort_analysis, {
                    "cohort_period": cohort_period
                })
                if result:
                    st.markdown('<div class="success-box">✓ Analysis Complete</div>', unsafe_allow_html=True)
                    format_result(result, "Cohort Analysis")

# Sidebar
with st.sidebar:
    st.markdown("## Settings")

    if st.session_state.user_data['onboarding_complete']:
        st.markdown(f"### {st.session_state.user_data.get('company', 'Company')}")
        if st.session_state.user_data.get('name'):
            st.markdown(f"**Founder:** {st.session_state.user_data['name']}")
        st.markdown(f"**Plan:** {st.session_state.user_data['plan'].upper()}")
        st.markdown(f"**Tools Used:** {st.session_state.user_data['usage_count']}")

        st.divider()

        # EXPANSION REVENUE: PRO to TEAM upgrade
        if st.session_state.user_data['plan'] == 'pro':
            st.markdown("### Upgrade to TEAM")
            st.write("Invite your whole team and collaborate in real-time.")
            st.markdown("- 10 team members")
            st.markdown("- Real-time collaboration")
            st.markdown("- **$99/month**")
            if st.button("Learn about TEAM Plan", key="team_expansion"):
                st.info("TEAM plan coming soon! Invite up to 10 team members, real-time collaboration, and team dashboards.")

        if st.button("Reset & Start Over"):
            st.session_state.user_data['onboarding_complete'] = False
            st.session_state.user_data['market_analysis_done'] = False
            st.session_state.view_mode = 'onboarding'
            st.rerun()

    st.divider()

    st.markdown("### Pricing")
    st.markdown("**FREE** - 1 tool/month")
    st.markdown("**PRO** - $29/month (unlimited tools)")
    st.markdown("**TEAM** - $99/month (10 people)")
    st.markdown("**ENTERPRISE** - Custom pricing")

    st.divider()

    st.markdown("### About")
    st.write("**AI Business Tools** - Your AI co-founder for strategic thinking. 18 tools across Consulting, Marketing & Analytics.")

    st.divider()

    st.markdown("### Support")
    st.write("Email: support@aibusinesstools.com")

# Main content routing
if not st.session_state.user_data['onboarding_complete']:
    show_onboarding()
elif st.session_state.view_mode == 'tools':
    show_tools()
else:
    show_dashboard()
