Semi-join
You are now going to use the concept of a semi-join to identify languages spoken in the Middle East.

Instructions 2/3
35 XP
2
3
Comment out the answer to the previous tab by surrounding it in /* and */. You'll come back to it!
Below the commented code, select only unique languages by name appearing in the languages table.
Order the resulting single field table by name in ascending order.
Take Hint (-10 XP)

/*
SELECT code
FROM countries
WHERE region = 'Middle East';
*/

SELECT DISTINCT name
FROM languages
ORDER BY name;

Now combine the previous two queries into one query:

Add a WHERE IN statement to the SELECT DISTINCT query, and use the commented out query from the first instruction in there. That way, you can determine the unique languages spoken in the Middle East.
Carefully review this result and its code after completing it. It serves as a great example of subqueries, which are the focus of Chapter 4.

Take Hint (-9 XP)

SELECT country.code
FROM countries AS country
WHERE country.region = 'Middle East';

Relating semi-join to a tweaked inner join
Let's revisit the code from the previous exercise. Sometimes problems solved with semi-joins can also be solved using an inner join.

What is missing from the code at the bottom of the editor to get it to match with the correct answer produced by the commented out
code at the top of the editor, which retrieves languages spoken in the Middle East?

Instructions
50 XP
Possible Answers
HAVING instead of WHERE
DISTINCT
UNIQUE


Diagnosing problems using anti-join

Another powerful join in SQL is the anti-join. It is particularly useful in identifying which records are causing an
incorrect number of records to appear in join queries.

You will also see another example of a subquery here, as you saw in the first exercise on semi-joins. Your goal is to
identify the currencies used in Oceanian countries!

Instructions 1/3
35 XP

Begin by determining the number of countries in countries that are listed in Oceania using SELECT, FROM, and WHERE.

Complete an inner join with countries AS c1 on the left and currencies AS c2 on the right to get the different currencies
used in the countries of Oceania.

Match ON the code field in the two tables.
Include the country code, country name, and basic_unit AS currency.
Observe query result and make note of how many different countries are listed here.





Note that not all countries in Oceania were listed in the resulting inner join with currencies. Use an anti-join to determine
which countries were not included!

Use NOT IN and (SELECT code FROM currencies) as a subquery to get the country code and country name for the Oceanian countries
that are not included in the currencies table.









