import os
import pymysql
import shutil
# MySQL database connection settings
db_host = "localhost"
db_user = "root"
db_password = "admin"
db_name = "Ebooks"

# Function to insert a book and its chapters into the database
def insert_book_and_chapters(book_name, author_name, description, cover_image_path, chapter_files):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = conn.cursor()

    try:
        # Insert data for the author
        cursor.execute("INSERT INTO author (name) VALUES (%s) ON DUPLICATE KEY UPDATE author_ID=LAST_INSERT_ID(author_ID)", (author_name,))
        author_id = cursor.lastrowid

        # Generate a unique filename for the cover image
        cover_image_filename = f"cover.jpg"
        cover_image_path_on_disk = os.path.join('books',book_name, cover_image_filename)  # Change "image_uploads" to your desired image storage path

        # Copy the cover image to the specified path
        # cover_image_dst_path = os.path.join(data_folder, cover_image_path_on_disk)
        # os.makedirs(os.path.dirname(cover_image_dst_path), exist_ok=True)
        # shutil.copy(cover_image_path, cover_image_dst_path)

        # Insert data for the book, including the image path
        cursor.execute("INSERT INTO books (name, author_ID, description, image_path) VALUES (%s, %s, %s, %s)", (book_name, author_id, description, cover_image_path_on_disk))
        book_id = cursor.lastrowid

        # Insert data for each chapter
        for i,chapter_file in enumerate(chapter_files):
            # Extract the chapter name from the file name (assuming file names are like "chapter_name.txt")
            chapter_name = os.path.basename(chapter_file).split(".")[0][:45]
            # print(i,type(i))
            with open(chapter_file, "r", encoding="utf-8") as file:
                chapter_text = file.read()
                cursor.execute("INSERT INTO chapters (book_ID, chapter_name, chapter, position) VALUES (%s, %s, %s, %s)", (book_id, chapter_name, chapter_text, i+1))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()

# Specify the path to the folder containing book data
data_folder = "books/"

# Loop through the subdirectories in the data folder
for dir_name in os.listdir(data_folder):
    dir_path = os.path.join(data_folder, dir_name)
    if os.path.isdir(dir_path):
        author_file = os.path.join(dir_path, "author.txt")
        cover_file = os.path.join(dir_path, "cover.jpg")
        chapter_files = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.startswith("Chapter")]

        if os.path.exists(author_file) and os.path.exists(cover_file) and chapter_files:
            with open(author_file, "r", encoding="utf-8") as file:
                author_name = file.read().strip()

            book_name = dir_name
            description = f"{book_name}"

            insert_book_and_chapters(book_name, author_name, description, cover_file, chapter_files)
