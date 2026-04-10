"""
Metrics Tracker - Continuous Improvement System
Real-time measurement of KPIs and engagement
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class UserSession:
    session_id: str
    user_id: str
    created_at: str
    completed_onboarding: bool
    tools_used: int
    exports_created: int
    last_activity: str
    plan: str

@dataclass
class DailyMetrics:
    date: str
    new_signups: int
    onboarding_completion_rate: float
    avg_tools_per_user: float
    weekly_active_users: int
    paid_conversions: int
    mrr: float
    export_rate: float
    share_rate: float
    user_satisfaction: float

class MetricsDatabase:
    """SQLite database for metrics tracking"""

    def __init__(self, db_path: str = "metrics.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize metrics database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # User sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                company TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_onboarding BOOLEAN DEFAULT FALSE,
                tools_used INTEGER DEFAULT 0,
                exports_created INTEGER DEFAULT 0,
                shares_created INTEGER DEFAULT 0,
                last_activity TIMESTAMP,
                plan TEXT DEFAULT 'free',
                paid_at TIMESTAMP,
                mrr FLOAT DEFAULT 0
            )
        """)

        # Tools usage table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                category TEXT NOT NULL,
                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_time_ms INTEGER,
                result_quality TEXT,
                FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
            )
        """)

        # Daily metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                date TEXT PRIMARY KEY,
                new_signups INTEGER,
                onboarding_completion_rate FLOAT,
                avg_tools_per_user FLOAT,
                weekly_active_users INTEGER,
                paid_conversions INTEGER,
                mrr FLOAT,
                export_rate FLOAT,
                share_rate FLOAT,
                user_satisfaction FLOAT,
                top_tool_used TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                feedback_type TEXT,
                message TEXT,
                rating INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
            )
        """)

        # A/B test results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ab_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                variant_a TEXT,
                variant_b TEXT,
                metric TEXT,
                variant_a_value FLOAT,
                variant_b_value FLOAT,
                winner TEXT,
                confidence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def log_session_start(self, session_id: str, user_id: str, company: str = "") -> bool:
        """Log new user session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_sessions (session_id, user_id, company)
                VALUES (?, ?, ?)
            """, (session_id, user_id, company))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error logging session: {e}")
            return False

    def log_onboarding_completion(self, session_id: str):
        """Log when user completes onboarding"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_sessions
            SET completed_onboarding = TRUE, last_activity = CURRENT_TIMESTAMP
            WHERE session_id = ?
        """, (session_id,))
        conn.commit()
        conn.close()

    def log_tool_usage(self, session_id: str, tool_name: str, category: str,
                      execution_time_ms: int = 0, result_quality: str = "good"):
        """Log tool usage event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tool_usage (session_id, tool_name, category, execution_time_ms, result_quality)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, tool_name, category, execution_time_ms, result_quality))

            cursor.execute("""
                UPDATE user_sessions
                SET tools_used = tools_used + 1, last_activity = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """, (session_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error logging tool usage: {e}")
            return False

    def log_export(self, session_id: str, export_format: str):
        """Log export event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_sessions
            SET exports_created = exports_created + 1
            WHERE session_id = ?
        """, (session_id,))
        conn.commit()
        conn.close()

    def log_share(self, session_id: str):
        """Log share event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_sessions
            SET shares_created = shares_created + 1
            WHERE session_id = ?
        """, (session_id,))
        conn.commit()
        conn.close()

    def log_conversion(self, session_id: str, plan: str, mrr: float):
        """Log paid conversion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_sessions
            SET plan = ?, mrr = ?, paid_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
        """, (plan, mrr, session_id))
        conn.commit()
        conn.close()

    def log_feedback(self, session_id: str, feedback_type: str, message: str, rating: int = 0):
        """Log user feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_feedback (session_id, feedback_type, message, rating)
            VALUES (?, ?, ?, ?)
        """, (session_id, feedback_type, message, rating))
        conn.commit()
        conn.close()

    def get_daily_metrics(self, days_back: int = 7) -> List[Dict]:
        """Get daily metrics for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        start_date = (datetime.now() - timedelta(days=days_back)).date()

        cursor.execute("""
            SELECT * FROM daily_metrics
            WHERE date >= ?
            ORDER BY date DESC
        """, (str(start_date),))

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        return [dict(zip(columns, row)) for row in rows]

    def calculate_daily_metrics(self, date: str = None) -> DailyMetrics:
        """Calculate daily metrics for a specific date"""
        if date is None:
            date = datetime.now().date().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # New signups today
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions
            WHERE DATE(created_at) = ?
        """, (date,))
        new_signups = cursor.fetchone()[0]

        # Onboarding completion rate
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions WHERE completed_onboarding = TRUE AND DATE(created_at) = ?
        """, (date,))
        completed_today = cursor.fetchone()[0]
        onboarding_rate = (completed_today / new_signups * 100) if new_signups > 0 else 0

        # Average tools per user (all time)
        cursor.execute("""
            SELECT AVG(tools_used) FROM user_sessions
        """)
        avg_tools = cursor.fetchone()[0] or 0

        # Weekly active users
        cursor.execute("""
            SELECT COUNT(DISTINCT session_id) FROM user_sessions
            WHERE last_activity >= datetime('now', '-7 days')
        """)
        weekly_active = cursor.fetchone()[0]

        # Paid conversions today
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions
            WHERE plan != 'free' AND DATE(paid_at) = ?
        """, (date,))
        paid_today = cursor.fetchone()[0]

        # Current MRR
        cursor.execute("""
            SELECT COALESCE(SUM(mrr), 0) FROM user_sessions WHERE plan != 'free'
        """)
        mrr = cursor.fetchone()[0]

        # Export rate
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions WHERE exports_created > 0
        """)
        export_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM user_sessions")
        total_users = cursor.fetchone()[0]
        export_rate = (export_users / total_users * 100) if total_users > 0 else 0

        # Share rate
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions WHERE shares_created > 0
        """)
        share_users = cursor.fetchone()[0]
        share_rate = (share_users / total_users * 100) if total_users > 0 else 0

        # User satisfaction (from feedback)
        cursor.execute("""
            SELECT AVG(rating) FROM user_feedback
            WHERE rating > 0 AND DATE(created_at) >= datetime('now', '-7 days')
        """)
        satisfaction = cursor.fetchone()[0] or 0

        conn.close()

        return DailyMetrics(
            date=date,
            new_signups=new_signups,
            onboarding_completion_rate=round(onboarding_rate, 2),
            avg_tools_per_user=round(avg_tools, 2),
            weekly_active_users=weekly_active,
            paid_conversions=paid_today,
            mrr=round(mrr, 2),
            export_rate=round(export_rate, 2),
            share_rate=round(share_rate, 2),
            user_satisfaction=round(satisfaction, 2)
        )

    def get_top_tools(self, days: int = 7) -> List[Dict]:
        """Get most used tools"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tool_name, category, COUNT(*) as usage_count
            FROM tool_usage
            WHERE used_at >= datetime('now', ? || ' days')
            GROUP BY tool_name
            ORDER BY usage_count DESC
            LIMIT 10
        """, (f"-{days}",))

        rows = cursor.fetchall()
        conn.close()

        return [
            {"tool": row[0], "category": row[1], "uses": row[2]}
            for row in rows
        ]

    def get_cohort_retention(self, cohort_days: int = 7) -> Dict:
        """Get retention by cohort (users who return N days later)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                DATE(created_at) as cohort_date,
                COUNT(*) as cohort_size,
                SUM(CASE WHEN last_activity >= datetime(created_at, ? || ' days') THEN 1 ELSE 0 END) as day_n_retained
            FROM user_sessions
            GROUP BY DATE(created_at)
            ORDER BY cohort_date DESC
            LIMIT 7
        """, (f"+{cohort_days}",))

        rows = cursor.fetchall()
        conn.close()

        cohorts = {}
        for row in rows:
            retention_rate = (row[2] / row[1] * 100) if row[1] > 0 else 0
            cohorts[row[0]] = {
                "size": row[1],
                "retained": row[2],
                "retention_rate": round(retention_rate, 2)
            }

        return cohorts

    def get_funnel_analysis(self) -> Dict:
        """Get conversion funnel metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM user_sessions")
        total_signups = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE completed_onboarding = TRUE")
        completed_onboarding = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE tools_used >= 2")
        used_two_tools = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE tools_used >= 5")
        used_five_tools = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE exports_created > 0")
        exported = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE plan != 'free'")
        paid = cursor.fetchone()[0]

        conn.close()

        return {
            "signups": total_signups,
            "onboarding_completion": completed_onboarding,
            "onboarding_rate": round((completed_onboarding / total_signups * 100) if total_signups > 0 else 0, 2),
            "two_tools": used_two_tools,
            "two_tools_rate": round((used_two_tools / total_signups * 100) if total_signups > 0 else 0, 2),
            "five_tools": used_five_tools,
            "five_tools_rate": round((used_five_tools / total_signups * 100) if total_signups > 0 else 0, 2),
            "exports": exported,
            "export_rate": round((exported / total_signups * 100) if total_signups > 0 else 0, 2),
            "paid": paid,
            "conversion_rate": round((paid / total_signups * 100) if total_signups > 0 else 0, 2)
        }

    def log_ab_test_result(self, test_name: str, variant_a: str, variant_b: str,
                          metric: str, variant_a_value: float, variant_b_value: float,
                          confidence: float = 0.95):
        """Log A/B test results"""
        winner = "A" if variant_a_value > variant_b_value else "B"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ab_tests (test_name, variant_a, variant_b, metric, variant_a_value, variant_b_value, winner, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (test_name, variant_a, variant_b, metric, variant_a_value, variant_b_value, winner, confidence))
        conn.commit()
        conn.close()
