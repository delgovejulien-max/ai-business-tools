"""
Admin Dashboard for AI Business Tools SaaS
Real-time analytics, user metrics, and revenue tracking
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict
import json


class AdminDashboard:
    """Admin analytics dashboard"""

    def __init__(self):
        self.db_path = 'marketing.db'
        self.app_db_path = 'app_state.db'

    # ==================== DATA RETRIEVAL ====================

    def get_user_metrics(self) -> Dict:
        """Get user signup and activity metrics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Total users
        c.execute('SELECT COUNT(*) FROM subscribers WHERE status = ?', ('active',))
        total_users = c.fetchone()[0]

        # Users by plan
        c.execute('''SELECT plan, COUNT(*) FROM subscribers
                     WHERE status = ? GROUP BY plan''', ('active',))
        plan_breakdown = dict(c.fetchall())

        # New users (last 7 days)
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        c.execute('''SELECT COUNT(*) FROM subscribers
                     WHERE signup_date > ? AND status = ?''',
                  (seven_days_ago, 'active'))
        new_users_7d = c.fetchone()[0]

        # New users (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        c.execute('''SELECT COUNT(*) FROM subscribers
                     WHERE signup_date > ? AND status = ?''',
                  (thirty_days_ago, 'active'))
        new_users_30d = c.fetchone()[0]

        # Churn (users with inactive status in last 30 days)
        c.execute('''SELECT COUNT(*) FROM subscribers
                     WHERE status = ? AND signup_date < ?''',
                  ('inactive', thirty_days_ago))
        churned_users = c.fetchone()[0]

        conn.close()

        return {
            'total_users': total_users,
            'free_users': plan_breakdown.get('free', 0),
            'pro_users': plan_breakdown.get('pro', 0),
            'business_users': plan_breakdown.get('business', 0),
            'new_users_7d': new_users_7d,
            'new_users_30d': new_users_30d,
            'churned_users': churned_users,
            'churn_rate': (churned_users / total_users * 100) if total_users > 0 else 0
        }

    def get_revenue_metrics(self) -> Dict:
        """Get revenue and subscription metrics"""
        # In production, these would come from Stripe
        # For demo, we calculate based on subscriber plans
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''SELECT plan, COUNT(*) FROM subscribers
                     WHERE status = ? GROUP BY plan''', ('active',))
        plan_counts = dict(c.fetchall())

        pro_count = plan_counts.get('pro', 0)
        business_count = plan_counts.get('business', 0)

        # MRR (Monthly Recurring Revenue)
        mrr = (pro_count * 49) + (business_count * 199)

        # ARR (Annual Recurring Revenue)
        arr = mrr * 12

        # Average Revenue Per User (ARPU)
        total_paid_users = pro_count + business_count
        arpu = (mrr / total_paid_users) if total_paid_users > 0 else 0

        # Conversion rate
        total_users = plan_counts.get('free', 0) + pro_count + business_count
        conversion_rate = (total_paid_users / total_users * 100) if total_users > 0 else 0

        conn.close()

        return {
            'mrr': mrr,
            'arr': arr,
            'arpu': arpu,
            'conversion_rate': conversion_rate,
            'pro_subscriptions': pro_count,
            'business_subscriptions': business_count,
            'total_paid_users': total_paid_users
        }

    def get_email_metrics(self) -> Dict:
        """Get email marketing metrics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Total emails sent
        c.execute('SELECT COUNT(*) FROM email_campaigns WHERE sent_date IS NOT NULL')
        total_sent = c.fetchone()[0]

        # Opened
        c.execute('SELECT COUNT(*) FROM email_campaigns WHERE opened = 1')
        total_opened = c.fetchone()[0]

        # Clicked
        c.execute('SELECT COUNT(*) FROM email_campaigns WHERE clicked = 1')
        total_clicked = c.fetchone()[0]

        # By template type
        c.execute('''SELECT template_type, COUNT(*) FROM email_campaigns
                     WHERE sent_date IS NOT NULL
                     GROUP BY template_type''')
        template_breakdown = dict(c.fetchall())

        conn.close()

        return {
            'total_sent': total_sent,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'open_rate': (total_opened / total_sent * 100) if total_sent > 0 else 0,
            'click_rate': (total_clicked / total_sent * 100) if total_sent > 0 else 0,
            'template_breakdown': template_breakdown
        }

    def get_tool_usage_metrics(self) -> Dict:
        """Get tool usage statistics"""
        conn = sqlite3.connect(self.app_db_path)
        c = conn.cursor()

        try:
            # Tool usage by name
            c.execute('''SELECT tool_name, COUNT(*) FROM tool_usage
                         GROUP BY tool_name ORDER BY COUNT(*) DESC''')
            tool_usage = dict(c.fetchall())

            # Total tool invocations
            c.execute('SELECT COUNT(*) FROM tool_usage')
            total_invocations = c.fetchone()[0]

            # Most used category (approximate based on tool names)
            categories = defaultdict(int)
            for tool in tool_usage.keys():
                if 'market' in tool.lower() or 'competitive' in tool.lower() or 'pricing' in tool.lower():
                    categories['Consulting'] += tool_usage[tool]
                elif 'campaign' in tool.lower() or 'audience' in tool.lower() or 'budget' in tool.lower():
                    categories['Marketing'] += tool_usage[tool]
                else:
                    categories['Analytics'] += tool_usage[tool]

        except:
            tool_usage = {}
            total_invocations = 0
            categories = defaultdict(int)

        conn.close()

        return {
            'total_invocations': total_invocations,
            'top_tools': tool_usage,
            'category_breakdown': dict(categories)
        }

    def get_growth_metrics(self) -> Dict:
        """Get growth trend data (last 30 days)"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        growth_data = {'date': [], 'users': [], 'signups': []}

        for i in range(30, 0, -1):
            date = (datetime.now() - timedelta(days=i)).date()
            date_str = date.isoformat()

            # Users on this date
            c.execute('''SELECT COUNT(*) FROM subscribers
                         WHERE signup_date <= ? AND status = ?
                         ORDER BY signup_date DESC LIMIT 1''',
                      (date_str + ' 23:59:59', 'active'))
            result = c.fetchone()
            users = result[0] if result else 0

            # Signups on this date
            c.execute('''SELECT COUNT(*) FROM subscribers
                         WHERE DATE(signup_date) = ?''', (date_str,))
            signups = c.fetchone()[0]

            growth_data['date'].append(date_str)
            growth_data['users'].append(users)
            growth_data['signups'].append(signups)

        conn.close()
        return growth_data

    def get_user_segments(self) -> Dict:
        """Get user segmentation data"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # By plan
        c.execute('''SELECT plan, COUNT(*) FROM subscribers
                     WHERE status = ? GROUP BY plan''', ('active',))
        by_plan = dict(c.fetchall())

        # Engagement levels (based on email interactions)
        c.execute('''SELECT email, COUNT(*) as engagement
                     FROM email_campaigns
                     WHERE opened = 1 OR clicked = 1
                     GROUP BY email''')
        engagement_scores = defaultdict(int)
        for email, count in c.fetchall():
            if count >= 5:
                engagement_scores['High Engagement'] += 1
            elif count >= 2:
                engagement_scores['Medium Engagement'] += 1
            else:
                engagement_scores['Low Engagement'] += 1

        # By signup source (if tracked)
        high_value = sum(1 for plan, count in by_plan.items() if plan in ['pro', 'business'])
        free_only = by_plan.get('free', 0)

        conn.close()

        return {
            'by_plan': by_plan,
            'engagement': dict(engagement_scores),
            'value_segments': {
                'High-Value (Pro+)': high_value,
                'Free Users': free_only
            }
        }

    def get_funnel_data(self) -> Dict:
        """Get conversion funnel data"""
        users = self.get_user_metrics()
        revenue = self.get_revenue_metrics()

        return {
            'stage': ['Free Signups', 'Pro Trials', 'Pro Paid', 'Business'],
            'count': [
                users['free_users'],
                max(1, users['pro_users'] // 3),  # Assume 1/3 converted
                users['pro_users'],
                users['business_users']
            ]
        }

    # ==================== STREAMLIT DASHBOARD ====================

    def render_dashboard(self):
        """Render complete admin dashboard"""
        st.set_page_config(page_title="Admin Dashboard", layout="wide")

        # Title
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1f77b4, #0d47a1); padding: 20px; border-radius: 10px; margin-bottom: 30px;">
            <h1 style="color: white; margin: 0;">📊 AI Business Tools Admin Dashboard</h1>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">Real-time analytics and metrics</p>
        </div>
        """, unsafe_allow_html=True)

        # Sidebar filters
        with st.sidebar:
            st.header("Filters")
            time_period = st.selectbox(
                "Time Period",
                ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"]
            )
            view_type = st.selectbox(
                "View",
                ["Overview", "Users", "Revenue", "Marketing", "Tools"]
            )

        # Render based on view type
        if view_type == "Overview":
            self.render_overview()
        elif view_type == "Users":
            self.render_users_analytics()
        elif view_type == "Revenue":
            self.render_revenue_analytics()
        elif view_type == "Marketing":
            self.render_marketing_analytics()
        elif view_type == "Tools":
            self.render_tool_analytics()

    def render_overview(self):
        """Render overview dashboard"""
        st.subheader("Overview")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        users = self.get_user_metrics()
        revenue = self.get_revenue_metrics()

        with col1:
            st.metric(
                "Total Users",
                f"{users['total_users']:,}",
                f"+{users['new_users_30d']} this month"
            )

        with col2:
            st.metric(
                "Monthly Revenue (MRR)",
                f"${revenue['mrr']:,.0f}",
                f"${revenue['arr']:,.0f}/year"
            )

        with col3:
            st.metric(
                "Conversion Rate",
                f"{revenue['conversion_rate']:.1f}%",
                f"{revenue['total_paid_users']} paid users"
            )

        with col4:
            st.metric(
                "Churn Rate",
                f"{users['churn_rate']:.1f}%",
                f"{users['churned_users']} churned"
            )

        # Growth chart
        st.subheader("Growth Trend (30 days)")
        growth = self.get_growth_metrics()
        df_growth = pd.DataFrame(growth)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_growth['date'],
            y=df_growth['users'],
            name='Total Users',
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2)
        ))
        fig.add_trace(go.Bar(
            x=df_growth['date'],
            y=df_growth['signups'],
            name='New Signups',
            marker=dict(color='#ff6b35', opacity=0.6)
        ))

        fig.update_layout(
            hovermode='x unified',
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Plan breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Users by Plan")
            plan_data = pd.DataFrame({
                'Plan': ['Free', 'Pro', 'Business'],
                'Count': [
                    users['free_users'],
                    users['pro_users'],
                    users['business_users']
                ]
            })

            fig = px.pie(
                plan_data,
                values='Count',
                names='Plan',
                color_discrete_map={
                    'Free': '#ccc',
                    'Pro': '#1f77b4',
                    'Business': '#ff6b35'
                }
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Revenue by Plan")
            revenue_data = pd.DataFrame({
                'Plan': ['Pro', 'Business'],
                'Revenue': [
                    users['pro_users'] * 49,
                    users['business_users'] * 199
                ]
            })

            fig = px.bar(
                revenue_data,
                x='Plan',
                y='Revenue',
                color='Plan',
                color_discrete_map={
                    'Pro': '#1f77b4',
                    'Business': '#ff6b35'
                }
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    def render_users_analytics(self):
        """Render user analytics view"""
        st.subheader("User Analytics")

        users = self.get_user_metrics()
        segments = self.get_user_segments()

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", users['total_users'])
        with col2:
            st.metric("New (30d)", users['new_users_30d'])
        with col3:
            st.metric("Churn Rate", f"{users['churn_rate']:.1f}%")

        # User segments
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("By Engagement Level")
            engagement_df = pd.DataFrame({
                'Segment': list(segments['engagement'].keys()),
                'Users': list(segments['engagement'].values())
            })

            fig = px.bar(
                engagement_df,
                x='Segment',
                y='Users',
                color='Segment',
                color_discrete_sequence=['#ff6b35', '#1f77b4', '#aaa']
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("By Value Segment")
            value_df = pd.DataFrame({
                'Segment': list(segments['value_segments'].keys()),
                'Count': list(segments['value_segments'].values())
            })

            fig = px.pie(
                value_df,
                values='Count',
                names='Segment',
                color_discrete_map={
                    'High-Value (Pro+)': '#ff6b35',
                    'Free Users': '#1f77b4'
                }
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        # Signup sources
        st.subheader("Acquisition & Retention")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Free Users", users['free_users'])
        with col2:
            st.metric("Pro Users", users['pro_users'])
        with col3:
            st.metric("Business Users", users['business_users'])

    def render_revenue_analytics(self):
        """Render revenue analytics view"""
        st.subheader("Revenue Analytics")

        revenue = self.get_revenue_metrics()

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("MRR", f"${revenue['mrr']:,.0f}")
        with col2:
            st.metric("ARR", f"${revenue['arr']:,.0f}")
        with col3:
            st.metric("ARPU", f"${revenue['arpu']:.2f}")
        with col4:
            st.metric("Conversion", f"{revenue['conversion_rate']:.1f}%")

        # Revenue projection
        st.subheader("Revenue Projections")
        months = []
        projected_mrr = []
        current_mrr = revenue['mrr']

        for i in range(12):
            months.append(f"Month {i+1}")
            # Assume 10% MoM growth
            projected_mrr.append(current_mrr * (1.1 ** i))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=projected_mrr,
            mode='lines+markers',
            name='Projected MRR',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy'
        ))

        fig.update_layout(
            yaxis_title="MRR ($)",
            hovermode='x',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Plan breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenue by Plan")
            plan_revenue = pd.DataFrame({
                'Plan': ['Pro', 'Business'],
                'Revenue': [
                    revenue['pro_subscriptions'] * 49,
                    revenue['business_subscriptions'] * 199
                ]
            })

            fig = px.bar(
                plan_revenue,
                x='Plan',
                y='Revenue',
                color='Plan',
                color_discrete_map={'Pro': '#1f77b4', 'Business': '#ff6b35'}
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Customer Lifetime Value")
            # Simple LCV calculation: (monthly revenue / churn rate) if no churn
            users = self.get_user_metrics()
            avg_mrr_per_customer = revenue['arpu']
            st.metric("Avg Revenue Per User", f"${avg_mrr_per_customer:.2f}")
            st.metric("Estimated Customer LCV", f"${avg_mrr_per_customer * 24:.0f}")

    def render_marketing_analytics(self):
        """Render marketing analytics view"""
        st.subheader("Marketing Analytics")

        email = self.get_email_metrics()

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Emails Sent", f"{email['total_sent']:,}")
        with col2:
            st.metric("Open Rate", f"{email['open_rate']:.1f}%")
        with col3:
            st.metric("Click Rate", f"{email['click_rate']:.1f}%")

        # Email template performance
        st.subheader("Email Template Performance")
        if email['template_breakdown']:
            template_df = pd.DataFrame({
                'Template': list(email['template_breakdown'].keys()),
                'Sent': list(email['template_breakdown'].values())
            })

            fig = px.bar(
                template_df,
                x='Template',
                y='Sent',
                color='Template',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    def render_tool_analytics(self):
        """Render tool usage analytics"""
        st.subheader("Tool Usage Analytics")

        tools = self.get_tool_usage_metrics()

        # Key metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Tool Uses", f"{tools['total_invocations']:,}")

        if tools['category_breakdown']:
            with col2:
                st.metric(
                    "Most Used Category",
                    max(tools['category_breakdown'], key=tools['category_breakdown'].get)
                        if tools['category_breakdown'] else "N/A"
                )

        # Top tools
        if tools['top_tools']:
            st.subheader("Top 10 Most Used Tools")
            top_tools = dict(sorted(
                tools['top_tools'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10])

            tools_df = pd.DataFrame({
                'Tool': list(top_tools.keys()),
                'Uses': list(top_tools.values())
            })

            fig = px.barh(
                tools_df,
                x='Uses',
                y='Tool',
                color='Uses',
                color_continuous_scale='Blues',
                orientation='h'
            )
            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        # Category breakdown
        if tools['category_breakdown']:
            st.subheader("Tool Usage by Category")
            category_df = pd.DataFrame({
                'Category': list(tools['category_breakdown'].keys()),
                'Uses': list(tools['category_breakdown'].values())
            })

            fig = px.pie(
                category_df,
                values='Uses',
                names='Category',
                color_discrete_map={
                    'Consulting': '#1f77b4',
                    'Marketing': '#ff6b35',
                    'Analytics': '#2ecc71'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)


def main():
    """Main dashboard entry point"""
    dashboard = AdminDashboard()
    dashboard.render_dashboard()


if __name__ == "__main__":
    main()
