SELECT 1.0*COUNT(DISTINCT [物件].[物件コード
]) AS 物件数, Sum(棟別総戸数) AS 供給量, Sum(棟別総戸数 - レッツ戸数 - 現時点契約数) AS 在庫数, SWITCH ( ([交通徒歩orバス] = 1) , 歩 , ([交通徒歩orバス] = 2) , バス , True, other ) AS Koutu
FROM BUKKEN;

