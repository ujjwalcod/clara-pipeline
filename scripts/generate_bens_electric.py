import json
from pathlib import Path

OUTPUT_BASE = Path("/home/claude/clara-pipeline/outputs/accounts/bens_electric_solutions")

# ── V1 MEMO (from demo call) ──────────────────────────────────────────────
v1_memo = {
  "account_id": "bens_electric_solutions",
  "_version": "v1",
  "_source": "demo_call",
  "_extracted_at": "2026-01-08T18:30:00Z",
  "company_name": "Ben's Electric Solutions",
  "owner": "Ben Penoyer",
  "contact_email": "ben@benselectricsolutionsteam.com",
  "office_address": "Calgary, Alberta, Canada",
  "business_hours": {
    "days": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "start_time": "08:00",
    "end_time": "17:00",
    "timezone": "America/Edmonton",
    "notes": "Exact closing time not confirmed on demo call"
  },
  "services_supported": [
    "Service calls",
    "Outlet replacement and aluminum wiring mitigation",
    "EV charger installation",
    "Hot tub hookup and electrical",
    "Panel changes",
    "Fixture replacement",
    "Lighting upgrades (LED)",
    "Renovations and troubleshooting",
    "Custom home builds",
    "Tenant improvements",
    "Generator hookups",
    "Residential and commercial electrical"
  ],
  "services_not_supported": [
    "Gemstone lights",
    "Full pool installation (plumbing only)",
    "Full hot tub installation (electrical only)"
  ],
  "team": {
    "owner": "Ben Penoyer",
    "journeymen": 3,
    "apprentices": 1,
    "subcontractors": 2,
    "operations_manager_incoming": "Greg (last name unknown)"
  },
  "crm": "Jobber",
  "accounting": "QuickBooks",
  "call_volume_estimate": "20-50 calls per week",
  "emergency_definition": [
    "Gas station pump failure (VIP customer only)",
    "Active electrical emergency for known property managers or general contractors"
  ],
  "emergency_routing_rules": [
    {
      "priority": 1,
      "contact_name": "Ben Penoyer",
      "phone_number": "main business number (personal)",
      "method": "call",
      "notes": "Ben is sole on-call contact after hours. Only for known/existing clients."
    }
  ],
  "non_emergency_routing_rules": {
    "during_hours": "Clara collects caller details and job info, sends summary to Ben via email/SMS",
    "after_hours": "Clara collects details and informs caller that someone will follow up next business day"
  },
  "call_transfer_rules": {
    "timeout_seconds": None,
    "retries": None,
    "transfer_fail_action": "Take message and assure callback",
    "what_to_say_if_fail": "I wasn't able to connect you right now. I've taken your details and someone will be in touch shortly."
  },
  "integration_constraints": [
    "Jobber CRM integration with Clara is in progress — not yet live",
    "Do not auto-create Jobber jobs — Ben reviews and books manually",
    "Clara does not have access to Jobber calendar for scheduling confirmation"
  ],
  "after_hours_flow_summary": "Greet caller, identify if emergency or non-emergency. For emergencies from known clients, route to Ben. For all others, collect name, number, and issue details, confirm follow-up next business day.",
  "office_hours_flow_summary": "Greet caller, collect name, callback number, and nature of job. Route or transfer to Ben. Send post-call summary via email and SMS. Mention service call fee only if customer asks.",
  "questions_or_unknowns": [
    "Exact business hours closing time not confirmed (approx 5 PM from demo)",
    "Ben's second personal number not yet set up — transfer destination TBD",
    "Greg's contact details (operations manager) unknown",
    "Whitelist of VIP/contractor numbers not defined",
    "Pricing details not mentioned in demo call"
  ],
  "notes": "Ben is first-time AI user. Very positive demo reaction. Signed 3-month starter plan at $249/month. Sole proprietor, sole admin, growing to 5 vans. Uses Jobber + QuickBooks."
}

