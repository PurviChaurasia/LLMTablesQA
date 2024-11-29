generate_queries_prompt = """
Read the table schema and 5 rows given from the table carefully and understand it correctly - 
         
         Table Schema:
         {schema}

         ROW DATA:
         {row_samples}

         SQL TEMPLATE:

         SELECT [column] FROM {table_name} WHERE [condition1] AND [condition2]

         Instruction:
            1. Please use the information from the table and data provided to fill in the placeholders in the template. Each SQL query should only return a single result using either:
            - A specific column (e.g., city, attendance, capacity, etc.)
            - An aggregate function (e.g., COUNT(), SUM(), MAX(), etc.)

            2. Follow the template given and try to fill in the placeholders in a way that can lead to logical and complex queries.
            3. Add HAVING, LIKE and DISTINCT to the template to generate queries as you wish. Note that HAVING should be followed by a GROUP BY always.
            4. Make use of AND,OR and NOT at will in the conditions.
            5. If you're adding LIMIT make sure it follows a meaningful ORDER BY so that the answer is not dependent on internal ordering of the database.
            6. Try to make the query set as diverse as possible while not deviating much from the template given to you.
            7. Ensure that the queries generate deterministic answers, such as a single count, maximum, or specific column value (e.g., "How many games were held in Orlando?").

            Example:
            1. SELECT city FROM sportset_west_30_4 WHERE dayname = 'Monday' AND season = 2014 AND capacity > attendance
            2. SELECT DISTINCT stadium FROM sportset_west_30_4 WHERE year = 2015 OR year = 2014
            
            Please STRICTLY follow the Response format while answering :
            Query: <Single Liner SQL Query>
            Table: {table_name}

            Generate 5 such SQL queries.
"""

query_to_nl_question_prompt = """
You are an expert data scientist skilled in SQL and natural language processing. Your task is to convert SQL queries into natural language questions. 

        Here is the SQL Query: 
        {sql_query}
        The questions should:
        - Clearly represent the intent of the SQL query.
        - Translate technical terms, column headers, and values into natural, descriptive forms.
        - Avoid technical jargon unless absolutely necessary.
        - Ensure the question retains the same scope and meaning as the SQL query to avoid altering the query's answer.
        - Try to craft intuitive and complex questions from the query

        Example:
        SQL: SELECT COUNT(game_id) FROM sportset_2 WHERE city = 'Orlando' AND year = 2015
        Output: In 2015, how many games were hosted by the city of Orlando?

        SQL: SELECT DISTINCT city FROM sportset_northeast_30_1 WHERE state = 'Massachusetts' AND capacity > 18000
        Output: Amongst various cities in Masschusets which ones are home to stadiums with a seating capacity exceeding 18,000?

        SQL: SELECT SUM(attendance) FROM sportset_northeast_30_1 WHERE year = 2015 AND month LIKE 'April%'
        Output: What was the total attendance recorded for sport events in the northeastern states in April 2015?

        Please convert this SQL query into a single natural language question. Ensure the column headers and values are human-readable. 
        Respond STRICTLY in the following format:
        Question: <Natural Language Question
"""