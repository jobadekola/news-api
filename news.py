import requests
import json
import snowflake.connector

class SnowflakeIngester:
    def __init__(self, user, password, account):
        self.cnx = snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        )
        self.cursor = self.cnx.cursor()
        
    def create_table(self, table_name, columns):
        table_create_query = "CREATE TABLE {} ({});".format(table_name, columns)
        self.cursor.execute(table_create_query)
        
    def insert_data(self, table_name, data):
        for item in data:
            insert_query = "INSERT INTO {} VALUES ('{}', {});".format(table_name, item['data_col1'], item['data_col2'])
            self.cursor.execute(insert_query)
            
    def commit(self):
        self.cnx.commit()
        
    def close(self):
        self.cnx.close()
        
def extract_data(url):
    response = requests.get(url)
    return response.json()

def main():
    # Extract the data
    data = extract_data("API_URL")
    
    # Connect to Snowflake
    ingester = SnowflakeIngester("SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD", "SNOWFLAKE_ACCOUNT")
    
    # Create a table to store the data in Snowflake
    ingester.create_table("api_data", "data_col1 VARCHAR, data_col2 INTEGER")
    
    # Ingest the data into Snowflake
    ingester.insert_data("api_data", data)
    
    # Commit the changes
    ingester.commit()
    
    # Close the connection
    ingester.close()

if __name__ == "__main__":
    main()