# ── V2 MEMO (after onboarding call) ──────────────────────────────────────
v2_memo = {
  "account_id": "bens_electric_solutions",
  "_version": "v2",
  "_source": "onboarding_call",
  "_extracted_at": "2026-01-09T14:00:00Z",
  "company_name": "Ben's Electric Solutions",
  "owner": "Ben Penoyer",
  "contact_email": "info@benselectricsolutionsteam.com",
  "notification_email": "info@benselectricsolutionsteam.com",
  "notification_sms": "Ben's main business number",
  "office_address": "Calgary, Alberta, Canada",
  "business_hours": {
    "days": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "start_time": "08:00",
    "end_time": "16:30",
    "timezone": "America/Edmonton",
    "notes": "Confirmed 8:00 AM to 4:30 PM Mountain Time"
  },
  "services_supported": [
    "Service calls",
    "Outlet replacement and aluminum wiring mitigation",
    "EV charger installation",
    "Hot tub hookup and electrical",
    "Panel changes",
    "Fixture replacement",
    "Lighting upgrades (LED)",
    "Renovations and troubleshooting",
    "Custom home builds",
    "Tenant improvements",
    "Generator hookups",
    "Residential and commercial electrical"
  ],
  "services_not_supported": [
    "Gemstone lights",
    "Full pool installation (plumbing only)",
    "Full hot tub installation (electrical only)"
  ],
  "team": {
    "owner": "Ben Penoyer",
    "journeymen": 3,
    "apprentices": 1,
    "subcontractors": 2,
    "operations_manager_incoming": "Greg (last name unknown)"
  },
  "crm": "Jobber",
  "accounting": "QuickBooks",
  "call_volume_estimate": "20-50 calls per week",
  "pricing": {
    "service_call_fee": 115,
    "hourly_rate": 98,
    "billing_increment_hours": 0.5,
    "half_hour_rate": 49,
    "currency": "CAD",
    "mention_policy": "Only mention pricing when customer asks — do not proactively state on every call"
  },
  "emergency_definition": [
    "Gas station pump failure or electrical outage (VIP customer G&M Pressure Washing only)",
    "Active electrical emergency for known property managers or general contractors"
  ],
  "emergency_routing_rules": [
    {
      "priority": 1,
      "contact_name": "Ben Penoyer",
      "phone_number": "Ben's second personal number (pending setup)",
      "method": "call transfer",
      "notes": "Only for VIP customer G&M Pressure Washing / Shelley Manley. Collect gas station address/location before transferring."
    }
  ],
  "vip_customers": [
    {
      "company": "G&M Pressure Washing",
      "contact_name": "Shelley Manley",
      "phone": "403-870-8494",
      "email": "gm_pressurewash@yahoo.ca",
      "type": "Property manager",
      "properties": "~20 Chevron and Esso gas stations across Calgary",
      "emergency_treatment": "Patch call through to Ben after hours. Collect gas station address first.",
      "notes": "They manage gas stations — electrical failures at pumps are emergencies"
    }
  ],
  "non_emergency_routing_rules": {
    "during_hours": "Clara collects caller name, number, and job details. Sends email + SMS to Ben. Transfer to Ben's second number if caller insists on speaking to someone.",
    "after_hours": "For non-VIP: collect name, number, job details. Inform caller team will follow up next business day. For VIP G&M Pressure Washing: treat as emergency — collect gas station address and patch through to Ben."
  },
  "call_transfer_rules": {
    "timeout_seconds": 30,
    "retries": 1,
    "transfer_destination": "Ben's second personal number (TBD — pending setup)",
    "transfer_fail_action": "Take message and assure callback",
    "what_to_say_if_fail": "I wasn't able to connect you right now, but I've taken your details and Ben will follow up with you as soon as possible."
  },
  "integration_constraints": [
    "Jobber CRM integration with Clara is in progress — not yet live",
    "Do not auto-create Jobber jobs — Ben reviews and books manually",
    "Clara does not have access to Jobber calendar — cannot confirm appointment slots",
    "Clara trained on Ben's Electric website for services and FAQs"
  ],
  "call_setup": {
    "device": "Android",
    "forwarding_method": "Forward-on-no-answer until second number ready, then full forwarding to Clara",
    "second_number_status": "Pending — Ben setting up new personal number"
  },
  "after_hours_flow_summary": "Greet caller, note office is closed. Ask purpose of call. If caller is from G&M Pressure Washing / Shelley Manley (or mentions Chevron/Esso gas station emergency): collect gas station address and patch through to Ben. For all other callers: collect name, callback number, and description of issue. Confirm team will follow up next business day by start of business hours.",
  "office_hours_flow_summary": "Greet caller as Ben's Electric Solutions. Ask purpose of call. Collect name and callback number. Describe service briefly. Mention pricing only if asked ($115 call-out, $98/hr billed in 30-min increments). Attempt transfer to Ben if caller insists on speaking live. If transfer fails or not needed, confirm details received and team will be in touch. Send post-call email + SMS to Ben.",
  "questions_or_unknowns": [
    "Ben's second personal number not yet confirmed — transfer destination still TBD",
    "Greg's full name and contact details not provided",
    "Exact list of VIP contractor numbers not provided — only G&M Pressure Washing confirmed"
  ],
  "notes": "Onboarding completed. Business hours confirmed 8AM-4:30PM MT Mon-Fri. Pricing confirmed. G&M Pressure Washing is sole after-hours VIP. Testing phase begins immediately. Go-live target: weekend of Jan 11-12, 2026. Follow-up call Friday Jan 10 at 2PM."
}

