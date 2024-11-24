generate_queries_prompt = """
Read the table schema and 5 rows given from the table carefully and understand it correctly - 
         
         Table Schema:
         {schema}

         ROW DATA:
         {row_samples}

         SQL TEMPLATE:

         SELECT [column] FROM {table_name} WHERE [condition1] AND [condition2]

         Instruction:
            Please use the information from the table and data provided to fill in the placeholders in the template. Each SQL query should only return a single result using either:

            - A specific column (e.g., city, attendance, capacity, etc.)
            - An aggregate function (e.g., COUNT(), SUM(), MAX(), etc.)
            Follow the template given and try to fill in the placeholders in a way that can lead to logical and complex queries.
            Ensure that the queries generate deterministic answers, such as a single count, maximum, or specific column value (e.g., "How many games were held in Orlando?").
            Generate 5 such SQL queries.
            
            Please follow the Response format while answering :
            Query: <Single Liner SQL Query>
            Table: {table_name}
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

        For example:
        SQL: SELECT COUNT(game_id) FROM sportset_2 WHERE city = 'Orlando' AND year = 2015
        Output: How many games took place in Orlando in the year 2015?

        Please convert this SQL query into a single natural language question. Ensure the column headers and values are human-readable. 
        
        Respond STRICTLY in the following format:
        Question: <Natural Language Question>
"""