# Changelog – Ben's Electric Solutions

**Updated:** 2026-01-09T14:30:00Z
**Source:** onboarding_call_jan_9_2026

## Summary
13 fields updated: business hours confirmed, pricing added, VIP customer G&M Pressure Washing defined, notification channels confirmed, transfer setup clarified, contact email updated.

## Field-by-Field Changes

### `business_hours.end_time`
- **Before:** `17:00`
- **After:**  `16:30`
- **Reason:** Confirmed by Ben on onboarding call as 8:00 AM to 4:30 PM

### `contact_email`
- **Before:** `ben@benselectricsolutionsteam.com`
- **After:**  `info@benselectricsolutionsteam.com`
- **Reason:** Ben confirmed info@ is the preferred business notification email

### `notification_email`
- **Before:** `None`
- **After:**  `info@benselectricsolutionsteam.com`
- **Reason:** New field — confirmed on onboarding call

### `notification_sms`
- **Before:** `None`
- **After:**  `Ben's main business number`
- **Reason:** Confirmed: SMS + email both sent after every call

### `pricing`
- **Before:** `None`
- **After:**  `{'service_call_fee': 115, 'hourly_rate': 98, 'billing_increment_hours': 0.5}`
- **Reason:** Pricing details not discussed in demo — confirmed fully on onboarding call

### `vip_customers`
- **Before:** `None`
- **After:**  `G&M Pressure Washing – Shelley Manley – 403-870-8494`
- **Reason:** Onboarding confirmed G&M Pressure Washing as sole after-hours emergency VIP

### `emergency_routing_rules[0].phone_number`
- **Before:** `main business number (personal)`
- **After:**  `Ben's second personal number (pending setup)`
- **Reason:** Ben setting up separate personal number — transfer will go there once ready

### `call_transfer_rules.timeout_seconds`
- **Before:** `None`
- **After:**  `30`
- **Reason:** Standard 30s timeout confirmed during onboarding

### `call_setup`
- **Before:** `None`
- **After:**  `{'device': 'Android', 'forwarding_method': 'forward-on-no-answer'}`
- **Reason:** Confirmed Android device — call forwarding on no-answer until second number ready

### `after_hours_flow_summary`
- **Before:** `Generic after-hours flow`
- **After:**  `VIP G&M Pressure Washing patched through to Ben. All others: collect details and follow up next business day.`
- **Reason:** Specific VIP routing rule confirmed on onboarding

### `office_hours_flow_summary`
- **Before:** `Collect details and send to Ben`
- **After:**  `Collect details, mention pricing only if asked, attempt transfer if customer insists, send post-call email+SMS`
- **Reason:** Pricing mention policy and transfer behavior confirmed on onboarding

### `questions_or_unknowns`
- **Before:** `['Exact business hours closing time', "Ben's second number", "Greg's contact", 'Whitelist numbers', 'Pricing details']`
- **After:**  `["Ben's second personal number TBD", "Greg's full contact details not provided", 'Full VIP contractor list not provided']`
- **Reason:** Most unknowns resolved. Three items still pending.

### `integration_constraints`
- **Before:** `['Jobber integration in progress', 'No auto-create jobs']`
- **After:**  `['Jobber integration in progress', 'No auto-create jobs', 'Clara trained on website for FAQ', 'Cannot confirm appointment slots — no calendar access']`
- **Reason:** Additional constraints clarified on onboarding call

## Unresolved Items

- Ben's second personal number not yet available — transfer destination cannot be finalized until provided
- Greg's role as operations manager not yet active — no routing rules for Greg yet