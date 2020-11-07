from Web_Application.utils.utils import read_content, add2database, createFile
from Web_Application.models import Post
from Web_Application import app, db
from flask import render_template, url_for, request, redirect, send_file, after_this_request
from GDPR_checker.verifier import GDPR_Verifier

import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=Post.query.all(), maxlen=app.config['MAX_OUTLEN'])

@app.route('/post/new', methods=['POST', "GET"])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        # check if file is selected by the user
        if file.filename != '':
            """
            the simpliest way of reading the content of the file is to store it temprorarily,
            read content of the file using classical pythonic way and to delete the file, this is
            the approach I am going to take here. 
            """

            content = read_content(file, app)

            # saving content in the DataBase
            p1 = Post(original_text=content)
            add2database(db, p1)

    return redirect(url_for('home'))


@app.route('/summaryCreator/<int:post_id>', methods=['POST', 'GET'])
def create_summary(post_id):
    app.logger.info("Creating a summary")

    post = Post.query.get_or_404(post_id)

    # set status as processing
    post.summary = "$Processing$"
    db.session.commit()


    # start processing operation
    model = GDPR_Verifier(language="en", window_size=10)

    similarity_score = model.analyse_text(post.original_text)*100



    summarized_text = f"{int(similarity_score)}"

    post.summary = summarized_text
    db.session.commit()

    return redirect(url_for('home'))  # 'file uploaded successfully'

@app.route('/download/<int:post_id>', methods=['POST', 'GET'])
@app.route('/download/<int:post_id>/<format>', methods=['POST', 'GET'])
def download_data(post_id:int, format:str):
    post = Post.query.get_or_404(post_id)
    if format == "original_text":
        text = post.original_text
    else:
        text = post.summary


    file_local_path = os.path.join(os.path.dirname(__file__), f"generated_files/{format}_{post_id}.txt")

    # Currently bad solution as we are storing the file as txt and in database
    if not os.path.exists(file_local_path):
        createFile(text, file_local_path)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_local_path)
        except Exception as error:
            app.logger.error("Error removing downloaded file handle", error)
        return response

    return send_file(f"generated_files/{format}_{post_id}.txt", as_attachment=True)


@app.route('/delete/<int:post_id>', methods=['POST', 'GET'])
def delete_post(post_id:int):
    app.logger.info("Deleting post")

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))





