-- Fix listing statuses to show star button
-- Run this if you can't run the Python script

-- Check current listing statuses
SELECT
    LISTING_ID,
    LISTING_TITLE,
    LISTING_STATUS,
    IS_FEATURED,
    CASE
        WHEN IS_FEATURED = 0 AND LISTING_STATUS = 'active' THEN '⭐ Star button VISIBLE'
        WHEN IS_FEATURED = 1 THEN '❌ Already featured'
        WHEN LISTING_STATUS != 'active' THEN '❌ Status not active'
        ELSE '❌ Unknown issue'
    END AS STAR_BUTTON_STATUS
FROM LISTINGS
ORDER BY LISTING_ID;

-- Update all pending listings to active (for testing)
UPDATE LISTINGS
SET LISTING_STATUS = 'active'
WHERE LISTING_STATUS = 'pending';

-- Verify the fix
SELECT
    LISTING_ID,
    LISTING_TITLE,
    LISTING_STATUS,
    IS_FEATURED,
    '⭐ Star button should now be visible!' AS STATUS
FROM LISTINGS
WHERE LISTING_STATUS = 'active' AND IS_FEATURED = 0;

-- Check if you have any featured pricing plans
SELECT
    PRICING_ID,
    PRICING_NAME,
    PLAN_PRICE,
    DURATION_DAYS,
    IS_FEATURED,
    IS_ACTIVE
FROM PRICING_PLANS
WHERE IS_FEATURED = 1 AND IS_ACTIVE = 1;
