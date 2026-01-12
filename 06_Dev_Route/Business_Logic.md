# MAPA-RD Business Logic

> [!IMPORTANT]
> This document acts as the SOURCE OF TRUTH for the business process. Code must strictly follow these steps.

## Phase 1: Intake & Onboarding

### Step 1: Data Reception (Input)
The system must be able to receive client information in two primary formats:
1.  **Text**: JSON structure, Form data, or Direct String input.
2.  **Image**: OCR-ready images (ID cards, Forms) containing client details.

**Failure Criteria:**
- If input is unreadable or missing essential fields (Name, ID), the process MUST halt immediately (Fast Fail).
