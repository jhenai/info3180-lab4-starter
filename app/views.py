"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from werkzeug.utils import secure_filename

PIC_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/add-file', methods=['POST', 'GET'])
def add_file():
    if not session.get('logged_in'):
        abort(401)

    file_folder = app.config["UPLOAD_FOLDER"]

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_folder, filename))

        flash('File Saved')
        return redirect(url_for('home'))

    return render_template('add_file.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in')
            return redirect(url_for('add_file'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
    
    
@app.route('/filelisting')    
def file_traverse():
    if not session.get('logged_in'):
        abort(401)
        
    rootdir = os.getcwd()
    filelist=[]
    pic=[]
    print rootdir
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            f= str(file)
            if allowed_file(f):
                pic.append(f)
            else:
                filelist.append(os.path.join(subdir, file))
        return render_template('file_list.html', file=filelist, pic=pic)
    return render_template('file_list.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PIC_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