# ── CHANGELOG ─────────────────────────────────────────────────────────────
changelog = {
  "account_id": "bens_electric_solutions",
  "updated_at": "2026-01-09T14:30:00Z",
  "source": "onboarding_call_jan_9_2026",
  "summary": "13 fields updated: business hours confirmed, pricing added, VIP customer G&M Pressure Washing defined, notification channels confirmed, transfer setup clarified, contact email updated.",
  "changes": [
    {
      "field": "business_hours.end_time",
      "old_value": "17:00",
      "new_value": "16:30",
      "reason": "Confirmed by Ben on onboarding call as 8:00 AM to 4:30 PM"
    },
    {
      "field": "contact_email",
      "old_value": "ben@benselectricsolutionsteam.com",
      "new_value": "info@benselectricsolutionsteam.com",
      "reason": "Ben confirmed info@ is the preferred business notification email"
    },
    {
      "field": "notification_email",
      "old_value": None,
      "new_value": "info@benselectricsolutionsteam.com",
      "reason": "New field — confirmed on onboarding call"
    },
    {
      "field": "notification_sms",
      "old_value": None,
      "new_value": "Ben's main business number",
      "reason": "Confirmed: SMS + email both sent after every call"
    },
    {
      "field": "pricing",
      "old_value": None,
      "new_value": {"service_call_fee": 115, "hourly_rate": 98, "billing_increment_hours": 0.5},
      "reason": "Pricing details not discussed in demo — confirmed fully on onboarding call"
    },
    {
      "field": "vip_customers",
      "old_value": None,
      "new_value": "G&M Pressure Washing – Shelley Manley – 403-870-8494",
      "reason": "Onboarding confirmed G&M Pressure Washing as sole after-hours emergency VIP"
    },
    {
      "field": "emergency_routing_rules[0].phone_number",
      "old_value": "main business number (personal)",
      "new_value": "Ben's second personal number (pending setup)",
      "reason": "Ben setting up separate personal number — transfer will go there once ready"
    },
    {
      "field": "call_transfer_rules.timeout_seconds",
      "old_value": None,
      "new_value": 30,
      "reason": "Standard 30s timeout confirmed during onboarding"
    },
    {
      "field": "call_setup",
      "old_value": None,
      "new_value": {"device": "Android", "forwarding_method": "forward-on-no-answer"},
      "reason": "Confirmed Android device — call forwarding on no-answer until second number ready"
    },
    {
      "field": "after_hours_flow_summary",
      "old_value": "Generic after-hours flow",
      "new_value": "VIP G&M Pressure Washing patched through to Ben. All others: collect details and follow up next business day.",
      "reason": "Specific VIP routing rule confirmed on onboarding"
    },
    {
      "field": "office_hours_flow_summary",
      "old_value": "Collect details and send to Ben",
      "new_value": "Collect details, mention pricing only if asked, attempt transfer if customer insists, send post-call email+SMS",
      "reason": "Pricing mention policy and transfer behavior confirmed on onboarding"
    },
    {
      "field": "questions_or_unknowns",
      "old_value": ["Exact business hours closing time", "Ben's second number", "Greg's contact", "Whitelist numbers", "Pricing details"],
      "new_value": ["Ben's second personal number TBD", "Greg's full contact details not provided", "Full VIP contractor list not provided"],
      "reason": "Most unknowns resolved. Three items still pending."
    },
    {
      "field": "integration_constraints",
      "old_value": ["Jobber integration in progress", "No auto-create jobs"],
      "new_value": ["Jobber integration in progress", "No auto-create jobs", "Clara trained on website for FAQ", "Cannot confirm appointment slots — no calendar access"],
      "reason": "Additional constraints clarified on onboarding call"
    }
  ],
  "unresolved_conflicts": [
    "Ben's second personal number not yet available — transfer destination cannot be finalized until provided",
    "Greg's role as operations manager not yet active — no routing rules for Greg yet"
  ]
}

