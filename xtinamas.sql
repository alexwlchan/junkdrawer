WITH RECURSIVE
  cnt(x)
AS
  (
    VALUES(1)
    UNION ALL
    SELECT x+1 FROM cnt
    LIMIT length("Happy Xtina-mas 2019!")
  )
SELECT
  sum(unicode(substr("Happy Xtina-mas 2019!", x, 1)) / 100.0)
FROM cnt;
