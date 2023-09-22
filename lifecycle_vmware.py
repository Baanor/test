import json
import requests
import mysql.connector

# Function to fetch JSON data from URL
def fetch_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from URL. Status code: {response.status_code}")
        return None

# Function to insert data into MySQL database
def insert_data_into_mysql(data):
    try:
        connection = mysql.connector.connect(
            host="172.9.0.2",
            user="nocobase",
            password="nocobase",
            database="nocobase"
        )
        
        cursor = connection.cursor()

        for product in data["data"]["productLifecycle"]:
            productRelease = product["productRelease"]
            endOfGeneralSupport = product["endOfGeneralSupport"]
            generalAvailability = product["generalAvailability"]

            # Insert data into MySQL table
            sql = "INSERT INTO lifecycle_vmware (productRelease, endOfGeneralSupport, generalAvailability) VALUES (%s, %s, %s)"
            values = (productRelease, endOfGeneralSupport, generalAvailability)
            cursor.execute(sql, values)

        connection.commit()
        print("Data inserted successfully into MySQL database.")

    except mysql.connector.Error as error:
        print(f"Error inserting data into MySQL database: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    json_url = "https://www.virten.net/repo/vmwareProductLifecycle.json"
    json_data = fetch_json_data(json_url)

    if json_data:
        insert_data_into_mysql(json_data)
