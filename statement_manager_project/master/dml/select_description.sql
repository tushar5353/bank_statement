SELECT
  row_sha,
  description
FROM <MASTER_DB>.<MASTER_TRANSACTIONS>
WHERE
  (category IS NULL
   OR
   category = 'unknown'
   OR
   info IS NULL
   OR
   info = 'unknown'
  )
AND bank_name = '<BANKNAME>';
