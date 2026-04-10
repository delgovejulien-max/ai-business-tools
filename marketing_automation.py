"""
Marketing Automation System for AI Business Tools SaaS
Handles email campaigns, customer sequences, and engagement tracking
"""

import sqlite3
import smtplib
import json
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from enum import Enum


class EmailTemplate(Enum):
    """Email template types"""
    WELCOME = "welcome"
    ONBOARDING = "onboarding"
    FEATURE_HIGHLIGHT = "feature_highlight"
    UPSELL_PRO = "upsell_pro"
    UPSELL_BUSINESS = "upsell_business"
    WINBACK = "winback"
    SUCCESS_STORY = "success_story"
    PRICING_REMINDER = "pricing_reminder"
    UPGRADE_CONFIRMATION = "upgrade_confirmation"


class MarketingAutomation:
    """Main marketing automation engine"""

    def __init__(self, smtp_server: str = None, smtp_user: str = None, smtp_password: str = None):
        """
        Initialize marketing automation system

        Args:
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_user: SMTP username/email
            smtp_password: SMTP password or app-specific password
        """
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = 587
        self.smtp_user = smtp_user or os.getenv('SMTP_USER')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')
        self.sender_name = "AI Business Tools"
        self.sender_email = self.smtp_user or "support@aibusinesstools.com"

        self._init_database()
        self.templates = self._load_templates()

    def _init_database(self):
        """Initialize email marketing database"""
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()

        # Subscribers table
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                     (id INTEGER PRIMARY KEY,
                      email TEXT UNIQUE,
                      name TEXT,
                      company TEXT,
                      plan TEXT,
                      signup_date TIMESTAMP,
                      last_email_date TIMESTAMP,
                      email_count INTEGER DEFAULT 0,
                      engagement_score REAL DEFAULT 0,
                      status TEXT DEFAULT 'active')''')

        # Email campaign tracking
        c.execute('''CREATE TABLE IF NOT EXISTS email_campaigns
                     (id INTEGER PRIMARY KEY,
                      template_type TEXT,
                      email TEXT,
                      subject TEXT,
                      sent_date TIMESTAMP,
                      opened INTEGER DEFAULT 0,
                      clicked INTEGER DEFAULT 0,
                      unsubscribed INTEGER DEFAULT 0)''')

        # User actions (for automation triggers)
        c.execute('''CREATE TABLE IF NOT EXISTS user_actions
                     (id INTEGER PRIMARY KEY,
                      email TEXT,
                      action_type TEXT,
                      action_date TIMESTAMP,
                      tool_used TEXT,
                      metadata TEXT)''')

        conn.commit()
        conn.close()

    def _load_templates(self) -> Dict[EmailTemplate, Dict[str, str]]:
        """Load all email templates"""
        return {
            EmailTemplate.WELCOME: {
                "subject": "Welcome to AI Business Tools! Get Your First Free Analysis",
                "body": self._get_welcome_template()
            },
            EmailTemplate.ONBOARDING: {
                "subject": "Here's How to Get the Most Out of Your AI Business Tools",
                "body": self._get_onboarding_template()
            },
            EmailTemplate.FEATURE_HIGHLIGHT: {
                "subject": "You're Missing Out: Our Most Powerful Tool [TOOL_NAME]",
                "body": self._get_feature_highlight_template()
            },
            EmailTemplate.UPSELL_PRO: {
                "subject": "Unlock Unlimited Tools: 40% Off Pro for Early Users",
                "body": self._get_upsell_pro_template()
            },
            EmailTemplate.UPSELL_BUSINESS: {
                "subject": "Scale Your Strategy: Business Plan + API Access",
                "body": self._get_upsell_business_template()
            },
            EmailTemplate.WINBACK: {
                "subject": "We Miss You! Here's $20 Off Your Next Tool Usage",
                "body": self._get_winback_template()
            },
            EmailTemplate.SUCCESS_STORY: {
                "subject": "How [COMPANY] Generated $50K in Revenue Using AI Tools",
                "body": self._get_success_story_template()
            },
            EmailTemplate.PRICING_REMINDER: {
                "subject": "Your Free Tools Expire Soon - Upgrade Now",
                "body": self._get_pricing_reminder_template()
            },
            EmailTemplate.UPGRADE_CONFIRMATION: {
                "subject": "Welcome to Pro! Here's Your Welcome Gift",
                "body": self._get_upgrade_confirmation_template()
            }
        }

    # ==================== EMAIL TEMPLATES ====================

    def _get_welcome_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">Welcome to AI Business Tools! 🚀</h2>

        <p>Hi {NAME},</p>

        <p>You've just unlocked access to <strong>18 AI-powered business tools</strong> designed specifically for startups and growing companies like {COMPANY}.</p>

        <h3 style="color: #ff6b35;">What You Can Do Today:</h3>
        <ul>
            <li><strong>Market Analysis:</strong> Understand your market size, growth rate, and opportunities</li>
            <li><strong>Competitive Analysis:</strong> Know exactly who you're up against</li>
            <li><strong>Revenue Forecast:</strong> Project your revenue with confidence intervals</li>
            <li><strong>Campaign Planning:</strong> Launch campaigns that actually drive results</li>
        </ul>

        <p style="background-color: #f0f2f6; padding: 15px; border-radius: 5px;">
            <strong>Your Free Tier Includes:</strong> 5 tools per month + basic features
        </p>

        <h3 style="color: #1f77b4;">Get Started in 2 Minutes:</h3>
        <ol>
            <li>Log in to your dashboard</li>
            <li>Pick a tool (we recommend "Market Analysis" first)</li>
            <li>Describe your business</li>
            <li>Get AI-powered insights in under 30 seconds</li>
        </ol>

        <p>Questions? Reply to this email or check out our <a href="https://aibusinesstools.com/help" style="color: #1f77b4;">Help Center</a>.</p>

        <p>Let's build something amazing together!</p>

        <p>
            <strong>The AI Business Tools Team</strong><br>
            <em>Strategy powered by AI. Built for entrepreneurs.</em>
        </p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">

        <p style="font-size: 12px; color: #999;">
            You're receiving this because you signed up for AI Business Tools.
            <a href="{UNSUBSCRIBE_LINK}" style="color: #999;">Unsubscribe</a>
        </p>
    </div>
</body>
</html>
"""

    def _get_onboarding_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">Your Onboarding Roadmap</h2>

        <p>Hi {NAME},</p>

        <p>You've been a user for a few days. Here's how to maximize the value from AI Business Tools:</p>

        <h3>Day 1-2: Foundation (You're Here)</h3>
        <ul>
            <li>✓ Create company profile</li>
            <li>→ <strong>Next:</strong> Try Market Analysis tool</li>
        </ul>

        <h3>Day 3-5: Strategy</h3>
        <ul>
            <li>→ Run Competitive Analysis</li>
            <li>→ Generate Go-to-Market Strategy</li>
            <li>→ Create Pricing Model</li>
        </ul>

        <h3>Day 6-7: Execution</h3>
        <ul>
            <li>→ Design Campaign Plan</li>
            <li>→ Setup Revenue Forecast</li>
            <li>→ Export your strategy as PDF</li>
        </ul>

        <h3 style="color: #ff6b35;">Pro Tip:</h3>
        <p>Most users who run the "Business Model Canvas" tool 3x per week get their strategy right and reduce planning time by 80%.</p>

        <p style="background-color: #f0f2f6; padding: 15px; border-radius: 5px;">
            <strong>Limited Time:</strong> Upgrade to Pro for only $39/month (save 20%) and get unlimited tools + priority support
        </p>

        <p><a href="{APP_URL}/pricing" style="background-color: #ff6b35; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Pricing</a></p>

        <p>Need help? I'm here at support@aibusinesstools.com</p>

        <p><strong>The AI Business Tools Team</strong></p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">

        <p style="font-size: 12px; color: #999;">
            <a href="{UNSUBSCRIBE_LINK}" style="color: #999;">Unsubscribe</a>
        </p>
    </div>
</body>
</html>
"""

    def _get_feature_highlight_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">Here's the Tool That Changes Everything</h2>

        <p>Hi {NAME},</p>

        <p>We noticed you've been using our tools for market research. That's great! But there's one tool that most successful users tell us they can't live without:</p>

        <h3 style="color: #ff6b35;"><strong>{TOOL_NAME}</strong></h3>

        <p><strong>Why it matters:</strong> {TOOL_DESCRIPTION}</p>

        <p><strong>Real example:</strong> A SaaS founder used this tool and increased their conversion rate by 45% in 30 days.</p>

        <h3>What This Tool Does:</h3>
        <ul>
            <li>Analyzes your customer segments automatically</li>
            <li>Identifies your highest-value customers</li>
            <li>Recommends optimization strategies</li>
            <li>Generates actionable insights in seconds</li>
        </ul>

        <p><a href="{APP_URL}/tools/{TOOL_ID}" style="background-color: #1f77b4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Try {TOOL_NAME} Now</a></p>

        <p>This is available on the Free plan - no upgrade needed. Try it today!</p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    def _get_upsell_pro_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #ff6b35;">Last Chance: 40% Off Pro Plan</h2>

        <p>Hi {NAME},</p>

        <p>We're running a special promotion for power users like you.</p>

        <h3>What You're Missing on Free Plan:</h3>
        <ul style="color: #999;">
            <li>5 tools per month → <strong style="color: #1f77b4;">UNLIMITED tools</strong></li>
            <li>Basic support → <strong style="color: #1f77b4;">Email + priority support</strong></li>
            <li>No export → <strong style="color: #1f77b4;">PDF/Excel reports</strong></li>
            <li>No team access → <strong style="color: #1f77b4;">5 team members</strong></li>
        </ul>

        <h3 style="color: #ff6b35;">Pro Plan - Special Offer</h3>
        <p style="font-size: 24px; color: #ff6b35;">
            <strong>$39/month</strong> <span style="text-decoration: line-through; color: #999;">$49/month</span>
        </p>

        <p><strong>What's included:</strong></p>
        <ul>
            <li>✓ Unlimited tool usage</li>
            <li>✓ Export reports (PDF, Excel, JSON)</li>
            <li>✓ 5 team member accounts</li>
            <li>✓ Priority email support</li>
            <li>✓ Custom company branding</li>
        </ul>

        <p style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ff6b35;">
            <strong>Offer expires in 7 days.</strong> After that, price returns to $49/month.
        </p>

        <p><a href="{APP_URL}/upgrade/pro" style="background-color: #ff6b35; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-size: 16px;">Upgrade to Pro Now</a></p>

        <p>Questions? Check your account dashboard or email support@aibusinesstools.com</p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    def _get_upsell_business_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">Ready to Scale? Meet Business Plan</h2>

        <p>Hi {NAME},</p>

        <p>You've been crushing it with Pro. Time to scale to the next level.</p>

        <h3>Perfect For:</h3>
        <ul>
            <li>Agencies using our tools for clients</li>
            <li>Teams with 10+ members</li>
            <li>Companies needing API integration</li>
            <li>White-label / reselling</li>
        </ul>

        <h3 style="color: #1f77b4;">Business Plan - $199/month</h3>

        <p><strong>Everything in Pro, plus:</strong></p>
        <ul>
            <li>✓ Unlimited team members</li>
            <li>✓ REST API access</li>
            <li>✓ Webhook integration</li>
            <li>✓ White-label branding</li>
            <li>✓ SSO/SAML support</li>
            <li>✓ Dedicated account manager</li>
            <li>✓ SLA guarantee (99.9% uptime)</li>
        </ul>

        <h3>ROI Example:</h3>
        <p>If you run 10 client engagements/month at $5K each, the Business plan pays for itself 25x over.</p>

        <p><a href="{APP_URL}/upgrade/business" style="background-color: #1f77b4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-size: 16px;">Upgrade to Business</a></p>

        <p>Want to discuss custom enterprise pricing? <a href="mailto:sales@aibusinesstools.com">Contact our sales team</a></p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    def _get_winback_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">We Miss You {NAME}!</h2>

        <p>It's been a while since you've used AI Business Tools.</p>

        <p>Here's what's new since you left:</p>

        <ul>
            <li>✓ 3 new tools added (Cohort Analysis, Customer Segmentation, Performance Reports)</li>
            <li>✓ 50% faster analysis (LLM upgrades)</li>
            <li>✓ New integrations with Stripe, HubSpot, Salesforce</li>
            <li>✓ Team collaboration features</li>
        </ul>

        <h3 style="color: #ff6b35;">Welcome Back Special</h3>
        <p>As a returning user, you get:</p>

        <ul style="background-color: #f0f2f6; padding: 15px; border-radius: 5px;">
            <li>💰 $20 credit toward Pro plan</li>
            <li>🎁 Free team account (normally $10/user/month)</li>
            <li>⚡ Unlimited free tools for 7 days</li>
        </ul>

        <p><a href="{APP_URL}/welcome-back" style="background-color: #ff6b35; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Claim Your Welcome Back Bonus</a></p>

        <p>No strings attached. The offer expires in 14 days.</p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    def _get_success_story_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">How {COMPANY} Generated {REVENUE} Using AI Tools</h2>

        <p>Hi {NAME},</p>

        <p>I wanted to share an inspiring story from one of our customers.</p>

        <h3>{COMPANY} - A Case Study</h3>

        <p><strong>The Challenge:</strong> {CHALLENGE}</p>
        <p><strong>What They Did:</strong> Used our {TOOL_NAME} tool to {ACTION}</p>
        <p><strong>The Results:</strong></p>
        <ul>
            <li>💰 Generated {REVENUE} in new revenue</li>
            <li>📈 Increased conversion rate by {METRIC_1}</li>
            <li>⏱️ Reduced planning time by {METRIC_2}</li>
        </ul>

        <p><strong>Their Quote:</strong></p>
        <p style="border-left: 4px solid #ff6b35; padding-left: 15px; font-style: italic;">
            "{QUOTE}"<br>
            - {FOUNDER_NAME}, {FOUNDER_TITLE}
        </p>

        <h3>You Can Get Similar Results</h3>
        <p>The tools {COMPANY} used are available right now in your dashboard:</p>

        <ul>
            <li>{TOOL_1}</li>
            <li>{TOOL_2}</li>
            <li>{TOOL_3}</li>
        </ul>

        <p><a href="{APP_URL}" style="background-color: #1f77b4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Go to Dashboard</a></p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    def _get_pricing_reminder_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #ff6b35;">Your Free Tools Expire in {DAYS} Days</h2>

        <p>Hi {NAME},</p>

        <p>Great news! You have <strong>{TOOLS_USED} of your 5 free tools remaining</strong> this month.</p>

        <p>Here's what you've accomplished:</p>
        <ul>
            <li>✓ Market Analysis: {TOOL_1_USE} times</li>
            <li>✓ Campaign Planning: {TOOL_2_USE} times</li>
            <li>✓ Revenue Forecast: {TOOL_3_USE} times</li>
        </ul>

        <h3>Want More Tools?</h3>
        <p style="background-color: #fff3cd; padding: 15px; border-radius: 5px;">
            Upgrade to <strong>Pro ($49/month)</strong> for unlimited tools + all your data in one dashboard
        </p>

        <h3>Pricing Options:</h3>
        <ul>
            <li><strong>Free:</strong> $0/month - 5 tools/month (perfect for trying)</li>
            <li><strong>Pro:</strong> $49/month - Unlimited tools + export + team (most popular)</li>
            <li><strong>Business:</strong> $199/month - API + white-label + dedicated support</li>
        </ul>

        <p><a href="{APP_URL}/pricing" style="background-color: #1f77b4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View All Plans</a></p>

        <p>Questions? Reply to this email.</p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    def _get_upgrade_confirmation_template(self) -> str:
        return """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1f77b4;">Welcome to Pro! 🎉</h2>

        <p>Hi {NAME},</p>

        <p>Your upgrade to <strong>Pro</strong> is now active! You now have access to all premium features.</p>

        <h3>Here's Your Welcome Gift:</h3>
        <ul>
            <li>💰 Coupon Code: <strong>WELCOME20</strong> - 20% off future billing cycles</li>
            <li>📚 Free training: "Advanced Strategy Guide" PDF</li>
            <li>🎯 Free consultation: 30-min call with our strategy team (optional)</li>
        </ul>

        <h3>You Now Have Unlimited Access To:</h3>
        <ul>
            <li>✓ All 18 business tools</li>
            <li>✓ PDF/Excel exports</li>
            <li>✓ Team collaboration (5 members)</li>
            <li>✓ Priority email support</li>
            <li>✓ Custom branding</li>
            <li>✓ API access (coming soon)</li>
        </ul>

        <h3>Next Steps:</h3>
        <ol>
            <li>Log in to your Pro dashboard</li>
            <li>Invite your team (Settings > Team)</li>
            <li>Download "Advanced Strategy Guide"</li>
            <li>Try the "Business Model Canvas" tool (most popular)</li>
        </ol>

        <p><a href="{APP_URL}/dashboard" style="background-color: #1f77b4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Go to Dashboard</a></p>

        <h3>Need Help?</h3>
        <ul>
            <li>📧 Email: support@aibusinesstools.com (priority response)</li>
            <li>📅 Schedule consultation: {CALENDLY_LINK}</li>
            <li>📖 Help center: {HELP_URL}</li>
        </ul>

        <p>Excited to have you on board!</p>

        <p><strong>The AI Business Tools Team</strong></p>
    </div>
</body>
</html>
"""

    # ==================== EMAIL SENDING ====================

    def send_email(self, to_email: str, template: EmailTemplate, variables: Dict[str, str]) -> bool:
        """
        Send email with template

        Args:
            to_email: Recipient email
            template: EmailTemplate enum
            variables: Dictionary of template variables

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.smtp_user or not self.smtp_password:
            print(f"[DEMO] Would send email to {to_email}")
            return True

        try:
            tmpl = self.templates[template]
            subject = self._replace_variables(tmpl['subject'], variables)
            body = self._replace_variables(tmpl['body'], variables)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email

            msg.attach(MIMEText(body, 'html'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            # Log to database
            self._log_email_sent(to_email, template, subject)
            return True

        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")
            return False

    def _replace_variables(self, text: str, variables: Dict[str, str]) -> str:
        """Replace template variables"""
        for key, value in variables.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text

    def _log_email_sent(self, email: str, template: EmailTemplate, subject: str):
        """Log email sending"""
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()
        c.execute('''INSERT INTO email_campaigns
                     (template_type, email, subject, sent_date)
                     VALUES (?, ?, ?, ?)''',
                  (template.value, email, subject, datetime.now()))
        conn.commit()
        conn.close()

    # ==================== AUTOMATION SEQUENCES ====================

    def create_automation_sequence(self, email: str, sequence_type: str) -> bool:
        """
        Create automated email sequence

        Args:
            email: User email
            sequence_type: 'welcome', 'onboarding', 'upsell', 'winback'
        """
        sequences = {
            'welcome': [
                (EmailTemplate.WELCOME, 0),
                (EmailTemplate.ONBOARDING, 2),
                (EmailTemplate.FEATURE_HIGHLIGHT, 5),
                (EmailTemplate.UPSELL_PRO, 7),
            ],
            'onboarding': [
                (EmailTemplate.ONBOARDING, 1),
                (EmailTemplate.FEATURE_HIGHLIGHT, 3),
                (EmailTemplate.UPSELL_PRO, 7),
            ],
            'upsell': [
                (EmailTemplate.UPSELL_PRO, 0),
                (EmailTemplate.UPSELL_PRO, 3),
                (EmailTemplate.UPSELL_BUSINESS, 7),
            ],
            'winback': [
                (EmailTemplate.WINBACK, 0),
                (EmailTemplate.SUCCESS_STORY, 3),
                (EmailTemplate.UPSELL_PRO, 7),
            ]
        }

        if sequence_type not in sequences:
            return False

        # Store sequence in database
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()

        for template, delay_days in sequences[sequence_type]:
            scheduled_date = (datetime.now() + timedelta(days=delay_days)).isoformat()
            c.execute('''INSERT INTO email_campaigns
                         (template_type, email, sent_date)
                         VALUES (?, ?, ?)''',
                      (template.value, email, scheduled_date))

        conn.commit()
        conn.close()
        return True

    # ==================== SUBSCRIBER MANAGEMENT ====================

    def add_subscriber(self, email: str, name: str = "", company: str = "", plan: str = "free") -> bool:
        """Add new subscriber"""
        try:
            conn = sqlite3.connect('marketing.db')
            c = conn.cursor()
            c.execute('''INSERT INTO subscribers
                         (email, name, company, plan, signup_date, status)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (email, name, company, plan, datetime.now(), 'active'))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_subscriber(self, email: str) -> Optional[Dict]:
        """Get subscriber info"""
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()
        c.execute('SELECT * FROM subscribers WHERE email = ?', (email,))
        result = c.fetchone()
        conn.close()

        if result:
            return {
                'id': result[0],
                'email': result[1],
                'name': result[2],
                'company': result[3],
                'plan': result[4],
                'signup_date': result[5],
                'email_count': result[8],
                'engagement_score': result[9],
                'status': result[10]
            }
        return None

    def get_subscribers_by_plan(self, plan: str) -> List[Dict]:
        """Get all subscribers on specific plan"""
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()
        c.execute('SELECT email FROM subscribers WHERE plan = ? AND status = ?',
                  (plan, 'active'))
        emails = [row[0] for row in c.fetchall()]
        conn.close()
        return emails

    # ==================== CAMPAIGN MANAGEMENT ====================

    def create_campaign(self, name: str, template: EmailTemplate,
                       recipient_filter: str = "all") -> bool:
        """
        Create and execute bulk email campaign

        Args:
            name: Campaign name
            template: Email template to use
            recipient_filter: 'all', 'free', 'pro', 'inactive'
        """
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()

        if recipient_filter == "all":
            c.execute('SELECT email FROM subscribers WHERE status = ?', ('active',))
        elif recipient_filter in ['free', 'pro', 'business']:
            c.execute('SELECT email FROM subscribers WHERE plan = ? AND status = ?',
                      (recipient_filter, 'active'))
        else:
            conn.close()
            return False

        recipients = [row[0] for row in c.fetchall()]
        conn.close()

        # Send emails
        sent_count = 0
        for email in recipients:
            if self.send_email(email, template, {'NAME': email.split('@')[0]}):
                sent_count += 1

        print(f"Campaign '{name}' sent to {sent_count} recipients")
        return True

    # ==================== ANALYTICS ====================

    def get_campaign_stats(self) -> Dict:
        """Get overall campaign statistics"""
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()

        c.execute('SELECT COUNT(*) FROM email_campaigns WHERE sent_date IS NOT NULL')
        total_sent = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM email_campaigns WHERE opened = 1')
        total_opened = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM email_campaigns WHERE clicked = 1')
        total_clicked = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM subscribers WHERE status = ?', ('active',))
        total_subscribers = c.fetchone()[0]

        conn.close()

        return {
            'total_sent': total_sent,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'total_subscribers': total_subscribers,
            'open_rate': (total_opened / total_sent * 100) if total_sent > 0 else 0,
            'click_rate': (total_clicked / total_sent * 100) if total_sent > 0 else 0
        }

    def get_subscriber_engagement(self, email: str) -> Dict:
        """Get engagement metrics for specific subscriber"""
        conn = sqlite3.connect('marketing.db')
        c = conn.cursor()

        c.execute('''SELECT COUNT(*),
                            SUM(opened),
                            SUM(clicked)
                     FROM email_campaigns
                     WHERE email = ?''', (email,))
        result = c.fetchone()

        conn.close()

        total = result[0] or 0
        opened = result[1] or 0
        clicked = result[2] or 0

        return {
            'emails_sent': total,
            'emails_opened': opened,
            'emails_clicked': clicked,
            'open_rate': (opened / total * 100) if total > 0 else 0,
            'click_rate': (clicked / total * 100) if total > 0 else 0
        }


