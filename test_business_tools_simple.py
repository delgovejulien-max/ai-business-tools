#!/usr/bin/env python
"""
Test Business Tools - Simple Version
Direct function calls without decorators
"""
from agents.business_tools.consulting_tools import (
    market_analysis as ma_tool,
    competitive_analysis as ca_tool,
    business_model_canvas as bmc_tool,
    go_to_market_strategy as gtm_tool,
    pricing_strategy as ps_tool,
)
from agents.business_tools.marketing_tools import (
    campaign_plan as cp_tool,
    audience_analysis as aa_tool,
    budget_optimizer as bo_tool,
    content_calendar as cc_tool,
)
from agents.business_tools.analytics_tools import (
    revenue_forecast as rf_tool,
    churn_analysis as ca2_tool,
    kpi_dashboard as kd_tool,
    customer_segmentation as cs_tool,
    performance_report as pr_tool,
)


def invoke_tool(tool_func, *args, **kwargs):
    """Call a LangChain tool properly"""
    if hasattr(tool_func, 'invoke'):
        return tool_func.invoke({**dict(zip(['arg' + str(i) for i in range(len(args))], args)), **kwargs})
    else:
        return tool_func(*args, **kwargs)


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
    try:
        result = ma_tool.invoke({
            "market_name": "European SaaS",
            "product_category": "project management",
            "target_audience": "Startups"
        })
        print(f"Market: {result['market']}")
        print(f"Market Size: {result['market_size']}")
        print(f"Growth Rate: {result['growth_rate']}")
        print(f"Investment Needed: {result['investment_needed']}")
        print(f"Top Opportunities:")
        for opp in result['opportunities'][:2]:
            print(f"  - {opp}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 2: Competitive Analysis
    print("[TOOL 2] Competitive Analysis")
    print("-" * 80)
    try:
        result = ca_tool.invoke({
            "your_product": "AI-powered project management tool",
            "competitors": ["Asana", "Monday.com", "Notion"]
        })
        print(f"Your Product: {result['your_product']}")
        print(f"Competitors Analyzed: {result['competitors_analyzed']}")
        print(f"Your Advantages:")
        for adv in result['your_advantages'][:3]:
            print(f"  + {adv}")
        print(f"Recommended Positioning: {result['recommended_positioning']}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 3: Business Model Canvas
    print("[TOOL 3] Business Model Canvas")
    print("-" * 80)
    try:
        result = bmc_tool.invoke({
            "company_name": "TechFlow AI",
            "business_idea": "AI-powered workflow automation"
        })
        canvas = result['canvas']
        print(f"Company: {result['company']}")
        print(f"Value Propositions: {', '.join(canvas['value_propositions'][:2])}")
        print(f"Revenue Streams: {', '.join(canvas['revenue_streams'][:2])}")
        print(f"Year 1 Revenue: {result['financial_projections']['year_1_revenue']}")
        print(f"Year 2 Revenue: {result['financial_projections']['year_2_revenue']}")
        print(f"Year 3 Revenue: {result['financial_projections']['year_3_revenue']}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 4: Go-to-Market Strategy
    print("[TOOL 4] Go-to-Market Strategy")
    print("-" * 80)
    try:
        result = gtm_tool.invoke({
            "product_name": "TechFlow",
            "target_market": "Startups",
            "budget_usd": 50000
        })
        print(f"Product: {result['product']}")
        print(f"Target Market: {result['target_market']}")
        print(f"Budget: ${result['budget']:,.0f}")
        print(f"Launch Timeline:")
        for phase, timeline in result['launch_timeline'].items():
            print(f"  - {phase}: {timeline}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 5: Pricing Strategy
    print("[TOOL 5] Pricing Strategy")
    print("-" * 80)
    try:
        result = ps_tool.invoke({
            "product_name": "TechFlow",
            "target_segment": "Startups",
            "production_cost": 1000
        })
        print(f"Product: {result['product']}")
        print(f"Pricing Strategy: {result['pricing_strategy_type']}")
        pricing = result['recommended_pricing']
        for tier, info in list(pricing.items())[:2]:
            print(f"\n  {tier.upper()}:")
            print(f"    Price: {info['price']}")
            print(f"    Margin: {info['margin']}")
            print(f"    Target: {info['target_customers']}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def test_marketing_tools():
    """Test marketing-specific tools"""
    print_section("MARKETING TOOLS DEMONSTRATION")

    # Test 1: Campaign Plan
    print("[TOOL 1] Campaign Plan")
    print("-" * 80)
    try:
        result = cp_tool.invoke({
            "campaign_name": "Product Launch",
            "objective": "awareness",
            "target_audience": "Tech startups",
            "budget": 50000
        })
        print(f"Campaign: {result['campaign_name']}")
        print(f"Objective: {result['objective']}")
        print(f"Budget: ${result['budget']:,.0f}")
        print(f"Duration: {result['duration_days']} days")
        print(f"Target KPIs:")
        for kpi, value in list(result['target_kpis'].items())[:3]:
            print(f"  - {kpi}: {value}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 2: Audience Analysis
    print("[TOOL 2] Audience Analysis")
    print("-" * 80)
    try:
        result = aa_tool.invoke({
            "audience_segment": "Startup Founders",
            "market": "SaaS"
        })
        persona = result['persona']
        print(f"Segment: {result['segment']}")
        print(f"Persona: {persona['name']} - {persona['title']}")
        print(f"Income: {persona['income']}")
        print(f"Top Pain Points:")
        for pain in result['pain_points'][:3]:
            print(f"  - {pain}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 3: Budget Optimizer
    print("[TOOL 3] Budget Optimizer")
    print("-" * 80)
    try:
        result = bo_tool.invoke({
            "total_budget": 50000,
            "channels": ["social_media", "paid_ads", "content", "email"],
            "goal": "leads"
        })
        print(f"Total Budget: ${result['total_budget']:,.0f}")
        print(f"Goal: {result['goal']}")
        print(f"Budget Allocation:")
        for channel, data in result['allocation'].items():
            amount = data['amount']
            pct = data['percentage']
            print(f"  - {channel}: ${amount:,.0f} ({pct:.1f}%)")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 4: Content Calendar
    print("[TOOL 4] Content Calendar")
    print("-" * 80)
    try:
        result = cc_tool.invoke({
            "campaign_duration_days": 30,
            "frequency": "weekly"
        })
        print(f"Campaign Duration: {result['duration_days']} days")
        print(f"Posting Frequency: {result['frequency']}")
        print(f"Total Posts: {result['total_posts']}")
        print(f"Content Types: {', '.join(result['content_types'][:4])}")
        print(f"Best Posting Days: {', '.join(result['posting_schedule']['best_days'])}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def test_analytics_tools():
    """Test BI/Analytics tools"""
    print_section("ANALYTICS & BI TOOLS DEMONSTRATION")

    # Test 1: Revenue Forecast
    print("[TOOL 1] Revenue Forecast")
    print("-" * 80)
    try:
        historical = [10000, 12000, 14000, 15000, 17000, 19000, 21000, 23000, 25000, 27000, 29000, 31000]
        result = rf_tool.invoke({
            "historical_revenue": historical,
            "growth_rate": 0.10,
            "months_ahead": 6
        })
        print(f"Historical Avg: ${result['historical_avg']:,.0f}")
        print(f"Growth Rate: {result['growth_rate']}")
        print(f"6-Month Forecast:")
        for forecast in result['forecast'][:3]:
            print(f"  Month {forecast['month']}: ${forecast['revenue']:,.0f}")
        print(f"Total 6M Revenue: ${result['total_forecast_revenue']:,.0f}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 2: Churn Analysis
    print("[TOOL 2] Churn Analysis")
    print("-" * 80)
    try:
        result = ca2_tool.invoke({
            "customer_count": 1000,
            "monthly_churn_rate": 0.05,
            "months_ahead": 6
        })
        print(f"Starting Customers: {result['starting_customers']}")
        print(f"Monthly Churn Rate: {result['monthly_churn_rate']}")
        print(f"Customers in 6 Months: {result['retained_customers_at_end']}")
        print(f"Retention Rate: {result['retention_rate_at_end']}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 3: KPI Dashboard
    print("[TOOL 3] KPI Dashboard")
    print("-" * 80)
    try:
        result = kd_tool.invoke({
            "business_metrics": {
                "monthly_revenue": 50000,
                "customers": 500,
                "monthly_active_users": 15000,
                "daily_active_users": 5000
            }
        })
        financial = result['dashboard']['financial_metrics']
        print(f"MRR: ${financial['mrr']:,.0f}")
        print(f"ARR: ${financial['arr']:,.0f}")
        print(f"Gross Margin: {financial['gross_margin']}")
        growth = result['dashboard']['growth_metrics']
        print(f"MAU: {growth['mau']:,}")
        print(f"Customer Count: {growth['customer_count']:,}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 4: Customer Segmentation
    print("[TOOL 4] Customer Segmentation")
    print("-" * 80)
    try:
        result = cs_tool.invoke({
            "total_customers": 1000
        })
        print(f"Total Customers: {result['total_customers']}")
        for segment_name, segment_data in list(result['segments'].items())[:3]:
            print(f"\n  {segment_name.upper()}:")
            print(f"    Count: {segment_data['count']} ({segment_data['percentage']})")
            print(f"    Revenue: {segment_data['revenue_contribution']}")
    except Exception as e:
        print(f"Error: {e}")
    print()

    # Test 5: Performance Report
    print("[TOOL 5] Performance Report")
    print("-" * 80)
    try:
        result = pr_tool.invoke({
            "period": "monthly",
            "metrics": {"revenue": 150000}
        })
        print(f"Report Period: {result['period']}")
        print(f"Key Highlights:")
        for highlight in result['key_highlights'][:3]:
            print(f"  - {highlight}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def main():
    print("")
    print("=" * 80)
    print("BUSINESS TOOLS SUITE - FULL DEMONSTRATION".center(80))
    print("=" * 80)

    test_consulting_tools()
    test_marketing_tools()
    test_analytics_tools()

    # Summary
    print_section("SUMMARY: 18 SPECIALIZED BUSINESS TOOLS")
    print("[CONSULTING] 6 tools for strategy & business planning")
    print("  - market_analysis, competitive_analysis, business_model_canvas")
    print("  - go_to_market_strategy, funding_strategy, pricing_strategy\n")

    print("[MARKETING] 6 tools for campaigns & customer acquisition")
    print("  - campaign_plan, audience_analysis, budget_optimizer")
    print("  - content_calendar, social_media_strategy, conversion_optimization\n")

    print("[ANALYTICS] 6 tools for data & performance insights")
    print("  - revenue_forecast, churn_analysis, kpi_dashboard")
    print("  - cohort_analysis, customer_segmentation, performance_report\n")

    print("=" * 80)
    print("Next Step: Integrate into your CEO agent!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
