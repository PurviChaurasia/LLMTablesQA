import sqlite3
import os
import pandas as pd
import json
from openai import OpenAI
import random
from prompts import generate_queries_prompt, generate_queries_for_like_prompt, query_to_nl_question_prompt
from templates import query_templates, like_eg, like_queries

def csv_folder_to_database_custom_schema(folder_path, db_path):
    """
    Creating Database from CSV File Folders
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            table_name = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
            cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name}(
                        day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
                        month TEXT NOT NULL,
                        year INTEGER NOT NULL CHECK (year BETWEEN 1800 AND 2100),
                        dayname TEXT NOT NULL,
                        season INTEGER NOT NULL,
                        stadium TEXT NOT NULL,
                        city TEXT NOT NULL,
                        state TEXT NOT NULL,
                        attendance INTEGER NOT NULL,
                        capacity INTEGER NOT NULL,
                        summary TEXT
                    )
                """)
            print(f"Custom schema applied for table '{table_name}'.")

            if 'game_id' in df.columns:
                df = df.drop(columns=['game_id'])

            for _, row in df.iterrows():
                placeholders = ', '.join(['?'] * len(row))
                column_names = ', '.join(row.index)
                insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
                cursor.execute(insert_query, tuple(row))

    conn.commit()
    print("All CSV files have been successfully imported with the custom schema.")
    return conn

def check_tables_in_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables in the database:", tables)
    conn.close()

def get_table_schema_and_rows(table_name, db_path):
    # Get schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()
    schema_dict = {col[1]: col[2] for col in schema}
    
    # Get sample rows
    query = f"SELECT * FROM {table_name} LIMIT 5"
    df = pd.read_sql_query(query, conn)
    return schema_dict, df


def generate_queries(table_name, schema, rows):
    """
    Function to generate queries by replacing placeholders in query templates for a single table 
    """
    row_samples = [rows.sample(1, random_state=random.randint(1, 1000)).to_dict(orient="records")[0] for _ in range(5)]
    selected_template = random.choice(random.choice(query_templates))
    selected_template = selected_template.format(table=table_name)
    formatted_prompt = generate_queries_prompt.format(
        table_name=table_name,
        schema=json.dumps(schema, indent=4),
        row_samples=json.dumps(row_samples, indent=4),
        template=selected_template
    )
    messages = [
        {"role": "system", "content": "Act as an expert in SQL and databases. Please give valid output JSON."},
        {"role": "user", "content": formatted_prompt}
    ]

    chat_completion, *_ = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages,
        response_format={"type": "json_object"}

    ).choices
    content = chat_completion.message.content
    reply = json.loads(content)
    return reply

def generate_queries_for_like(table_name, schema, rows):
    """
    Function to generate queries by replacing placeholders in query templates for a single table 
    """
    row_samples = [rows.sample(1, random_state=random.randint(1, 1000)).to_dict(orient="records")[0] for _ in range(5)]
    selected_template = random.choice(like_queries)
    examples = random.sample(like_eg, 4)
    formatted_prompt = generate_queries_for_like_prompt.format(
        table_name=table_name,
        schema=json.dumps(schema, indent=4),
        row_samples=json.dumps(row_samples, indent=4),
        template=selected_template,
        example_1=examples[0],
        example_2=examples[1],
        example_3=examples[2],
        example_4=examples[3]
    )
    messages = [
        {"role": "system", "content": "Act as an expert in SQL and databases. Please give valid output JSON."},
        {"role": "user", "content": formatted_prompt}
    ]

    chat_completion, *_ = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages,
        response_format={"type": "json_object"}

    ).choices
    content = chat_completion.message.content
    reply = json.loads(content)
    return reply


