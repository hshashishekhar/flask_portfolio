from flask import Flask, render_template, request, url_for, flash, redirect, send_file


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'



@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(name)
        print(email)
        print(message)
        flash("Thankyou. We will get in touch with you soon.!")
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/bad")
def bad():
    return render_template('bad.html')

@app.route("/3dprinter")
def dprinter():
    return render_template('3dprinter.html')

@app.route("/lms")
def lms():
    return render_template('lms.html')

@app.route("/trading_bot")
def trading_bot():
    return render_template('trading_bot.html')

@app.route("/summarizer")
def summarizer():
    return render_template('summarizer.html')

@app.route("/yupbot")
def yupbot():
    return render_template('yupbot.html')

@app.route('/downloadResume') # this is a job for GET, not POST
def downloadResume():
    return send_file(
        'resume.pdf',
        download_name='Shashishekhar Python Developer.pdf',
        as_attachment=True
    )

if __name__== "__main__":
    app.run()


# flask run --debug