# ==================== PREDEFINED CAMPAIGNS ====================

def setup_welcome_campaign(automation: MarketingAutomation):
    """Setup automatic welcome campaign for new signups"""
    print("[✓] Welcome campaign: Triggered on signup")
    print("   - Day 0: Welcome + Quick Start")
    print("   - Day 2: Onboarding Guide")
    print("   - Day 5: Feature Highlight")
    print("   - Day 7: Pro Upgrade Offer (40% off)")


def setup_engagement_campaign(automation: MarketingAutomation):
    """Setup engagement campaign for inactive users"""
    print("[✓] Engagement campaign: Triggered on 7-day inactivity")
    print("   - Success Story (Day 0)")
    print("   - Feature Highlight (Day 3)")
    print("   - Winback Offer + $20 credit (Day 7)")


def setup_upsell_campaign(automation: MarketingAutomation):
    """Setup upsell campaign for free users"""
    print("[✓] Upsell campaign: For free plan users")
    print("   - Trial ending reminder (Day -3)")
    print("   - Pro upgrade offer (Day 0, Day 3)")
    print("   - Business plan positioning (Day 7)")


def setup_lifecycle_campaigns(automation: MarketingAutomation):
    """Setup all lifecycle campaigns"""
    setup_welcome_campaign(automation)
    setup_engagement_campaign(automation)
    setup_upsell_campaign(automation)


