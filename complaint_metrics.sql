-- Complaint volume by status, category

-- status volume
SELECT
    status,
    COUNT(*) AS complaint_count
FROM complaint
GROUP BY status;

-- category volume
SELECT
    category,
    COUNT(*) AS complaint_count
FROM complaint
GROUP BY category;

-- month volume
SELECT
    strftime('%Y-%m', received_at) AS month,
    COUNT(*) AS complaint_count
FROM complaint
GROUP BY month
ORDER BY month;


-- Open and escalated backlog

-- open backlog
SELECT COUNT(*) AS open_backlog
FROM complaint
WHERE status IN ('OPEN', 'IN_PROGRESS', 'UNDER_REVIEW');

-- escalated backlog
SELECT COUNT(*) AS escalated_backlog
FROM complaint c
WHERE c.status IN ('OPEN', 'IN_PROGRESS', 'UNDER_REVIEW')
AND EXISTS (
    SELECT 1
    FROM review_request rr
    JOIN review_decision rd
        ON rr.review_request_id = rd.review_request_id
    WHERE rr.complaint_id = c.complaint_id
        AND rd.decision = 'ESCALATED'
);


-- Distinct affected customers

SELECT
    COUNT(DISTINCT customer_id) AS affected_customers
FROM complaint;


-- average closed-case resolution days by category
WITH latest_closure AS (
    SELECT
        complaint_id,
        MAX(changed_at) AS closed_at
    FROM complaint_status_history
    WHERE new_status = 'CLOSED'
    GROUP BY complaint_id
)

SELECT
    c.category,
    COUNT(*) AS closed_complaints,
    ROUND(
        AVG(julianday(h.closed_at) - julianday(c.received_at)),
        2
    ) AS avg_resolution_days
FROM complaint c
JOIN latest_closure h
    ON c.complaint_id = h.complaint_id
WHERE c.status = 'CLOSED'
    AND julianday(h.closed_at) >= julianday(c.received_at)
GROUP BY c.category;