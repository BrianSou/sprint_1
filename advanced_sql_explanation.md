# Advanced SQL Explanation

## 1. Age Buckets (CASE)

I used `CASE` to group unresolved complaints based on how many days they have been open.

- **0–7 days:** Complaints open for up to 7 days.
- **8–30 days:** Complaints open for 8 to 30 days.
- **31+ days:** Complaints open for more than 30 days.

I excluded closed complaints and calculated age using the difference between today's date and `received_at`.

I tested the boundaries using 7, 8, 30, and 31 days. All four returned the correct buckets.

**Results (October 23, 2026):** 1 complaint in 0–7 days, 0 in 8–30 days, and 9 in 31+ days.

**Limitation:** Results change depending on the date the query runs.

## 2. Repeat Complainants (CTE)

I used CTEs to find customers who submitted more than one complaint and check whether their complaints were escalated.

- `repeat_complainants` counts complaints per customer and keeps customers with more than one.
- `escalation_context` checks whether a complaint has an `ESCALATED` review decision.

I joined these results to show each repeat customer's complaints and escalation information.

**Results:** CUS001 was the only repeat customer, with 2 complaints (CMP001 and CMP011). Neither was escalated.

**Limitation:** Escalations are identified using the review decisions, so escalations not recorded there may be missed.

## 3. Latest Complaint Status (ROW_NUMBER)

I used `ROW_NUMBER()` to find the latest recorded status for each complaint.

- `PARTITION BY complaint_id` separates the history records for each complaint.
- `ORDER BY changed_at DESC` puts the newest status first.
- `history_id DESC` breaks ties when timestamps are the same.
- `ROW_NUMBER()` assigns numbers, with 1 being the latest record.

I then selected row 1 for each complaint.

**Results:** 10 complaints had status-history records. CMP011 had no history record.

**Limitation:** Complaints without status history have NULL values for their latest history status.

## 4. Customer Ranking (RANK)

I counted each customer's complaints and ranked them from highest to lowest.

- `COUNT(*)` counts complaints per customer.
- `RANK()` ranks customers based on their complaint count.
- `ORDER BY complaint_count DESC` puts customers with the most complaints first.
- `ROW_NUMBER()` with `customer_id` breaks ties for a consistent display order.

Customers with the same complaint count receive the same rank.

**Results:** CUS001 ranked 1st with 2 complaints. The other 9 customers tied for 2nd with 1 complaint each.

**Limitation:** `RANK()` allows ties, so rank numbers can be skipped.

## Validation

I checked the query results against the database.

- Age buckets correctly account for all 10 unresolved complaints.
- All four boundary tests passed.
- The repeat-customer query correctly identified CUS001.
- The latest-status query returned 11 complaints, including the one without status history.
- The ranking query returned 10 customers with the correct complaint counts and ranks.