# ── AGENT SPEC V1 ─────────────────────────────────────────────────────────
v1_agent = {
  "agent_name": "Ben's Electric Solutions – Clara Agent",
  "version": "v1",
  "voice_style": "professional_warm",
  "language": "en-US",
  "system_prompt": """You are Clara, the virtual receptionist for Ben's Electric Solutions, an electrical contracting company based in Calgary, Alberta, Canada.

You handle inbound calls on behalf of Ben, the owner. Your job is to greet callers professionally, understand their needs, collect their information, and ensure they receive a prompt follow-up.

## BUSINESS HOURS
Monday to Friday, approximately 8:00 AM to 5:00 PM Mountain Time.

## SERVICES WE OFFER
We are a full-service electrical contractor serving residential and commercial clients in Calgary. We handle: service calls, outlet replacements, aluminum wiring mitigation, EV charger installations, hot tub electrical hookups, panel changes, fixture replacements, LED lighting upgrades, renovations, troubleshooting, custom home builds, and tenant improvements.

We do NOT offer: gemstone lights, full pool installation, or full hot tub installation (electrical connection only).

## DURING OFFICE HOURS FLOW
1. Greet the caller warmly: "Thank you for calling Ben's Electric Solutions, this is Clara. How can I help you today?"
2. Listen and understand the purpose of their call.
3. Collect their full name and best callback number.
4. If they ask about pricing: our service call fee is $115 to come to site, and we charge $98 per hour billed in 30-minute increments. Share this only if they ask.
5. Let them know Ben or a team member will be in touch shortly to confirm details.
6. Ask: "Is there anything else I can help you with today?"
7. Close warmly: "Thank you for calling Ben's Electric Solutions. We'll be in touch soon. Have a great day!"

## AFTER HOURS FLOW
1. Greet the caller: "Thank you for calling Ben's Electric Solutions. Our office is currently closed — our hours are Monday to Friday, 8 AM to 5 PM Mountain Time."
2. Ask the purpose of their call.
3. Ask if this is an emergency.
4. If EMERGENCY from a known client (property manager, contractor): Collect their name, callback number, and address of the issue. Attempt to connect them with Ben.
5. If transfer fails: "I wasn't able to reach Ben directly, but I've taken your details and someone will call you back as soon as possible."
6. If NON-EMERGENCY: Collect name, number, and description of the issue. "I've got your details and a team member will follow up with you next business day."
7. Ask: "Is there anything else I can help you with?"
8. Close the call.

## IMPORTANT RULES
- Never mention "function calls", "tools", "AI systems", or any technical terms to callers.
- Do not ask more questions than needed — only collect what is necessary for routing and follow-up.
- Never make up pricing, availability, or scheduling commitments.
- If you don't know something, say: "I'll make sure Ben follows up with you on that."
- Keep the tone warm, calm, and professional at all times.
""",
  "key_variables": {
    "company_name": "Ben's Electric Solutions",
    "owner_name": "Ben Penoyer",
    "timezone": "America/Edmonton",
    "business_hours_start": "08:00",
    "business_hours_end": "17:00",
    "business_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "office_address": "Calgary, Alberta, Canada",
    "emergency_contacts": ["Ben Penoyer – main business number"]
  },
  "tool_invocation_placeholders": [
    {
      "tool_id": "transfer_call",
      "trigger": "Caller insists on speaking to a live person OR emergency from known client after hours",
      "destination": "Ben Penoyer – main business number"
    },
    {
      "tool_id": "send_summary",
      "trigger": "End of every call",
      "destination": "ben@benselectricsolutionsteam.com + SMS to Ben's number"
    }
  ],
  "call_transfer_protocol": {
    "method": "warm_transfer",
    "timeout_seconds": 30,
    "announcement": "Let me connect you with Ben now. Please hold for just a moment."
  },
  "fallback_protocol": {
    "trigger": "transfer_fails",
    "action": "take_message",
    "agent_script": "I wasn't able to connect you right now, but I've taken your details and Ben will follow up with you as soon as possible."
  },
  "notes": "v1 based on demo call. Business hours end time approximate. Pricing not yet configured. VIP customer routing not yet defined. Second transfer number TBD."
}

