"""
Stripe Payment Integration for AI Business Tools SaaS
Handles subscriptions, billing, and payment processing
"""

import stripe
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from enum import Enum


class PlanType(Enum):
    """Subscription plan types"""
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"


class StripeIntegration:
    """Main Stripe integration handler"""

    # Pricing plans (update with your actual Stripe price IDs)
    PLANS = {
        PlanType.FREE: {
            "price_id": None,
            "amount": 0,
            "currency": "usd",
            "interval": None,
            "name": "Free",
            "description": "5 tools/month",
            "features": [
                "5 tools per month",
                "Basic features",
                "Community support"
            ]
        },
        PlanType.PRO: {
            "price_id": "price_pro_monthly",  # Replace with actual Stripe price ID
            "amount": 4900,  # $49.00 in cents
            "currency": "usd",
            "interval": "month",
            "name": "Pro",
            "description": "Unlimited tools + support",
            "features": [
                "Unlimited tool usage",
                "Export reports (PDF, Excel)",
                "5 team members",
                "Priority email support",
                "Custom branding"
            ]
        },
        PlanType.BUSINESS: {
            "price_id": "price_business_monthly",  # Replace with actual Stripe price ID
            "amount": 19900,  # $199.00 in cents
            "currency": "usd",
            "interval": "month",
            "name": "Business",
            "description": "API + White-label",
            "features": [
                "Everything in Pro",
                "Unlimited team members",
                "REST API access",
                "Webhook integration",
                "White-label branding",
                "SSO/SAML support",
                "Dedicated account manager",
                "99.9% SLA guarantee"
            ]
        }
    }

    def __init__(self, api_key: str = None):
        """
        Initialize Stripe integration

        Args:
            api_key: Stripe API key (sk_live_* or sk_test_*)
        """
        self.api_key = api_key or os.getenv('STRIPE_API_KEY')
        if self.api_key:
            stripe.api_key = self.api_key
        self.environment = "test" if "test" in self.api_key else "live" if self.api_key else "dev"

    # ==================== CUSTOMER MANAGEMENT ====================

    def create_customer(self, email: str, name: str = "", company: str = "") -> Optional[str]:
        """
        Create Stripe customer

        Args:
            email: Customer email
            name: Customer name
            company: Company name

        Returns:
            Stripe customer ID or None
        """
        if not self.api_key:
            print(f"[DEMO] Would create Stripe customer: {email}")
            return f"cus_demo_{email.split('@')[0]}"

        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                description=company,
                metadata={
                    "created_at": datetime.now().isoformat(),
                    "company": company
                }
            )
            return customer.id
        except stripe.error.StripeError as e:
            print(f"Error creating customer: {str(e)}")
            return None

    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """Get customer details"""
        if not self.api_key:
            return None

        try:
            customer = stripe.Customer.retrieve(customer_id)
            return {
                'id': customer.id,
                'email': customer.email,
                'name': customer.name,
                'created': customer.created,
                'balance': customer.balance
            }
        except stripe.error.StripeError as e:
            print(f"Error retrieving customer: {str(e)}")
            return None

    # ==================== SUBSCRIPTION MANAGEMENT ====================

    def create_subscription(self, customer_id: str, plan: PlanType,
                           trial_days: int = 0) -> Optional[Dict]:
        """
        Create subscription for customer

        Args:
            customer_id: Stripe customer ID
            plan: Plan type (FREE, PRO, BUSINESS)
            trial_days: Days of free trial (optional)

        Returns:
            Subscription details or None
        """
        if plan == PlanType.FREE:
            return {
                'id': f"sub_free_{customer_id}",
                'customer': customer_id,
                'plan': plan.value,
                'status': 'active',
                'amount': 0,
                'interval': None,
                'current_period_start': datetime.now().isoformat(),
                'current_period_end': None
            }

        if not self.api_key:
            print(f"[DEMO] Would create {plan.value} subscription for {customer_id}")
            return {
                'id': f"sub_{plan.value}_{customer_id}",
                'customer': customer_id,
                'plan': plan.value,
                'status': 'active',
                'amount': self.PLANS[plan]['amount'],
                'interval': self.PLANS[plan]['interval'],
                'current_period_start': datetime.now().isoformat(),
                'current_period_end': (datetime.now() + timedelta(days=30)).isoformat()
            }

        try:
            plan_config = self.PLANS[plan]
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'price': plan_config['price_id'],
                    }
                ],
                trial_period_days=trial_days if trial_days > 0 else None,
                metadata={
                    'plan': plan.value,
                    'created_at': datetime.now().isoformat()
                }
            )

            return self._format_subscription(subscription)

        except stripe.error.StripeError as e:
            print(f"Error creating subscription: {str(e)}")
            return None

    def cancel_subscription(self, subscription_id: str, at_period_end: bool = True) -> bool:
        """
        Cancel subscription

        Args:
            subscription_id: Stripe subscription ID
            at_period_end: If True, cancel at end of billing period; if False, cancel immediately

        Returns:
            True if successful
        """
        if not self.api_key:
            print(f"[DEMO] Would cancel subscription: {subscription_id}")
            return True

        try:
            if at_period_end:
                stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                stripe.Subscription.delete(subscription_id)
            return True
        except stripe.error.StripeError as e:
            print(f"Error canceling subscription: {str(e)}")
            return False

    def update_subscription(self, subscription_id: str, plan: PlanType) -> Optional[Dict]:
        """
        Update subscription to different plan

        Args:
            subscription_id: Current subscription ID
            plan: New plan type

        Returns:
            Updated subscription details or None
        """
        if not self.api_key:
            print(f"[DEMO] Would update subscription {subscription_id} to {plan.value}")
            return None

        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            new_price_id = self.PLANS[plan]['price_id']

            # Update the subscription
            subscription = stripe.Subscription.modify(
                subscription_id,
                items=[
                    {
                        'id': subscription['items'].data[0].id,
                        'price': new_price_id,
                    }
                ]
            )

            return self._format_subscription(subscription)

        except stripe.error.StripeError as e:
            print(f"Error updating subscription: {str(e)}")
            return None

    def get_subscription(self, subscription_id: str) -> Optional[Dict]:
        """Get subscription details"""
        if not self.api_key:
            return None

        try:
            sub = stripe.Subscription.retrieve(subscription_id)
            return self._format_subscription(sub)
        except stripe.error.StripeError as e:
            print(f"Error retrieving subscription: {str(e)}")
            return None

    def _format_subscription(self, sub) -> Dict:
        """Format Stripe subscription object"""
        return {
            'id': sub.id,
            'customer': sub.customer,
            'plan': sub.metadata.get('plan', 'unknown'),
            'status': sub.status,
            'amount': sub.items.data[0].price.unit_amount if sub.items.data else 0,
            'interval': sub.items.data[0].price.recurring.interval if sub.items.data else None,
            'current_period_start': sub.current_period_start,
            'current_period_end': sub.current_period_end,
            'cancel_at_period_end': sub.cancel_at_period_end
        }

    # ==================== PAYMENT PROCESSING ====================

    def create_checkout_session(self, customer_id: str, plan: PlanType,
                               success_url: str, cancel_url: str) -> Optional[str]:
        """
        Create Stripe Checkout session

        Args:
            customer_id: Stripe customer ID
            plan: Plan type to purchase
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel

        Returns:
            Checkout session URL or None
        """
        if not self.api_key:
            return f"{success_url}?session=demo"

        try:
            plan_config = self.PLANS[plan]

            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': plan_config['price_id'],
                        'quantity': 1,
                    }
                ],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'plan': plan.value
                }
            )

            return session.url

        except stripe.error.StripeError as e:
            print(f"Error creating checkout session: {str(e)}")
            return None

    def create_payment_intent(self, customer_id: str, amount: int,
                             currency: str = "usd", description: str = "") -> Optional[Dict]:
        """
        Create one-time payment intent

        Args:
            customer_id: Stripe customer ID
            amount: Amount in cents
            currency: Currency code
            description: Payment description

        Returns:
            Payment intent details or None
        """
        if not self.api_key:
            return {'id': f'pi_demo_{customer_id}', 'status': 'succeeded'}

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                customer=customer_id,
                description=description,
                metadata={'created_at': datetime.now().isoformat()}
            )

            return {
                'id': intent.id,
                'amount': intent.amount,
                'currency': intent.currency,
                'status': intent.status,
                'client_secret': intent.client_secret
            }

        except stripe.error.StripeError as e:
            print(f"Error creating payment intent: {str(e)}")
            return None

    # ==================== INVOICING ====================

    def get_customer_invoices(self, customer_id: str, limit: int = 10) -> List[Dict]:
        """Get customer invoices"""
        if not self.api_key:
            return []

        try:
            invoices = stripe.Invoice.list(
                customer=customer_id,
                limit=limit
            )

            return [
                {
                    'id': inv.id,
                    'amount': inv.amount_paid,
                    'status': inv.status,
                    'date': inv.created,
                    'pdf_url': inv.invoice_pdf,
                    'description': inv.description
                }
                for inv in invoices.data
            ]

        except stripe.error.StripeError as e:
            print(f"Error retrieving invoices: {str(e)}")
            return []

    # ==================== WEBHOOK HANDLING ====================

    def verify_webhook_signature(self, payload: str, signature: str, webhook_secret: str) -> bool:
        """
        Verify Stripe webhook signature

        Args:
            payload: Raw request body
            signature: Stripe signature header
            webhook_secret: Webhook secret from Stripe dashboard

        Returns:
            True if signature is valid
        """
        try:
            stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            return True
        except ValueError:
            print("Invalid payload")
            return False
        except stripe.error.SignatureVerificationError:
            print("Invalid signature")
            return False

    def handle_webhook_event(self, event_data: Dict) -> Optional[Dict]:
        """
        Handle Stripe webhook event

        Args:
            event_data: Webhook event data

        Returns:
            Processed event info or None
        """
        event_type = event_data.get('type')

        if event_type == 'customer.subscription.created':
            return self._handle_subscription_created(event_data)
        elif event_type == 'customer.subscription.updated':
            return self._handle_subscription_updated(event_data)
        elif event_type == 'customer.subscription.deleted':
            return self._handle_subscription_deleted(event_data)
        elif event_type == 'invoice.payment_succeeded':
            return self._handle_payment_succeeded(event_data)
        elif event_type == 'invoice.payment_failed':
            return self._handle_payment_failed(event_data)

        return None

    def _handle_subscription_created(self, event: Dict) -> Dict:
        """Handle subscription created event"""
        sub = event['data']['object']
        return {
            'action': 'subscription_created',
            'customer_id': sub['customer'],
            'subscription_id': sub['id'],
            'plan': sub['metadata'].get('plan', 'unknown'),
            'status': sub['status']
        }

    def _handle_subscription_updated(self, event: Dict) -> Dict:
        """Handle subscription updated event"""
        sub = event['data']['object']
        return {
            'action': 'subscription_updated',
            'customer_id': sub['customer'],
            'subscription_id': sub['id'],
            'plan': sub['metadata'].get('plan', 'unknown'),
            'cancel_at_period_end': sub['cancel_at_period_end']
        }

    def _handle_subscription_deleted(self, event: Dict) -> Dict:
        """Handle subscription deleted event"""
        sub = event['data']['object']
        return {
            'action': 'subscription_deleted',
            'customer_id': sub['customer'],
            'subscription_id': sub['id']
        }

    def _handle_payment_succeeded(self, event: Dict) -> Dict:
        """Handle payment succeeded event"""
        invoice = event['data']['object']
        return {
            'action': 'payment_succeeded',
            'customer_id': invoice['customer'],
            'invoice_id': invoice['id'],
            'amount': invoice['amount_paid'],
            'currency': invoice['currency']
        }

    def _handle_payment_failed(self, event: Dict) -> Dict:
        """Handle payment failed event"""
        invoice = event['data']['object']
        return {
            'action': 'payment_failed',
            'customer_id': invoice['customer'],
            'invoice_id': invoice['id'],
            'amount': invoice['amount_due'],
            'currency': invoice['currency']
        }

    # ==================== REPORTING ====================

    def get_subscription_stats(self) -> Dict:
        """Get subscription statistics"""
        if not self.api_key:
            return {
                'total_customers': 0,
                'active_subscriptions': 0,
                'mrr': 0,
                'churn_rate': 0,
                'avg_revenue_per_user': 0
            }

        try:
            # Get active subscriptions
            subs = stripe.Subscription.list(
                status='active',
                limit=100
            )

            total_amount = sum([
                sub.items.data[0].price.unit_amount
                for sub in subs.data
                if sub.items.data
            ])

            return {
                'total_customers': len(subs.data),
                'active_subscriptions': len(subs.data),
                'mrr': total_amount / 100,  # Convert cents to dollars
                'average_revenue_per_user': (total_amount / len(subs.data) / 100) if subs.data else 0
            }

        except stripe.error.StripeError as e:
            print(f"Error getting stats: {str(e)}")
            return {}

    # ==================== PLAN INFORMATION ====================

    @staticmethod
    def get_plans() -> Dict:
        """Get all available plans"""
        return StripeIntegration.PLANS

    @staticmethod
    def get_plan_details(plan: PlanType) -> Dict:
        """Get specific plan details"""
        return StripeIntegration.PLANS.get(plan)

    @staticmethod
    def format_price(cents: int) -> str:
        """Format price in cents to string"""
        return f"${cents / 100:.2f}"


