"""A realistic demo inbox so the product runs end-to-end with no Gmail account.

Static fixed timestamps (no datetime.now()) so the demo is deterministic.
"""

MOCK_INBOX = [
    {
        "id": "m1",
        "from": "Priya Nair <priya@acmeretail.com>",
        "subject": "Order #A4821 hasn't arrived — need help",
        "received": "2026-06-21 09:14",
        "unread": True,
        "body": (
            "Hi, I placed order #A4821 on 06/12/2026 for the standing desk ($499) and the "
            "tracking page still says 'label created'. It was promised by 06/18. Can you check "
            "what's going on and let me know when it'll ship? This is getting urgent."
        ),
    },
    {
        "id": "m2",
        "from": "Daniel Kim <daniel.kim@northwind.io>",
        "subject": "Quick sync on the partnership next week?",
        "received": "2026-06-21 08:02",
        "unread": True,
        "body": (
            "Hey Sneha — really enjoyed our chat at the conference. Could we grab 30 minutes "
            "next Tuesday or Wednesday to talk through how a Northwind x your-team integration "
            "might work? Mornings are best for me. Here's my calendar: https://cal.northwind.io/daniel"
        ),
    },
    {
        "id": "m3",
        "from": "Stripe <receipts@stripe.com>",
        "subject": "Your invoice for June is ready ($1,290.00)",
        "received": "2026-06-20 23:40",
        "unread": False,
        "body": (
            "Invoice INV-2026-0617 for $1,290.00 is now available. Payment will be automatically "
            "collected on 06/25/2026 from the card ending 4242. View invoice: https://stripe.com/inv/2026-0617"
        ),
    },
    {
        "id": "m4",
        "from": "TechCrunch <newsletter@techcrunch.com>",
        "subject": "🚀 This week in AI: 12 funding rounds you missed",
        "received": "2026-06-20 18:30",
        "unread": False,
        "body": (
            "The biggest AI raises of the week, plus a teardown of the latest agent frameworks. "
            "Read online or unsubscribe at the bottom of this email."
        ),
    },
    {
        "id": "m5",
        "from": "Aarav Sharma <aarav@boardco.com>",
        "subject": "URGENT: Board deck numbers need updating before 2pm",
        "received": "2026-06-21 07:48",
        "unread": True,
        "body": (
            "Sneha — the Q2 revenue figure on slide 7 is stale. Please update it to $842K and "
            "re-send the deck before the 2pm board call today. Let me know once it's done."
        ),
    },
]