# ── AGENT SPEC V2 ─────────────────────────────────────────────────────────
v2_agent = {
  "agent_name": "Ben's Electric Solutions – Clara Agent",
  "version": "v2",
  "voice_style": "professional_warm",
  "language": "en-US",
  "system_prompt": """You are Clara, the virtual receptionist for Ben's Electric Solutions, an electrical contracting company based in Calgary, Alberta, Canada.

You handle inbound calls on behalf of Ben Penoyer, the owner. Your job is to greet callers professionally, understand their needs, collect their information, and ensure they receive a prompt follow-up.

## BUSINESS HOURS
Monday to Friday, 8:00 AM to 4:30 PM Mountain Time (America/Edmonton).

## SERVICES WE OFFER
We are a full-service electrical contractor serving residential and commercial clients in Calgary. We handle: service calls, outlet replacements, aluminum wiring mitigation, EV charger installations, hot tub electrical hookups, panel changes, fixture replacements, LED lighting upgrades, renovations, troubleshooting, custom home builds, and tenant improvements.

We do NOT offer: gemstone lights, full pool installation, or full hot tub installation (electrical connection only).

## PRICING (share ONLY if the caller asks)
- Service call fee: $115 (covers our travel to your location)
- Labour rate: $98 per hour, billed in 30-minute increments ($49 per half hour)
- Do NOT mention pricing on every call — only when a customer directly asks about cost or minimum fees.

## DURING OFFICE HOURS FLOW
1. Greet warmly: "Thank you for calling Ben's Electric Solutions, this is Clara. How can I help you today?"
2. Listen and understand the purpose of their call.
3. Collect their full name and best callback number.
4. If they ask about pricing: share the service call fee and hourly rate as above.
5. Let them know someone will be in touch shortly to confirm details and next steps.
6. If the caller insists on speaking to someone live, say: "Of course — let me try to connect you now." Then attempt transfer to Ben's direct line.
7. If transfer fails: "I wasn't able to reach Ben right now, but I've got your details and he'll follow up with you as soon as possible."
8. Ask: "Is there anything else I can help you with today?"
9. Close: "Thank you for calling Ben's Electric Solutions. We'll be in touch soon. Have a great day!"

## AFTER HOURS FLOW
1. Greet: "Thank you for calling Ben's Electric Solutions. Our office is currently closed — we're available Monday to Friday, 8 AM to 4:30 PM Mountain Time."
2. Ask the purpose of their call.
3. Determine if this is an emergency or non-emergency.

### IF EMERGENCY AND CALLER IS FROM G&M PRESSURE WASHING (Shelley Manley / Chevron or Esso gas station):
- This is your one VIP after-hours emergency customer.
- Immediately collect: caller name, callback number, and the ADDRESS of the gas station with the issue.
- Say: "I'm going to connect you with Ben right now. Please hold."
- Attempt transfer to Ben's direct line.
- If transfer fails: "I wasn't able to reach Ben directly, but I've taken all your details and he will call you back immediately."

### IF EMERGENCY FROM ANY OTHER CALLER:
- Collect name, callback number, and address of the issue.
- Say: "I've taken your details and Ben will follow up with you as soon as possible."
- Do NOT attempt after-hours transfer for unknown callers.

### IF NON-EMERGENCY:
- Collect name, callback number, and brief description of the issue.
- Say: "I've got your details. A team member will follow up with you next business day."

4. Ask: "Is there anything else I can help you with?"
5. Close warmly.

## IMPORTANT RULES
- NEVER mention "function calls", "tools", "APIs", or any technical terms to callers.
- Do not ask more questions than needed — collect only what is needed for routing and follow-up.
- Never make up pricing, availability, or scheduling commitments not listed here.
- If you don't know something, say: "I'll make sure Ben follows up with you on that."
- Keep tone warm, calm, and professional at all times.
- Do not screen calls from callers who identify as existing contractors or field team members — note their details and route accordingly.
""",
  "key_variables": {
    "company_name": "Ben's Electric Solutions",
    "owner_name": "Ben Penoyer",
    "timezone": "America/Edmonton",
    "business_hours_start": "08:00",
    "business_hours_end": "16:30",
    "business_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "office_address": "Calgary, Alberta, Canada",
    "service_call_fee_cad": 115,
    "hourly_rate_cad": 98,
    "billing_increment_hours": 0.5,
    "emergency_contacts": ["Ben Penoyer – second personal number (TBD)"],
    "vip_after_hours": {
      "company": "G&M Pressure Washing",
      "contact": "Shelley Manley",
      "phone": "403-870-8494",
      "properties": "Chevron and Esso gas stations in Calgary"
    }
  },
  "tool_invocation_placeholders": [
    {
      "tool_id": "transfer_call",
      "trigger": "Caller insists on live person during office hours OR G&M Pressure Washing emergency after hours",
      "destination": "Ben Penoyer – second personal number (TBD)"
    },
    {
      "tool_id": "send_post_call_summary",
      "trigger": "End of every call",
      "destination": "info@benselectricsolutionsteam.com + SMS to Ben's main number"
    }
  ],
  "call_transfer_protocol": {
    "method": "warm_transfer",
    "timeout_seconds": 30,
    "retries": 1,
    "announcement": "Let me connect you with Ben now. Please hold for just a moment."
  },
  "fallback_protocol": {
    "trigger": "transfer_fails",
    "action": "take_message",
    "agent_script": "I wasn't able to reach Ben right now, but I've taken your details and he'll follow up with you as soon as possible."
  },
  "notes": "v2 based on onboarding call. Business hours confirmed 8AM-4:30PM MT. Pricing configured. G&M Pressure Washing VIP routing added. Transfer number pending Ben's second phone setup. Go-live target: Jan 11-12, 2026."
}