# ==================== DEMO / SETUP ====================

def setup_stripe_environment():
    """Setup Stripe test environment"""
    test_key = os.getenv('STRIPE_API_KEY_TEST')
    if not test_key:
        print("WARNING: STRIPE_API_KEY_TEST not set. Running in demo mode.")
        print("To enable payments:")
        print("  1. Go to https://stripe.com/account/apikeys")
        print("  2. Copy your Secret key (sk_test_*)")
        print("  3. Set environment variable: STRIPE_API_KEY_TEST=sk_test_...")
        return None
    return test_key


if __name__ == "__main__":
    print("=" * 70)
    print("STRIPE PAYMENT INTEGRATION - SETUP GUIDE")
    print("=" * 70)
    print()

    # Check environment
    api_key = setup_stripe_environment()

    # Initialize Stripe
    stripe_client = StripeIntegration(api_key)
    print(f"[✓] Stripe integration initialized ({stripe_client.environment} mode)")
    print()

    # Show plans
    print("AVAILABLE PLANS:")
    for plan_type, config in stripe_client.get_plans().items():
        if plan_type != PlanType.FREE:
            print(f"  - {config['name']}: {stripe_client.format_price(config['amount'])}/month")
            print(f"    → {config['description']}")
    print()

    print("USAGE EXAMPLES:")
    print("""
    from stripe_integration import StripeIntegration, PlanType

    # Initialize
    stripe_client = StripeIntegration()

    # Create customer
    customer_id = stripe_client.create_customer(
        "user@example.com",
        "John Smith",
        "Acme Inc"
    )

    # Create subscription
    sub = stripe_client.create_subscription(
        customer_id,
        PlanType.PRO,
        trial_days=7
    )

    # Create checkout session
    checkout_url = stripe_client.create_checkout_session(
        customer_id,
        PlanType.PRO,
        "https://yourapp.com/success",
        "https://yourapp.com/cancel"
    )

    # Get subscription status
    sub_info = stripe_client.get_subscription(sub['id'])

    # Cancel subscription
    stripe_client.cancel_subscription(sub['id'], at_period_end=True)

    # Get subscription stats
    stats = stripe_client.get_subscription_stats()
    """)
    print()

    print("WEBHOOK SETUP:")
    print("""
    1. Go to https://dashboard.stripe.com/webhooks
    2. Add endpoint: https://yourapp.com/webhook
    3. Select events:
       - customer.subscription.created
       - customer.subscription.updated
       - customer.subscription.deleted
       - invoice.payment_succeeded
       - invoice.payment_failed
    4. Copy signing secret
    5. Set: STRIPE_WEBHOOK_SECRET=whsec_...
    """)
