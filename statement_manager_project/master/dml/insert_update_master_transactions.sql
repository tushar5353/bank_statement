INSERT INTO <MASTER_DB>.<MASTER_TRANSACTIONS>(
  id, row_sha, date_time, description, category, info,
  amount, transaction_type, balance, bank_name, created_at, 
  updated_at
) 
SELECT 
  NULL AS id, 
  st.row_sha AS row_sha,
  st.date_time AS date_time, 
  st.description AS description,
  st.category AS category,
  st.info AS info,
  CASE
    WHEN st.debit is NULL
      THEN st.credit
      ELSE -st.debit
    END as amount,
  CASE
    WHEN st.debit is NULL
      THEN 'credit'
      ELSE 'debit'
    END as transaction_type,
  st.balance AS balance, 
  st.bank_name AS bank_name, 
  st.created_at AS created_at, 
  st.updated_at AS updated_at 
FROM 
  <STAGE_DB>.<STAGE_TRANSACTIONS> st
  LEFT JOIN <MASTER_DB>.<MASTER_TRANSACTIONS> mt ON st.row_sha = mt.row_sha 
WHERE 
  mt.row_sha IS NULL 
  AND st.bank_name = '<BANKNAME>' 
ORDER BY 
  st.id;
