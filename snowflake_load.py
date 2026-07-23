import os
import snowflake.connector

def load_into_snowflake():
    print("Connecting to Snowflake data warehouse...")
    
    # Establish secure connection using environment variables
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER", "NARESH7822"),
        password=os.getenv("SNOWFLAKE_PASSWORD", "Sadie@13102004"),
        account=os.getenv("SNOWFLAKE_ACCOUNT", "EO22455"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "DEV_DB"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    )
    
    cursor = conn.cursor()
    try:
        # Execute the Snowflake ELT command pointing to your S3 stage
        copy_query = """
            COPY INTO target_users_table
            FROM @my_s3_stage/raw/extracted_users.json
            FILE_FORMAT = (TYPE = 'JSON');
        """
        cursor.execute(copy_query)
        print("SUCCESS: Data successfully loaded into Snowflake warehouse table!")
    except Exception as e:
        print(f"ERROR: Snowflake load failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_into_snowflake()