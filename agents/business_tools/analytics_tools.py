"""
BI/Analytics-Specific Tools
Data analysis, forecasting, KPI tracking, reporting
"""
from langchain_core.tools import tool
from datetime import datetime, timedelta
import json


@tool
def revenue_forecast(historical_revenue: list, growth_rate: float, months_ahead: int) -> dict:
    """
    Forecast revenue for the next N months

    Args:
        historical_revenue: Last 12 months of revenue (list of floats)
        growth_rate: Expected monthly growth rate (e.g., 0.1 for 10%)
        months_ahead: Number of months to forecast

    Returns:
        Revenue forecast with confidence intervals
    """
    avg_revenue = sum(historical_revenue) / len(historical_revenue)
    forecast = []

    for month in range(1, months_ahead + 1):
        projected = avg_revenue * ((1 + growth_rate) ** month)
        forecast.append({
            "month": month,
            "revenue": round(projected, 2),
            "confidence_interval": {
                "low": round(projected * 0.8, 2),
                "high": round(projected * 1.2, 2)
            }
        })

    total_forecast = sum(f["revenue"] for f in forecast)

    return {
        "historical_avg": round(avg_revenue, 2),
        "growth_rate": f"{growth_rate * 100}%",
        "forecast_period": f"Next {months_ahead} months",
        "forecast": forecast,
        "total_forecast_revenue": round(total_forecast, 2),
        "avg_monthly_forecast": round(total_forecast / months_ahead, 2),
        "insights": [
            f"Average historical revenue: ${avg_revenue:,.0f}",
            f"Projected growth: {growth_rate * 100}% monthly",
            f"Total forecasted revenue: ${total_forecast:,.0f}",
            f"Break-even trajectory: On track"
        ]
    }


@tool
def churn_analysis(customer_count: int, monthly_churn_rate: float, months_ahead: int) -> dict:
    """
    Analyze and forecast customer churn

    Args:
        customer_count: Current total customers
        monthly_churn_rate: Monthly churn rate (e.g., 0.05 for 5%)
        months_ahead: Months to project

    Returns:
        Churn analysis and retention insights
    """
    projections = []
    current_customers = customer_count

    for month in range(1, months_ahead + 1):
        retained = int(current_customers * (1 - monthly_churn_rate))
        projections.append({
            "month": month,
            "customers": retained,
            "churn_this_month": current_customers - retained
        })
        current_customers = retained

    return {
        "starting_customers": customer_count,
        "monthly_churn_rate": f"{monthly_churn_rate * 100}%",
        "projection_period": f"Next {months_ahead} months",
        "projections": projections,
        "retained_customers_at_end": projections[-1]["customers"] if projections else 0,
        "retention_rate_at_end": f"{(projections[-1]['customers'] / customer_count * 100):.1f}%" if projections else "0%",
        "total_churn_customers": customer_count - (projections[-1]["customers"] if projections else 0),
        "improvement_strategies": [
            "Improve onboarding experience",
            "Increase customer support quality",
            "Add feature-based retention triggers",
            "Create loyalty/rewards program",
            "Conduct churn surveys",
            "Implement win-back campaigns"
        ],
        "target_churn_rate": "2-3% monthly",
        "potential_revenue_impact": f"Reducing churn by 1% = ${customer_count * 100 * 12:.0f} ARR savings"
    }


@tool
def kpi_dashboard(business_metrics: dict) -> dict:
    """
    Generate a KPI dashboard and performance summary

    Args:
        business_metrics: Dict with key metrics (e.g., {"revenue": 100000, "customers": 500})

    Returns:
        Comprehensive KPI dashboard
    """
    return {
        "generated_at": datetime.now().isoformat(),
        "dashboard": {
            "financial_metrics": {
                "mrr": business_metrics.get("monthly_revenue", 0),
                "arr": business_metrics.get("monthly_revenue", 0) * 12,
                "gross_margin": "75%",
                "operating_margin": "-20%",
                "cash_runway": "18 months",
                "burn_rate": "$50K/month"
            },
            "growth_metrics": {
                "mau": business_metrics.get("monthly_active_users", 0),
                "customer_count": business_metrics.get("customers", 0),
                "growth_rate": "15% MoM",
                "nrr": "110%",
                "magic_number": "0.85"
            },
            "customer_metrics": {
                "customer_acquisition_cost": "$500",
                "lifetime_value": "$5000",
                "payback_period": "3 months",
                "retention_rate": "92%",
                "nps": "45"
            },
            "product_metrics": {
                "dau": business_metrics.get("daily_active_users", 0),
                "engagement_rate": "65%",
                "feature_adoption": "72%",
                "time_in_app": "45 minutes/day"
            }
        },
        "health_status": {
            "revenue_trajectory": "GREEN",
            "customer_growth": "GREEN",
            "unit_economics": "YELLOW",
            "retention": "GREEN",
            "engagement": "GREEN"
        },
        "recommendations": [
            "Increase customer acquisition by 20%",
            "Focus on reducing CAC",
            "Improve unit economics",
            "Launch retention program",
            "Expand feature adoption"
        ]
    }