# ── WRITE ALL FILES ────────────────────────────────────────────────────────
for version, memo, agent in [("v1", v1_memo, v1_agent), ("v2", v2_memo, v2_agent)]:
    d = OUTPUT_BASE / version
    d.mkdir(parents=True, exist_ok=True)
    (d / "memo.json").write_text(json.dumps(memo, indent=2))
    (d / "agent_spec.json").write_text(json.dumps(agent, indent=2))
    print(f"✅ Saved {version}/memo.json and {version}/agent_spec.json")

# Write changelog
v2_dir = OUTPUT_BASE / "v2"
(v2_dir / "changelog.json").write_text(json.dumps(changelog, indent=2))

# Write markdown changelog
md = ["# Changelog – Ben's Electric Solutions", "", f"**Updated:** {changelog['updated_at']}", f"**Source:** {changelog['source']}", "", "## Summary", changelog['summary'], "", "## Field-by-Field Changes", ""]
for c in changelog["changes"]:
    md.append(f"### `{c['field']}`")
    md.append(f"- **Before:** `{c['old_value']}`")
    md.append(f"- **After:**  `{c['new_value']}`")
    md.append(f"- **Reason:** {c['reason']}")
    md.append("")
md += ["## Unresolved Items", ""]
for u in changelog["unresolved_conflicts"]:
    md.append(f"- {u}")
(v2_dir / "changelog.md").write_text("\n".join(md))
print("✅ Saved v2/changelog.json and v2/changelog.md")
print(f"\n📁 All outputs in: {OUTPUT_BASE}")
