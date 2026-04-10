# Weekly Improvement Ritual
## 90 Minutes to Better Product

**Time Allocation:** Monday 9:00-10:30 AM  
**Output:** 1 validated improvement shipped by Friday

---

## THE RITUAL (90 minutes)

### Segment 1: MEASURE (20 minutes)
**9:00 AM - 9:20 AM**

Pull the numbers:
```python
from metrics_tracker import MetricsDatabase

db = MetricsDatabase()

# Last week's metrics
metrics = db.calculate_daily_metrics()
funnel = db.get_funnel_analysis()
top_tools = db.get_top_tools(days=7)
retention = db.get_cohort_retention()

print(f"Signups: {metrics.new_signups}")
print(f"Onboarding: {metrics.onboarding_completion_rate}%")
print(f"Tools/user: {metrics.avg_tools_per_user}")
print(f"Weekly active: {metrics.weekly_active_users}")
print(f"MRR: ${metrics.mrr}")
print(f"Paid conversions: {funnel['conversion_rate']}%")
```

**Fill in dashboard:**
```
LAST WEEK RESULTS:

Signups:               ___ (target: 20+ → 100+)
Onboarding rate:       __% (target: 50%)
Tools/user:            ___ (target: 3+)
Weekly active:         __% (target: 30%)
Exports created:       ___ (target: 50%+)
Paid conversions:      ___ (target: 5%)
MRR:                   $___ (target: +20% growth)
User satisfaction:     ___ (target: 4.5+/5)

Biggest blocker:
- If onboarding is low (< 50%), that's the blocker
- If tools/user is low (< 3), that's the blocker
- If weekly active is low (< 30%), that's the blocker
- If paid conversions low (< 5%), that's the blocker
```

**Top 3 insights:**
1. What worked well?
2. What didn't work?
3. What surprised you?

---

### Segment 2: ROOT CAUSE (25 minutes)
**9:20 AM - 9:45 AM**

For your #1 blocker:

**If Onboarding Rate < 50%:**
```
Ask users: "Why didn't you complete the form?"
├─ Form too long?
├─ Results too slow?
├─ Didn't understand the question?
├─ Results not impressive enough?
└─ Technical issue?

Check data:
├─ What % drop at field 1 vs 2 vs 3?
├─ What % wait > 5 seconds and leave?
├─ What do their market analysis results look like?
└─ Any errors in logs?
```

**If Tools/User < 3:**
```
Why aren't users trying 2nd tool?
├─ Dashboard not recommending it?
├─ Hard to find other tools?
├─ 1st tool result not satisfying?
├─ Don't understand what tools do?
└─ Want to come back later?

Check:
├─ What % see dashboard after tool 1?
├─ What % click "next tool" button?
├─ Which tool do they try 2nd?
└─ How many try tool 2 same session vs later?
```

**If Weekly Active < 30%:**
```
Why don't users return?
├─ Strategy not clear what to do next?
├─ Forgot they had an account?
├─ Results not actionable?
├─ No reminder/notification?
└─ Better tool available elsewhere?

Check:
├─ Last activity time for churned users
├─ What % visit > 1 day later?
├─ What % return after 1 week?
└─ Compare returning vs leaving users
```

**If Paid Conversion < 5%:**
```
Why don't they upgrade?
├─ Don't see upgrade button?
├─ Unclear what you get?
├─ Price too high?
├─ Didn't need more tools?
└─ Will decide later?

Check:
├─ What % see Pro tier pricing?
├─ What % click upgrade button?
├─ How many free users have used 5+ tools?
├─ What % of power users convert?
```

**Document finding:**
```
BLOCKER: [name]
CURRENT: __% (target: __%)
ROOT CAUSE: ________________
EVIDENCE: ________________
```

---

### Segment 3: HYPOTHESIS (25 minutes)
**9:45 AM - 10:10 AM**

**Template:**

```
EXPERIMENT: [Name]

HYPOTHESIS:
If we [SPECIFIC CHANGE],
Then [METRIC] will improve to [TARGET]%

SPECIFIC CHANGE:
What: ________________
How: ________________
Where: ________________
Timeline: This week (Mon-Sun)

METRIC TO MOVE:
Primary: ________________ (current: __%)
Target: ________________ (__%)
Success = move by 10%+

MEASUREMENT:
Track via: ________________
Check frequency: [Daily/Twice daily]
Success indicator: ________________
```

**Examples:**

```
EXPERIMENT: Simplify Onboarding Form

HYPOTHESIS:
If we remove the optional fields (step 2 → step 1),
Then onboarding completion will improve to 65%

SPECIFIC CHANGE:
What: Remove "industry description" field
How: Just keep: name, company, startup description
Where: In onboarding form in app.py
Timeline: Mon-Thu build & test, Fri deploy

METRIC TO MOVE:
Primary: Onboarding completion rate (current: 35%)
Target: 65% (goal: +30% improvement)
Success = move to 50%+ (conservative: +15%)

MEASUREMENT:
Track via: Count of users seeing dashboard
Check: Daily (via metrics_tracker.py)
Success: By Friday, 50%+ of signups complete form
```