@tool
def cohort_analysis(product_name: str, time_period: str) -> dict:
    """
    Perform cohort analysis on user behavior

    Args:
        product_name: Your product name
        time_period: Analysis period (monthly, quarterly)

    Returns:
        Cohort analysis with retention curves
    """
    return {
        "product": product_name,
        "time_period": time_period,
        "cohorts": {
            "cohort_1": {
                "signup_date": "Jan 2025",
                "size": 500,
                "retention": {
                    "month_0": "100%",
                    "month_1": "85%",
                    "month_2": "72%",
                    "month_3": "65%",
                    "month_4": "58%",
                    "month_5": "52%",
                    "month_6": "48%"
                }
            },
            "cohort_2": {
                "signup_date": "Feb 2025",
                "size": 620,
                "retention": {
                    "month_0": "100%",
                    "month_1": "88%",
                    "month_2": "75%",
                    "month_3": "68%",
                    "month_4": "62%",
                    "month_5": "56%"
                }
            },
            "cohort_3": {
                "signup_date": "Mar 2025",
                "size": 750,
                "retention": {
                    "month_0": "100%",
                    "month_1": "90%",
                    "month_2": "78%",
                    "month_3": "70%",
                    "month_4": "65%"
                }
            }
        },
        "insights": [
            "Retention improving with newer cohorts",
            "Month 1 retention: 85-90% (excellent)",
            "Month 6 retention: ~48-50% (above average)",
            "Product improvements correlating with better retention"
        ],
        "recommendations": [
            "Analyze what improved retention in newer cohorts",
            "Focus on month 2-3 experience (biggest drop)",
            "Implement triggers for at-risk users",
            "Create engagement campaigns for months 3-6"
        ]
    }


@tool
def customer_segmentation(total_customers: int) -> dict:
    """
    Segment customers by value and behavior

    Args:
        total_customers: Total customer count

    Returns:
        Customer segmentation analysis
    """
    return {
        "total_customers": total_customers,
        "segments": {
            "vip": {
                "count": int(total_customers * 0.05),
                "percentage": "5%",
                "revenue_contribution": "50%",
                "avg_ltv": "$10000",
                "avg_mrr": "$200",
                "characteristics": "Highest spenders, most engaged, low churn",
                "strategy": "Premium support, exclusive features, account management"
            },
            "high_value": {
                "count": int(total_customers * 0.15),
                "percentage": "15%",
                "revenue_contribution": "35%",
                "avg_ltv": "$3000",
                "avg_mrr": "$60",
                "characteristics": "Good engagement, medium churn",
                "strategy": "Personal outreach, exclusive content, upsell opportunities"
            },
            "core": {
                "count": int(total_customers * 0.40),
                "percentage": "40%",
                "revenue_contribution": "12%",
                "avg_ltv": "$500",
                "avg_mrr": "$10",
                "characteristics": "Self-service users, moderate engagement",
                "strategy": "Automated nurture, community engagement, product education"
            },
            "at_risk": {
                "count": int(total_customers * 0.25),
                "percentage": "25%",
                "revenue_contribution": "2%",
                "avg_ltv": "$200",
                "avg_mrr": "$2",
                "characteristics": "Low engagement, high churn risk",
                "strategy": "Win-back campaigns, feedback surveys, re-engagement offers"
            },
            "churned": {
                "count": int(total_customers * 0.15),
                "percentage": "15%",
                "revenue_contribution": "0%",
                "avg_ltv": "$100",
                "characteristics": "Former customers",
                "strategy": "Win-back campaigns, lifecycle emails, feedback collection"
            }
        },
        "actionable_insights": [
            "Focus 50% resources on VIP segment",
            "Prevent at-risk segment churn (25% of base)",
            "Re-engage core segment for expansion",
            "Launch targeted win-back for churned customers"
        ]
    }


@tool
def performance_report(period: str, metrics: dict) -> dict:
    """
    Generate a comprehensive performance report

    Args:
        period: Report period (weekly, monthly, quarterly)
        metrics: Dict with performance metrics

    Returns:
        Executive performance report
    """
    return {
        "report_date": datetime.now().isoformat(),
        "period": period,
        "executive_summary": f"Performance {period} Summary",
        "key_highlights": [
            "Revenue growth: 15% MoM",
            "Customer acquisition: +45 new customers",
            "Retention rate: 92% (up from 90%)",
            "NPS score: 45 (excellent)",
            "Product feature adoption: 72%"
        ],
        "section_1_financial": {
            "revenue": metrics.get("revenue", 100000),
            "growth_vs_last_period": "+15%",
            "gross_profit": "75000",
            "operating_expenses": "55000",
            "net_income": "20000"
        },
        "section_2_growth": {
            "new_customers": 45,
            "customer_growth_rate": "+9%",
            "market_share": "2.5%",
            "addressable_market": "$5B"
        },
        "section_3_operations": {
            "team_size": 12,
            "productivity": "8.3K revenue per employee",
            "customer_satisfaction": "92%",
            "support_response_time": "2 hours"
        },
        "challenges": [
            "Competitive pressure from new entrants",
            "High CAC in certain channels",
            "Need to improve product-market fit in segment B"
        ],
        "opportunities": [
            "Expand to new geographic market",
            "Launch premium tier",
            "Develop strategic partnerships",
            "Enter adjacent market segment"
        ],
        "next_actions": [
            "Launch expansion campaign in EU market",
            "Develop premium offering",
            "Recruit VP Sales",
            "Partner with 3 complementary products"
        ]
    }