def process_all_tables_and_save_simple(db_path, output_file):
    """
    Scaled function to generate queries on all tables in the database and save to a json
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    final_result = []

    for table_name in tables:
        for i in range(3):
            print(f"  Generating queries for table '{table_name}', iteration {i + 1}")
            schema, rows = get_table_schema_and_rows(table_name, db_path)
            queries_json = generate_queries(table_name, schema, rows)
            for query in queries_json["queries"]:
                normalized_query = {k.lower(): v for k, v in query.items()}
                final_result.append({
                    "table_name": normalized_query.get("table", table_name), 
                    "query": normalized_query.get("query", "Unknown Query")  
                })
    conn.close()
    with open(output_file, "w") as f:
        json.dump(final_result, f, indent=4)
    
    print(f"JSON output saved to {output_file}")
    return final_result


def execute_queries_and_update_json(db_path, input_json_file, output_json_file):
    """
    Save executed results of generated queries to the same json
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    with open(input_json_file, "r") as f:
        queries_json = json.load(f)
    updated_queries = []
    for entry in queries_json:
        table_name = entry["table_name"]
        query = entry["query"]
        
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            
            if len(result) == 1 and len(result[0]) == 1:
                result_value = result[0][0]
            else:
                result_value = str(result)
        except Exception as e:
            result_value = f"Error: {str(e)}"

        updated_queries.append({
            "table_name": table_name,
            "query": query,
            "result": result_value
        })
    conn.close()
    
    # Save the updated JSON to a file
    with open(output_json_file, "w") as f:
        json.dump(updated_queries, f, indent=4)
    
    print(f"Updated JSON with results saved to {output_json_file}")
    return updated_queries



def convert_sql_to_natural_language(input_json_file, output_json_file):
    """
    Function to convert generated SQL Queries to Natural Language Questions
    """
    with open(input_json_file, "r") as f:
        queries_json = json.load(f)
    
    updated_json = []
    
    for entry in queries_json:
        sql_query = entry["query"]
        table_name = entry["table_name"]
        result = entry.get("result", None)

        formatted_prompt = query_to_nl_question_prompt.format(
            sql_query=sql_query
        )
        
        messages = [
        {"role": "system", "content": "Act as an expert data scientist skilled in SQL and natural language processing."},
        {"role": "user", "content": formatted_prompt}
        ]
        
        try:  
            chat_completion, *_ = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    messages=messages
                ).choices
            content = chat_completion.message.content     
            question = content.replace("Question: ", "").strip()
        except Exception as e:
            question = f"Error generating question: {str(e)}"
        
        updated_json.append({
            "table_name": table_name,
            "query": sql_query,
            "result": result,
            "question": question
        })
    with open(output_json_file, "w") as f:
        json.dump(updated_json, f, indent=4)
    
    print(f"Updated JSON with natural language questions saved to {output_json_file}")
    return updated_json

# ------------ Evaluation Code -------------------------#
def convert_to_pipe_format(path_to_csv):
    df = pd.read_csv(path_to_csv)
    string = '/*\n'
    col_list = df.columns.values.tolist()
    string += 'col : ' + ' | '.join(df.columns) + '\n'
    for row_id, row in df.iterrows():
        string += f'row {row_id} : '
        for column_id, header in enumerate(df.columns):
            string += str(row[header])
            if column_id != len(df.columns) - 1:
                string += ' | '
        string += '\n'
    string += '*/\n'
    string += f'columns:{col_list}\n'
    return string

def generate_short_answer(table, question):
    answer_prompt = f"""
    Here is the table to answer this question. Answer the question in 3-4 words max.
    {table}
    Question: {question}
    The answer is: 
    """
    messages = [
        {"role": "system", "content": "You are an expert in answering questions from tabular data."},
        {"role": "user", "content": answer_prompt}
    ]
    completion = client.chat.completions.create(
        model="gpt-4o-mini", 
        temperature=0,
        messages=messages
    )
    generated_answer = completion.choices[0].message.content.strip()
    return generated_answer

def evaluate_qa_pair(qa_pair, correct_answers_list):
    table_path = rf"D:\LLMTables\Question Generation\test\{qa_pair['table_name']}.csv"
    table = convert_to_pipe_format(table_path)
    question = qa_pair['question']
    generated_answer = generate_short_answer(table, question)
    correct_answer = qa_pair["result"]
    if generated_answer == correct_answer:
        correct_answers_list.append(qa_pair)
        return True
    else:
        print("incorrect answer")
        print(question)
        print("actual: " + correct_answer)
        print("generated: " + generated_answer)
        return False
    
def process_evaluation(json_data):
    total_questions = len(json_data)
    print("total questions: " + str(total_questions))
    correct_answers = 0
    incorrect_answers = []

    for qa_pair in json_data:
        if evaluate_qa_pair(qa_pair, correct_answers_list=[]):
            correct_answers += 1
        else:
            incorrect_answers.append(qa_pair)
    accuracy = (correct_answers / total_questions) * 100
    return correct_answers, accuracy, incorrect_answers

def save_incorrect_answers(incorrect_answers, output_path):
    with open(output_path, "w") as json_file:
        json.dump(incorrect_answers, json_file, indent=4)
    print(f"Incorrectly answered questions saved to {output_path}")

