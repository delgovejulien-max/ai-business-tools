"""
Business Tools Module
Domain-specific tools for Consulting, Marketing, and BI/Analytics
"""
from agents.business_tools.consulting_tools import (
    market_analysis,
    competitive_analysis,
    business_model_canvas,
    go_to_market_strategy,
    funding_strategy,
    pricing_strategy,
)

from agents.business_tools.marketing_tools import (
    campaign_plan,
    audience_analysis,
    budget_optimizer,
    content_calendar,
    social_media_strategy,
    conversion_optimization,
)

from agents.business_tools.analytics_tools import (
    revenue_forecast,
    churn_analysis,
    kpi_dashboard,
    cohort_analysis,
    customer_segmentation,
    performance_report,
)

__all__ = [
    # Consulting
    "market_analysis",
    "competitive_analysis",
    "business_model_canvas",
    "go_to_market_strategy",
    "funding_strategy",
    "pricing_strategy",
    # Marketing
    "campaign_plan",
    "audience_analysis",
    "budget_optimizer",
    "content_calendar",
    "social_media_strategy",
    "conversion_optimization",
    # Analytics
    "revenue_forecast",
    "churn_analysis",
    "kpi_dashboard",
    "cohort_analysis",
    "customer_segmentation",
    "performance_report",
]
