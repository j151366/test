/*
https://www.w3schools.com/sql/trysql.asp?filename=trysql_asc
*/

-- 
SELECT
*
FROM Customers
INNER JOIN (SELECT City, Country, COUNT(*)
FROM Customers
GROUP BY City, Country
HAVING COUNT(*) = 1)
USING(City, Country)


--
SELECT
*
FROM Customers
INNER JOIN
  (SELECT City, COUNT(*)
  FROM Customers
  GROUP BY City
  HAVING COUNT(*) = 1)
USING(City)
INNER JOIN
  (SELECT Country, COUNT(*)
  FROM Customers
  GROUP BY Country
  HAVING COUNT(*) = 1)
USING(Country)


--
SELECT
*
FROM Customers
WHERE 
  City IN (SELECT City FROM (SELECT City, COUNT(*)
  FROM Customers
  GROUP BY City
  HAVING COUNT(*) = 1))
AND
  Country IN (SELECT Country FROM (SELECT Country, COUNT(*)
  FROM Customers
  GROUP BY Country
  HAVING COUNT(*) = 1))



