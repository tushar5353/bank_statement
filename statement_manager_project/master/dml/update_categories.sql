UPDATE <MASTER_DB>.<MASTER_TRANSACTIONS>
SET
  category = "<CATEGORY>",
  info = "<INFO>"
WHERE
  row_sha = "<ROW_SHA>";
