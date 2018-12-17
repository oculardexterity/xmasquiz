import datetime
import random
import re
import string

from bs4 import BeautifulSoup
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_mail import Mail
from flask_mail import Message
from flask_session import Session
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
mail = Mail(app)


STRING_OPTIONS = string.ascii_uppercase + string.ascii_lowercase + string.digits

def random_string():
    return ''.join(random.choices(STRING_OPTIONS, k=100))

q11_string = random_string()
q11_datetime = datetime.datetime.now()


@app.route('/')
def index():
    return render_template('1.html')

@app.route('/2/')
def two():
    return 'Now go to the next page.'

@app.route('/3/')
def three():
    return render_template('3.html')

@app.route('/4/')
def four():
    volume = request.args.get('volume')
    if volume in ('11', 'eleven'):
        return 'Correct. Move on the next question by subtracting its number from 37.'
    if volume == 'quiet':
        return "I can't hear you."
    if volume == 'loud':
        return "That's better, but let's go full Spinal Tap for the win."
    if volume:
        return 'Eh?'
    if not volume:
        return "No I don't think that's going to work."

@app.route('/6/')
def six():
    return "No cheating just like that."

@app.route('/7/')
def seven():
    return "No cheating just like that."

@app.route('/8/')
def eight():
    return "No cheating just like that."


@app.route('/32/')
def q5():
    return render_template('q5.html')

@app.route('/2398u4qesfhoiasdhf9a8sdyr983ruiwheasuhdiausdhf/')
def q5_question():
    if 'count' in session:
        session['count'] += 1
    else:
        session['count'] = 0
    
    if session['count'] == 13:
        session.clear()
        return render_template('q5-correct.html')
    return render_template('q5-question.html')

@app.route('/29uqwoenrqwkehjr0384uho3u4ihj3odfgsdfgisdufgoi/', methods=['GET'])
def q6_question():
    return render_template('q6-question.html')

@app.route('/29uqwoenrqwkehjr0384uho3u4ihj3odfgsdfgisdufgoi/', methods=['POST'])
def q6_question_submit():
    if 'answer' in request.form and request.form['answer'] == '60c6fa6f0974eb79069d1391dbd850f3e16b265e':
        return render_template('q6-correct.html')

    return render_template('q6-question.html', message="No, I don't think so.")

@app.route('/oi4j563ioj12iu34h1i2u3hv4k1j3k513hg5234h5i234uh5i2/', methods=['GET'])
def q7_question():
    return render_template('q7-question.html')

@app.route('/oi4j563ioj12iu34h1i2u3hv4k1j3k513hg5234h5i234uh5i2/', methods=['DELETE'])
def q7_question_submit():
    return 'Very good. Now load {} (in your browser is fine)'.format(url_for('q8', _external=True))

@app.route('/94859dgksjdfhgo324uy5235gbjhasdfh34h5k34jh53k4jh5wu/', methods=['GET'])
def q8():
    return render_template('q8-question.html')


@app.route('/94859dgksjdfhgo324uy5235gbjhasdfh34h5k34jh53k4jh5wu/', methods=['POST'])
def q8_submit():
    if 'answer' in request.form:
        if request.form['answer'] == '260549':
            return render_template('q8-correct.html')

        if re.match(r'[\dABCDEF]{6}', request.form['answer']):

            return render_template('q8-question.html', colour=request.form['answer'])
        else:
            return render_template('q8-question.html', gibberish=True)

    else:
        return render_template('q8-question.html')

@app.route('/gfhc6i765ic5645365edhgfhgdsdtrs54ew54wsgvfkuty78t87t/')
def q9():
    return render_template('q9.html')

@app.route('/aksljdfwiejroisjdfoasidhfoasiuhdfaioushdfoasidfjoaisdjf/')
def q9_correct():
    return render_template('q9-correct.html')

@app.route('/23u4qwehnlkasdjf09uw34riasheoirh23k4j5ki34h5234h5k23j4h5/')
def q10():
    if 'Trident' in request.headers['user-agent']:
        return render_template('q10-correct.html', answer_string=q11_string)
    return render_template('q10-question.html')


@app.route('/return-to-sender-really-quickly/')
def q11():
    global q11_string
    global q11_datetime
    if request.args.get('answer') and request.args.get('answer') == q11_string \
        and (datetime.datetime.now() - q11_datetime) < datetime.timedelta(seconds=15): ## Change time to something suitable!

        q11_datetime = datetime.datetime.now()
        q11_string = random_string()

        return 'HERE IT IS: {}'.format(url_for('q12', _external=True))

    q11_string = random_string()
    g11_datetime = datetime.datetime.now()

    return q11_string
    

@app.route('/aosidfjoijwernhkwerobisdfoghj34itjh345jhwoiu45y35/', methods=['GET', 'POST'])
def q12():
    if 'mstring' not in session:
        session['mstring'] = ''

    if 'input' not in request.form:
        return render_template('q12-question.html', mstring=session['mstring'])

    input_value = request.form['input']

    if not re.match(r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', input_value):
        return render_template('q12-question.html', mstring=session['mstring'], message="That's not gonna work!")

    if 'wikipedia.org' not in input_value:
        return render_template('q12-question.html', mstring=session['mstring'], message="It's the right idea, but you need a certain 'Hawaiian velocity'?!")

    
    if re.search(r'wikipedia.org\/wiki\/\w{1}$', input_value):
        return render_template('q12-question.html', mstring=session['mstring'], message="No triviality...")


    resp = requests.get(input_value)

    if resp.status_code != 200:
        return render_template('q12-question.html', mstring=session['mstring'], message="Something bad with that one...")

    soup = BeautifulSoup(resp.text, 'html.parser')
    title_string = soup.title.string

    if title_string.lower().startswith('space'):
        session['mstring'] += ' '
        return render_template('q12-question.html', mstring=session['mstring'], message="You discovered the spacebar!")

    if title_string.lower().startswith('delete'):
        if len(session['mstring']) > 0:
            session['mstring'] = session['mstring'][:-1]
        return render_template('q12-question.html', mstring=session['mstring'], message="You discovered backspace!")


    char = title_string[0].lower()
    session['mstring'] += char

    if session['mstring'] in ('merry christmas', 'happy christmas', 'happy xmas'):
        return redirect(url_for('win'))


    print("'" + session['mstring'] + "'")
    return render_template('q12-question.html', mstring=session['mstring'], message="Voilà. Keep going!")
    

@app.route('/onthefirstdayofchristmasmytruelovegavetomeonenicelovelypintofbeerandacoupleofpacketsofcrisps/', methods=['GET', 'POST'])
def win():
    if 'name' in request.form:
        msg = Message("Quiz winner!",
                  sender="from@xmasquiz.ed.ac.uk",
                  recipients=["richard.hadden@ed.ac.uk"])
        msg.body = '{} has won the quiz!'.format(request.form['name'])
        mail.send(msg)
        return render_template('win.html', show_form=False)

    return render_template('win.html', show_form=True)



@app.errorhandler(404)
def page_not_found(e):
    return "It looks like that didn't work. Try hitting back."







if __name__ == '__main__':
    app.run(debug=True)