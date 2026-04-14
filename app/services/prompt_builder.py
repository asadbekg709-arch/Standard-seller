JSON_SYSTEM = (
    "You are a helpful AI assistant for a CRM system. "
    "Always respond with valid JSON only — no markdown, no extra text."
)


def build_email_prompt(customer: dict, orders: list, tone: str, language: str) -> list[dict]:
    lang_map = {"en": "English", "ru": "Russian", "uz": "Uzbek"}
    lang = lang_map.get(language, "English")

    customer_info = (
        f"Name: {customer.get('name', 'N/A')}\n"
        f"Email: {customer.get('email', 'N/A')}\n"
        f"Company: {customer.get('company', 'N/A')}\n"
        f"Last contact: {customer.get('last_contact', 'N/A')}"
    )
    order_info = "\n".join(
        f"- {o.get('product', '?')} | {o.get('amount', '?')} | {o.get('status', '?')}"
        for o in orders[:5]
    ) or "No recent orders"

    return [
        {"role": "system", "content": JSON_SYSTEM},
        {
            "role": "user",
            "content": (
                f"Write a follow-up email in {lang} with a {tone} tone.\n\n"
                f"Customer info:\n{customer_info}\n\n"
                f"Recent orders:\n{order_info}\n\n"
                'Return JSON: {"subject": "...", "body": "..."}'
            ),
        },
    ]


def build_lead_prompt(customer: dict, orders: list, activities: list) -> list[dict]:
    customer_info = (
        f"Name: {customer.get('name', 'N/A')}\n"
        f"Industry: {customer.get('industry', 'N/A')}\n"
        f"Company size: {customer.get('company_size', 'N/A')}\n"
        f"Source: {customer.get('source', 'N/A')}"
    )
    order_info = (
        f"Total orders: {len(orders)}\n"
        f"Total value: {sum(o.get('amount', 0) for o in orders)}"
    )
    activity_info = "\n".join(
        f"- {a.get('type', '?')}: {a.get('description', '?')}"
        for a in activities[:10]
    ) or "No recent activity"

    return [
        {"role": "system", "content": JSON_SYSTEM},
        {
            "role": "user",
            "content": (
                "Score this CRM lead from 0 to 100.\n\n"
                f"Customer:\n{customer_info}\n\n"
                f"Orders:\n{order_info}\n\n"
                f"Activities:\n{activity_info}\n\n"
                'Return JSON: {"score": <0-100>, "priority": "low|medium|high", "reason": "..."}'
            ),
        },
    ]


def build_summary_prompt(text: str) -> list[dict]:
    return [
        {"role": "system", "content": JSON_SYSTEM},
        {
            "role": "user",
            "content": (
                "Summarize these meeting notes.\n\n"
                f"{text}\n\n"
                'Return JSON: {"summary": "...", "action_items": [...], "key_points": [...]}'
            ),
        },
    ]


def build_chat_prompt(customer: dict, question: str) -> list[dict]:
    customer_info = (
        f"Name: {customer.get('name', 'N/A')}\n"
        f"Email: {customer.get('email', 'N/A')}\n"
        f"Status: {customer.get('status', 'N/A')}"
    )
    return [
        {
            "role": "system",
            "content": (
                "You are a CRM assistant. Answer questions about the customer based on the provided data. "
                "Always respond with valid JSON only."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Customer data:\n{customer_info}\n\n"
                f"Question: {question}\n\n"
                'Return JSON: {"answer": "..."}'
            ),
        },
    ]
