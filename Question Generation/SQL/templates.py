#--------------------------- TEMPLATES ----------------------------------------------------------------------
basic_selection = [
    "SELECT [column] FROM [table] WHERE [conditions]",
    "SELECT [column] FROM [table] WHERE [conditions] ORDER BY [column]",
    "SELECT [column] FROM [table] WHERE [conditions] ORDER BY [ ] LIMIT [ ]"
]
and_queries = [
    "SELECT [column] FROM [table] WHERE [condition1] AND [condition2]",
    "SELECT [column] FROM [table] WHERE [condition1] AND [condition2] ORDER BY [column] LIMIT [n]"
]

or_queries = [
    "SELECT [column] FROM [table] WHERE [condition1] OR [condition2]",
    "SELECT [column] FROM [table] WHERE [condition1] OR [condition2] ORDER BY [column] LIMIT [n]",
    "SELECT [column] FROM [table] WHERE [condition1] OR [condition2] ORDER BY [column]"
]

advanced_and_or_queries = [
    "SELECT [column] FROM [table_name] WHERE [condition1 AND condition2 AND condition3]",
    "SELECT [column] FROM [table_name] WHERE [condition1] OR [condition2] OR [condition3]",
    "SELECT [column] FROM [table_name] WHERE [condition1] OR [condition2] OR [condition3] ORDER BY [column]",
    "SELECT [column] FROM [table_name] WHERE [condition1 AND condition2] OR [condition3]",
    "SELECT [column] FROM [table_name] WHERE [condition1 AND condition2] OR [condition3 AND column4]",
    "SELECT [column] FROM [table_name] WHERE [condition1 OR condition2] AND [condition3 OR column4]",
]

distinct_queries = [
    "SELECT DISTINCT [column] FROM [table] WHERE [conditions]",
    "SELECT DISTINCT [column] FROM [table] WHERE [conditions] ORDER BY [ ]",
    "SELECT DISTINCT [column] FROM [table] WHERE [conditions] ORDER BY [ ] LIMIT [n]"
]

aggregation_queries = [
    "SELECT MAX/MIN/AVG/SUM/COUNT([column]) FROM [table] WHERE [conditions]",
    "SELECT MAX/MIN/AVG/SUM/COUNT([column]) FROM [table] WHERE [conditions] LIMIT [ ]",
    "SELECT MAX/MIN/AVG/SUM/COUNT([column]) FROM [table] WHERE [conditions] ORDER BY [ ]"
]

case_queries = [
    "SELECT [column], CASE WHEN [condition1] THEN [value1] WHEN [condition2] THEN [value2] ELSE [default value] END AS [new column] FROM [table] WHERE [conditions]",
]

like_queries = [
    "SELECT [column] FROM [table] WHERE [column] LIKE '%pattern%'",
    "SELECT [column] FROM [table] WHERE [column] NOT LIKE '%pattern%'",
    "SELECT [column] FROM [table] WHERE [column] LIKE '%pattern1%' OR [column] LIKE '%pattern2%'",
    "SELECT [column] FROM [table] WHERE [column] NOT LIKE '%pattern1%' AND [column] LIKE '%pattern2%'",
    "SELECT [column] FROM [table] WHERE [column] LIKE '%pattern%' AND [another_column] = [value]",
    "SELECT [column] FROM [table] WHERE [column] LIKE '%pattern%' OR [another_column] BETWEEN [value1] AND [value2]",
    "SELECT [column] FROM [table] WHERE [column] LIKE '%pattern%' ORDER BY [column]",
    "SELECT [column] FROM [table] WHERE [column] LIKE '%pattern%' ORDER BY [column] LIMIT [n]",
]

group_by_queries = [
    # Basic Group By Queries
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [condition] GROUP BY [column1]",
    "SELECT [column1], COUNT(*) FROM [table] WHERE [condition] GROUP BY [column1]",
    "SELECT DISTINCT [column1], [aggregation]([column2]) FROM [table] WHERE [conditions] GROUP BY [column1]",
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [condition] GROUP BY [column1] ORDER BY [aggregation]([column2]) LIMIT [n]"
    
    # Group By with AND Conditions
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [condition1] AND [condition2] GROUP BY [column1]",
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [condition1] AND [condition2] GROUP BY [column1] HAVING COUNT([column2]) > [value]",
    
    # Group By with OR Conditions
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [condition1] OR [condition2] GROUP BY [column1]",
    "SELECT [column1], COUNT(*) FROM [table] WHERE [condition1] OR [condition2] GROUP BY [column1]",
    
    # Group By with LIKE Conditions
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [column1] LIKE '%pattern%' GROUP BY [column1]",
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [column1] NOT LIKE '%pattern%' GROUP BY [column1]",
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [column1] LIKE '%pattern%' AND [column2] BETWEEN [value1] AND [value2] GROUP BY [column1]",
    "SELECT [column1], COUNT(*) FROM [table] WHERE [column1] LIKE '%pattern%' GROUP BY [column1] HAVING COUNT(*) > [value]",
    "SELECT [column1], [aggregation1]([column2]) AS [alias1], [aggregation2]([column3]) AS [alias2] FROM [table] GROUP BY [column1] HAVING [aggregation1]([column2]) > [value]",
    "SELECT [column1], [aggregation]([column2]) FROM [table1] WHERE [column1] IN (SELECT [column3] FROM [table2] WHERE [condition]) GROUP BY [column1]",
    "SELECT [column1], [aggregation]([column2]) FROM [table1] WHERE [column1] IN (SELECT [column3] FROM [table2] WHERE [condition]) GROUP BY [column1] ORDER BY [aggregation]([column2]) DESC LIMIT [n]",

    # Group By with CASE Statements
    "SELECT [column1], CASE WHEN [condition1] THEN [value1] WHEN [condition2] THEN [value2] ELSE [default_value] END AS [new_column] FROM [table] GROUP BY [column1]",
    "SELECT [column1], COUNT(CASE WHEN [condition1] THEN 1 ELSE NULL END) AS count_condition1 FROM [table] GROUP BY [column1]",
    
    # Group By with Subqueries
    "SELECT [column1], [aggregation]([column2]) FROM [table] WHERE [column1] IN (SELECT [sub_column] FROM [sub_table] WHERE [sub_condition]) GROUP BY [column1]",
    "SELECT [column1], COUNT(*) FROM [table] WHERE EXISTS (SELECT 1 FROM [sub_table] WHERE [table].[column] = [sub_table].[column] AND [sub_condition]) GROUP BY [column1]",

    "SELECT [column1], [aggregation]([column2]) FROM [table_name] WHERE [condition1 AND condition2 AND condition3] GROUP BY [column1]",
    "SELECT [column1], [aggregation]([column2]) FROM [table_name] WHERE [condition1 AND condition2 AND condition3] GROUP BY [column1] ORDER BY [column1] LIMIT [n]"
]