def evaluation_pipeline(input_json_path, incorrect_output_json_path):
    with open(input_json_path, "r") as file:
        json_data = json.load(file)
    correct_answers, accuracy, incorrect_answers = process_evaluation(json_data)
    print(f"Total Correct Answers: {correct_answers}")
    print(f"Accuracy: {accuracy:.2f}%")
    save_incorrect_answers(incorrect_answers, incorrect_output_json_path)

def process_folder(folder_path):
    """
    Process a single folder containing CSVs to generate all outputs.
    """
    db_path = os.path.join(folder_path, "database.db")
    output_simple_queries = os.path.join(folder_path, "queries_output.json")
    output_queries_with_results = os.path.join(folder_path, "queries_with_results.json")
    output_natural_language = os.path.join(folder_path, "final_output.json")

    # Step 1: Convert CSVs to a database
    conn = csv_folder_to_database_custom_schema(folder_path, db_path)

    # Step 2: Check tables in DB
    check_tables_in_db(db_path)

    # Step 3: Generate SQL Queries throughout the DB
    process_all_tables_and_save_simple(db_path, output_simple_queries)

    # Step 4: Update JSON with executed SQL results
    execute_queries_and_update_json(db_path, output_simple_queries, output_queries_with_results)

    # Step 5: Convert SQL queries to natural language
    convert_sql_to_natural_language(output_queries_with_results, output_natural_language)

    print(f"Processing for folder {folder_path} completed.")


def process_all_subfolders(parent_folder):
    """
    Process each subfolder in the parent folder containing CSVs.
    """
    for subfolder_name in os.listdir(parent_folder):
        subfolder_path = os.path.join(parent_folder, subfolder_name)
        if os.path.isdir(subfolder_path):
            print(f"Processing folder: {subfolder_path}")
            process_folder(subfolder_path)

# -----------------Example usage (Uncomment according to need)-----------------
# Parent folder containing subfolders (e.g., `1`, `2`, `3`)
parent_folder = r"D:\LLMTables\split\train\test_2"

# Process all subfolders
client = OpenAI()
process_all_subfolders(parent_folder)

# # ----------For updating the DB and converting CSVs to tables in DB-----------
# conn = csv_folder_to_database_custom_schema(folder_path, db_path)

# # ---------Print Tables in DB-------------
# check_tables_in_db(db_path)

# # -----------Ad-hoc Query Generation on single table---------
# # table_name = "sportset_2"
# # schema, rows = get_table_schema_and_rows(table_name, db_path)
# # queries_json = generate_queries(table_name, schema, rows)
# # print("Generated JSON Output:")
# # print(json.dumps(queries_json, indent=4))

# # -----------Generate SQL Queries Throughout the DB---------------
# output_file = r"D:\LLMTables\LLMTablesQA\Question Generation\SQL\test_scaled_simple_queries_output.json"  # Path to save the JSON
# all_tables_result = process_all_tables_and_save_simple(db_path, output_file)
# print("Generated Simplified JSON Output for All Tables")
# # print(json.dumps(all_tables_result, indent=4))

# # ---------Update JSON with executed SQL Result-------------
# input_json_file = r"D:\LLMTables\LLMTablesQA\Question Generation\SQL\test_scaled_simple_queries_output.json"
# output_json_file = r"D:\LLMTables\LLMTablesQA\Question Generation\SQL\test_scaled_queries_with_results.json"  # Output JSON
# updated_result = execute_queries_and_update_json(db_path, input_json_file, output_json_file)
# # print("Updated JSON with Results:")
# # print(json.dumps(updated_result, indent=4))

# # -----------Convert SQL Query to Natural Langauge for the entire JSON----------------
# input_json_file = r"D:\NSFQA\Question Generation\SQL\queries_with_results.json"  # Input JSON
# output_json_file = r"D:\NSFQA\Question Generation\SQL\natural_language_output.json"  # Output JSON
# updated_json = convert_sql_to_natural_language(input_json_file, output_json_file)
# # print("Updated JSON with Natural Language Questions:")
# # print(json.dumps(updated_json, indent=4))

# # -----------Evaluation-----------------
# # input_json_path = r"D:\LLMTables\Question Generation\test\natural_language_output.json"  
# # incorrect_output_json_path = r"D:\LLMTables\Question Generation\test\incorrect_answers.json"  
# # evaluation_pipeline(input_json_path, incorrect_output_json_path)