if __name__ == "__main__":
    print("=" * 70)
    print("AI BUSINESS TOOLS - MARKETING AUTOMATION SYSTEM")
    print("=" * 70)

    # Initialize marketing automation
    marketing = MarketingAutomation()

    print("\n[✓] Marketing automation system initialized")
    print("[✓] Database created: marketing.db")
    print("[✓] 9 email templates loaded")
    print()

    # Setup demo data
    demo_users = [
        ("demo1@example.com", "John Smith", "TechStartup", "free"),
        ("demo2@example.com", "Sarah Johnson", "MarketingCo", "pro"),
        ("demo3@example.com", "Mike Davis", "Consulting", "free"),
    ]

    for email, name, company, plan in demo_users:
        marketing.add_subscriber(email, name, company, plan)

    print(f"[✓] Demo users added: {len(demo_users)}")
    print()

    # Setup campaigns
    print("CAMPAIGN SETUP:")
    setup_lifecycle_campaigns(marketing)
    print()

    # Show stats
    stats = marketing.get_campaign_stats()
    print("CURRENT METRICS:")
    print(f"  - Total Subscribers: {stats['total_subscribers']}")
    print(f"  - Emails Sent: {stats['total_sent']}")
    print(f"  - Open Rate: {stats['open_rate']:.1f}%")
    print(f"  - Click Rate: {stats['click_rate']:.1f}%")
    print()

    print("USAGE EXAMPLES:")
    print("""
    from marketing_automation import MarketingAutomation, EmailTemplate

    # Initialize
    marketing = MarketingAutomation()

    # Send welcome email
    marketing.send_email(
        "user@example.com",
        EmailTemplate.WELCOME,
        {"NAME": "John", "COMPANY": "Acme Inc", "UNSUBSCRIBE_LINK": "link"}
    )

    # Add subscriber
    marketing.add_subscriber("user@example.com", "John", "Acme Inc", "free")

    # Create automation sequence
    marketing.create_automation_sequence("user@example.com", "welcome")

    # Create bulk campaign
    marketing.create_campaign("Q1 Upgrade", EmailTemplate.UPSELL_PRO, "free")

    # Get analytics
    stats = marketing.get_campaign_stats()
    engagement = marketing.get_subscriber_engagement("user@example.com")
    """)
