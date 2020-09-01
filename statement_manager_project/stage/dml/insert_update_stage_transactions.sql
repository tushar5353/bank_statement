INSERT INTO <STAGE_DB>.<STAGE_TRANSACTIONS>_temp(
  id, row_sha, date_time, description, 
  debit, credit, balance, bank_name, 
  created_at, updated_at
) 
SELECT 
  NULL AS id, 
  sha1(
    concat(
      ifnull(date, 'aaa'), 
      ifnull(description, 'aaa'), 
      ifnull(debit, 'aaa'), 
      ifnull(credit, 'aaa'), 
      ifnull(balance, 'aaa'), 
      '<BANKNAME>'
    )
  ) AS row_sha, 
  date, 
  description, 
  debit, 
  credit, 
  balance, 
  '<BANKNAME>' AS bank_name, 
  now() AS created_at, 
  now() AS updated_at 
FROM 
  <RAW_DB>.<TRANSACTIONS> 
ORDER BY 
  `index`;


INSERT INTO <STAGE_DB>.<STAGE_TRANSACTIONS>(
  id, row_sha, date_time, description, debit, 
  credit, balance, bank_name, created_at, 
  updated_at
) 
SELECT 
  NULL AS id, 
  tmp.row_sha AS row_sha, 
  tmp.date_time AS date_time, 
  tmp.description AS description, 
  tmp.debit AS debit, 
  tmp.credit AS credit, 
  tmp.balance AS balance, 
  tmp.bank_name AS bank_name, 
  tmp.created_at AS created_at, 
  tmp.updated_at AS updated_at 
FROM 
  <STAGE_DB>.<STAGE_TRANSACTIONS>_temp tmp 
  LEFT JOIN <STAGE_DB>.<STAGE_TRANSACTIONS> st ON tmp.row_sha = st.row_sha 
WHERE 
  st.row_sha IS NULL 
  AND tmp.bank_name = '<BANKNAME>' 
ORDER BY 
  tmp.id;

DROP TABLE IF EXISTS  <STAGE_DB>.<STAGE_TRANSACTIONS>_temp;