# ---------------------------------- EXAMPLES -------------------------------------------------
basic_queries_eg = ["SELECT COUNT(*) FROM sportset_2 WHERE city = 'Orlando' AND attendance > 16000", 
                   "SELECT SUM(attendance) FROM sportset_2 WHERE stadium = 'Time Warner Cable Arena' AND year = 2014 GROUP BY year HAVING SUM(attendance) > 33000"
                   "SELECT city FROM sportset_2 WHERE season = 2014 AND dayname = 'Wednesday' ORDER BY capacity DESC LIMIT 1",
                   "SELECT COUNT(*) FROM sportset_midwest_30_8 WHERE city = 'Indianapolis' AND capacity > attendance",
                   "SELECT DISTINCT stadium FROM sportset_midwest_30_8 WHERE state = 'Minnesota' AND year = 2015",
                   "SELECT AVG(attendance) FROM sportset_northeast_30_1 WHERE state = 'New York' AND year = 2015",
                   "SELECT COUNT(DISTINCT city) FROM sportset_west_30_4 WHERE state = 'Utah' AND season = 2014",
                   "SELECT AVG(capacity) FROM sportset_coldtemp_30_13 WHERE season = 2014 GROUP BY city HAVING AVG(capacity) > 20000"]

and_queries_eg = ["SELECT COUNT(*) FROM sportset_2 WHERE city = 'Orlando' AND attendance > 16000", 
                   "SELECT SUM(attendance) FROM sportset_2 WHERE stadium = 'Time Warner Cable Arena' AND year = 2014 GROUP BY year HAVING SUM(attendance) > 33000"
                   "SELECT city FROM sportset_2 WHERE season = 2014 AND dayname = 'Wednesday' ORDER BY capacity DESC LIMIT 1",
                   "SELECT COUNT(*) FROM sportset_midwest_30_8 WHERE city = 'Indianapolis' AND capacity > attendance",
                   "SELECT DISTINCT stadium FROM sportset_midwest_30_8 WHERE state = 'Minnesota' AND year = 2015",
                   "SELECT AVG(attendance) FROM sportset_northeast_30_1 WHERE state = 'New York' AND year = 2015",
                   "SELECT COUNT(DISTINCT city) FROM sportset_west_30_4 WHERE state = 'Utah' AND season = 2014",
                   "SELECT AVG(capacity) FROM sportset_coldtemp_30_13 WHERE season = 2014 GROUP BY city HAVING AVG(capacity) > 20000"]

or_queries_eg = ["SELECT COUNT(*) FROM sportset_2 WHERE city = 'Orlando' OR city = 'Miami'",
                 "SELECT SUM(attendance) FROM sportset_2 WHERE month = 'November' OR month = 'February'",
                 "SELECT DISTINCT stadium FROM sportset_2 WHERE season = 2016 OR season = 2017",
                 "SELECT attendance FROM sportset_midwest_30_8 WHERE day = 4 OR month = 'February' ORDER BY attendance DESC",
                 "SELECT MAX(attendance) FROM sportset_midwest_30_8 WHERE city = 'New Orleans' OR stadium = 'Smoothie King Center'",
                 "SELECT dayname FROM sportset_midwest_30_8 WHERE year = 2016 AND season = 2016 GROUP BY dayname ORDER BY COUNT(*) DESC LIMIT 1",
                 "SELECT stadium, attendance FROM sportset_midwest_30_8 WHERE attendance > 16000 GROUP BY city"]

group_by_eg = ["SELECT MIN(capacity) FROM sportset_midwest_30_8 WHERE state = 'Ohio' AND season = 2017 GROUP BY city",
            "SELECT year, AVG(attendance) FROM sportset_midwest_30_8 WHERE month = 'February' GROUP BY year",
            "SELECT state, MAX(capacity) FROM sportset_midwest_30_8 GROUP BY state",
            "SELECT month, SUM(attendance) FROM sportset_midwest_30_8 WHERE year = 2016 GROUP BY month",
            "SELECT city, AVG(capacity) FROM sportset_midwest_30_8 GROUP BY city"]
