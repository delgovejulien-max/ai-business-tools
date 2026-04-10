#!/usr/bin/env python
"""
Test Business Tools
Demonstrate consulting, marketing, and BI tools for your CEO agent
"""
from agents.business_tools import (
    # Consulting
    market_analysis,
    competitive_analysis,
    business_model_canvas,
    go_to_market_strategy,
    pricing_strategy,
    # Marketing
    campaign_plan,
    audience_analysis,
    budget_optimizer,
    content_calendar,
    # Analytics
    revenue_forecast,
    churn_analysis,
    kpi_dashboard,
    customer_segmentation,
    performance_report,
)
import json


def print_section(title):
    """Pretty print section"""
    print(f"\n{'=' * 80}")
    print(f"{title.center(80)}")
    print(f"{'=' * 80}\n")


def test_consulting_tools():
    """Test consulting-specific tools"""
    print_section("CONSULTING TOOLS DEMONSTRATION")

    # Test 1: Market Analysis
    print("[TOOL 1] Market Analysis")
    print("-" * 80)
    result = market_analysis("European SaaS", "project management", "Startups")
    print(f"Market: {result['market']}")
    print(f"Market Size: {result['market_size']}")
    print(f"Growth Rate: {result['growth_rate']}")
    print(f"Key Opportunities:")
    for opp in result['opportunities'][:2]:
        print(f"  - {opp}")
    print(f"Investment Needed: {result['investment_needed']}")
    print(f"Time to Market: {result['time_to_market']}")
    print()

    # Test 2: Competitive Analysis
    print("[TOOL 2] Competitive Analysis")
    print("-" * 80)
    result = competitive_analysis(
        "AI-powered project management tool",
        ["Asana", "Monday.com", "Notion"]
    )
    print(f"Your Product: {result['your_product']}")
    print(f"Competitors: {result['competitors_analyzed']}")
    print(f"Your Advantages:")
    for adv in result['your_advantages'][:3]:
        print(f"  + {adv}")
    print(f"Recommended Positioning: {result['recommended_positioning']}")
    print()

    # Test 3: Business Model Canvas
    print("[TOOL 3] Business Model Canvas")
    print("-" * 80)
    result = business_model_canvas("TechFlow AI", "AI-powered workflow automation")
    canvas = result['canvas']
    print(f"Company: {result['company']}")
    print(f"Value Props: {', '.join(canvas['value_propositions'][:2])}")
    print(f"Revenue Model: {', '.join(result['canvas']['revenue_streams'][:2])}")
    print(f"Year 1 Revenue Projection: {result['financial_projections']['year_1_revenue']}")
    print()

    # Test 4: Go-to-Market Strategy
    print("[TOOL 4] Go-to-Market Strategy")
    print("-" * 80)
    result = go_to_market_strategy("TechFlow", "Startups", 50000)
    print(f"Product: {result['product']}")
    print(f"Target Market: {result['target_market']}")
    print(f"Budget: ${result['budget']:,.0f}")
    print(f"Channels:")
    for channel, data in list(result['channels'].items())[:3]:
        print(f"  - {channel}: ${data['budget_allocation']:,.0f}")
    print()

    # Test 5: Pricing Strategy
    print("[TOOL 5] Pricing Strategy")
    print("-" * 80)
    result = pricing_strategy("TechFlow", "Startups", 1000)
    print(f"Product: {result['product']}")
    print(f"Production Cost: ${result['production_cost']:,.0f}")
    pricing = result['recommended_pricing']
    for tier, info in pricing.items():
        print(f"\n  {tier.upper()}:")
        print(f"    Price: {info['price']}")
        print(f"    Margin: {info['margin']}")
        print(f"    Target: {info['target_customers']}")
    print()


def test_marketing_tools():
    """Test marketing-specific tools"""
    print_section("MARKETING TOOLS DEMONSTRATION")

    # Test 1: Campaign Plan
    print("[TOOL 1] Campaign Plan")
    print("-" * 80)
    result = campaign_plan("Product Launch", "awareness", "Tech startups", 50000)
    print(f"Campaign: {result['campaign_name']}")
    print(f"Objective: {result['objective']}")
    print(f"Budget: ${result['budget']:,.0f}")
    print(f"Duration: {result['duration_days']} days")
    print(f"Target KPIs:")
    for kpi, value in list(result['target_kpis'].items())[:3]:
        print(f"  - {kpi}: {value}")
    print()

    # Test 2: Audience Analysis
    print("[TOOL 2] Audience Analysis")
    print("-" * 80)
    result = audience_analysis("Startup Founders", "SaaS")
    persona = result['persona']
    print(f"Segment: {result['segment']}")
    print(f"Persona: {persona['name']} - {persona['title']}")
    print(f"Income: {persona['income']}")
    print(f"Top Pain Points:")
    for pain in result['pain_points'][:3]:
        print(f"  - {pain}")
    print(f"Preferred Channels: {', '.join(result['content_preferences']['channels'][:3])}")
    print()

    # Test 3: Budget Optimizer
    print("[TOOL 3] Budget Optimizer")
    print("-" * 80)
    channels = ["social_media", "paid_ads", "content", "email"]
    result = budget_optimizer(50000, channels, "leads")
    print(f"Total Budget: ${result['total_budget']:,.0f}")
    print(f"Goal: {result['goal']}")
    print(f"Budget Allocation:")
    for channel, data in result['allocation'].items():
        amount = data['amount']
        pct = data['percentage']
        print(f"  - {channel}: ${amount:,.0f} ({pct:.1f}%)")
    print()

    # Test 4: Content Calendar
    print("[TOOL 4] Content Calendar")
    print("-" * 80)
    result = content_calendar(30, "weekly")
    print(f"Campaign Duration: {result['duration_days']} days")
    print(f"Posting Frequency: {result['frequency']}")
    print(f"Total Posts: {result['total_posts']}")
    print(f"Content Types: {', '.join(result['content_types'][:4])}")
    print(f"Best Posting Days: {', '.join(result['posting_schedule']['best_days'])}")
    print()


