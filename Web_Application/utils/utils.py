import os
import datetime
import time


"""File with supporting functions"""


def read_content(req_file, app):
    file_name = str(datetime.datetime.now()) + ".txt"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    req_file.save(file_path)

    # in case file has not been uploaded yet (e.g. some delay happenned)
    while not os.path.exists(file_path):
        app.logger.info(f"Waiting for response...")
        time.sleep(1)

    with open(file_path, 'r', encoding='utf-8') as reader:
        content = reader.read()

    # delete uploaded temprorary file
    os.remove(file_path)

    return content


def add2database(db, data):
    db.session.add(data)
    db.session.commit()


def createFile(text:str, file_path:str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)