---

### Segment 4: PRIORITIZE (20 minutes)
**10:10 AM - 10:30 AM**

**Pick 1 primary experiment:**
```
This week I'll focus on: ________________
Why: ________________ is the blocker
How it helps: ________________
When we ship: ________________
```

**Add 1-2 quick wins:**
```
Quick win 1: ________________ (1-2 hour task)
Quick win 2: ________________ (1-2 hour task)

(These are small optimizations that don't require
experiments, just obvious improvements)
```

**Document in spreadsheet:**
```
Week of [DATE]:

Primary experiment: ________________
Status: [Not started / In progress / Shipped / Done]
Result: [Success / Fail / Pending]

Quick win 1: ________________
Quick win 2: ________________
```

---

## EXECUTION (Mon-Fri)

### Monday Afternoon (2 hours)
Build the change:
- Edit code
- Test locally
- Make sure it works

### Tuesday-Wednesday (As scheduled)
Run the experiment:
- Monitor errors
- Check adoption
- Gather feedback

### Thursday (1 hour)
Analyze results:
- Pull metrics
- Calculate success
- Decide: Keep or revert?

### Friday Morning (30 min)
Write report:
```
# Weekly Improvement Report

## Experiment: [Name]
- Before: ___%
- After: ___%
- Change: +__% (Success/Fail)

## What we learned:
- ________________
- ________________

## Next experiment:
- ________________
```

---

## Success Metrics for the Ritual

```
✓ Every Monday 9:00 AM, run the ritual (90 min)
✓ Every week, 1 experiment shipped and measured
✓ Every month, 4-6 improvements shipped
✓ Track cumulative progress (30% → 50% → 70%)
✓ Zero guess-based changes (only data-driven)
✓ Every change measured before going live
```

---

## What to Optimize Each Week

### Week 1: Onboarding
- Improve form completion rate (target: 50%+)
- Simplify inputs, better copy, faster results
- A/B test: Short vs long form, different CTAs

### Week 2: Tool Exploration
- Get more users to try 2+ tools (target: 60%+)
- Better dashboard recommendations
- "Next tool" buttons, email suggestions

### Week 3: Retention  
- Increase weekly active rate (target: 30%+)
- Email reminders, progress tracking, gamification
- Better "next steps" guidance

### Week 4: Monetization
- Free→Pro conversion (target: 5%+)
- Upgrade triggers, clear benefits, team tier
- Pricing visibility, limited free tools

### Weeks 5+
- Follow `IMPLEMENTATION_ROADMAP.md`
- Each week targets specific metric from roadmap
- Always measure before shipping

---

## Quick Checklist

**Every Monday 9 AM:**
- [ ] Pull metrics from metrics_tracker.py
- [ ] Identify #1 blocker
- [ ] Root cause analysis (why?)
- [ ] Hypothesis (what small change?)
- [ ] Experiment design (how to measure?)
- [ ] Pick primary experiment
- [ ] Document quick wins

**Every Friday:**
- [ ] Measure experiment results
- [ ] Success or fail?
- [ ] Write report
- [ ] Plan next week
- [ ] Celebrate wins

**Every successful change:**
- [ ] Keep (ship to all users)
- [ ] OR iterate (test different approach)
- [ ] OR revert (didn't move the needle)

---

## Tools You Need

```python
# Pull metrics
from metrics_tracker import MetricsDatabase
db = MetricsDatabase()

# Daily metrics
metrics = db.calculate_daily_metrics()

# Funnel analysis
funnel = db.get_funnel_analysis()

# Top tools
top_tools = db.get_top_tools(days=7)

# Cohort retention
retention = db.get_cohort_retention(cohort_days=7)

# Log experiment result
db.log_ab_test_result(
    test_name="Simplify Form",
    variant_a="Old form (5 fields)",
    variant_b="New form (3 fields)",
    metric="onboarding_completion_rate",
    variant_a_value=35,
    variant_b_value=55
)
```

---

## The Mindset

**Not:** "This feature seems cool, let's build it"  
**But:** "This metric is low, what will fix it? Let's test."

**Not:** "I think users will like this"  
**But:** "Here's what the data says, let's measure the change"

**Not:** "We're guessing"  
**But:** "We're learning rapidly from real users"

---

**Every Monday, 90 minutes, better product.**

That's all it takes.

🚀 Ship it Friday. Measure it Sunday. Improve it Monday.

Repeat 52 times.

You've built something unstoppable.