def test_analytics_tools():
    """Test BI/Analytics tools"""
    print_section("ANALYTICS & BI TOOLS DEMONSTRATION")

    # Test 1: Revenue Forecast
    print("[TOOL 1] Revenue Forecast")
    print("-" * 80)
    historical = [10000, 12000, 14000, 15000, 17000, 19000, 21000, 23000, 25000, 27000, 29000, 31000]
    result = revenue_forecast(historical, 0.10, 6)
    print(f"Historical Avg: ${result['historical_avg']:,.0f}")
    print(f"Growth Rate: {result['growth_rate']}")
    print(f"6-Month Forecast:")
    for forecast in result['forecast'][:3]:
        print(f"  Month {forecast['month']}: ${forecast['revenue']:,.0f}")
    print(f"Total Forecast: ${result['total_forecast_revenue']:,.0f}")
    print()

    # Test 2: Churn Analysis
    print("[TOOL 2] Churn Analysis")
    print("-" * 80)
    result = churn_analysis(1000, 0.05, 6)
    print(f"Starting Customers: {result['starting_customers']}")
    print(f"Monthly Churn Rate: {result['monthly_churn_rate']}")
    print(f"Customers in 6 Months: {result['retained_customers_at_end']}")
    print(f"Total Churn: {result['total_churn_customers']}")
    print(f"Retention Rate at End: {result['retention_rate_at_end']}")
    print()

    # Test 3: KPI Dashboard
    print("[TOOL 3] KPI Dashboard")
    print("-" * 80)
    metrics = {"monthly_revenue": 50000, "customers": 500, "monthly_active_users": 15000}
    result = kpi_dashboard(metrics)
    financial = result['dashboard']['financial_metrics']
    print(f"MRR: ${financial['mrr']:,.0f}")
    print(f"ARR: ${financial['arr']:,.0f}")
    print(f"Gross Margin: {financial['gross_margin']}")
    print(f"Burn Rate: {financial['burn_rate']}")
    growth = result['dashboard']['growth_metrics']
    print(f"MAU: {growth['mau']:,}")
    print(f"Customer Count: {growth['customer_count']:,}")
    print()

    # Test 4: Customer Segmentation
    print("[TOOL 4] Customer Segmentation")
    print("-" * 80)
    result = customer_segmentation(1000)
    print(f"Total Customers: {result['total_customers']}")
    for segment_name, segment_data in result['segments'].items():
        print(f"\n  {segment_name.upper()}:")
        print(f"    Count: {segment_data['count']} ({segment_data['percentage']})")
        print(f"    Revenue Contribution: {segment_data['revenue_contribution']}")
        if 'avg_ltv' in segment_data:
            print(f"    Avg LTV: {segment_data['avg_ltv']}")
    print()

    # Test 5: Performance Report
    print("[TOOL 5] Performance Report")
    print("-" * 80)
    metrics = {"revenue": 150000}
    result = performance_report("monthly", metrics)
    print(f"Report Period: {result['period']}")
    print(f"Key Highlights:")
    for highlight in result['key_highlights'][:3]:
        print(f"  - {highlight}")
    print(f"Health Status:")
    for metric, status in result['health_status'].items():
        print(f"  - {metric}: {status}")
    print()


def main():
    print("")
    print("=" * 80)
    print("BUSINESS TOOLS SUITE - FULL DEMONSTRATION".center(80))
    print("=" * 80)

    try:
        test_consulting_tools()
        test_marketing_tools()
        test_analytics_tools()

        # Summary
        print_section("BUSINESS TOOLS SUMMARY")
        print("Available Tool Categories:\n")
        print("[CONSULTING TOOLS] - 6 tools")
        print("  1. market_analysis - Analyze market opportunities")
        print("  2. competitive_analysis - Analyze competitors")
        print("  3. business_model_canvas - Create BMC")
        print("  4. go_to_market_strategy - Create GTM plan")
        print("  5. funding_strategy - Plan fundraising")
        print("  6. pricing_strategy - Develop pricing\n")

        print("[MARKETING TOOLS] - 6 tools")
        print("  1. campaign_plan - Plan marketing campaigns")
        print("  2. audience_analysis - Analyze target audience")
        print("  3. budget_optimizer - Optimize marketing spend")
        print("  4. content_calendar - Create content schedule")
        print("  5. social_media_strategy - Plan social media")
        print("  6. conversion_optimization - Improve conversion\n")

        print("[ANALYTICS TOOLS] - 6 tools")
        print("  1. revenue_forecast - Forecast revenue")
        print("  2. churn_analysis - Analyze customer churn")
        print("  3. kpi_dashboard - Generate KPI dashboard")
        print("  4. cohort_analysis - Analyze user cohorts")
        print("  5. customer_segmentation - Segment customers")
        print("  6. performance_report - Generate reports\n")

        print("=" * 80)
        print("TOTAL: 18 SPECIALIZED BUSINESS TOOLS READY".center(80))
        print("=" * 80)
        print()
        print("Next: Integrate these tools into your CEO agent!")
        print("  python agents/business_tools_integration.py")
        print()

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
