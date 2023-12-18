
import mysql.connector


def add_image_to_database(userID, imagefile):
    # Connect to the MySQL database
    db = mysql.connector.connect(
    host="69.23.75.181",
    port="3306",
    user="CMAdmin",
    password="Chucky123",
    database="brain_cancer_mock_data"
)
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # 
    
    # Prepare the SQL query
    values = imagefile
    query = "INSERT INTO image (imageFilePath) VALUES (%s);"
    print(query)

    # Execute the query
    cursor.execute(query, (values,))

    # Get a count of the number of images in the database
    cursor.execute("SELECT COUNT(*) FROM image")
    num_images = cursor.fetchone()[0]
    
    # update the image2user table
    query = "INSERT INTO usertoimage VALUES (%s, %s)"
    values = (userID, num_images)
    
    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    db.commit()
    
    # Close the cursor and database connection
    cursor.close()
    db.close()
    print("Image added to database")
    return

def update_user_result(userID, result):
    # Connect to the MySQL database
    db = mysql.connector.connect(
    host="192.168.0.63",
    port="3306",
    user="CMAdmin",
    password="Chucky123",
    database="brain_cancer_mock_data"
)
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()
    
    # Prepare the SQL query
    query = "UPDATE user SET results=%s WHERE userID=%s"
    values = (result, userID)
    
    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    db.commit()
    
    # Close the cursor and database connection
    cursor.close()
    db.close()
    return

# Debugging
# test_image = "C:\\Users\\chuck\\Desktop\\CapstoneImages\\AM200logo.jpg"
# add_image_to_database(1, test_image)
# update_user_result(1, "test, I'm batman")