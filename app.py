from flask import Flask, render_template, redirect, request, url_for
import logging
import time

app = Flask(__name__)

name = 'Player' # name of the player
timer_duration = 600 # number of seconds player has left
start_time = None

locks = {
    'ravenclaw_solved' : False,
    'hufflepuff_solved' : False,
    'gryffindor_solved' : False,
    'slytherin_solved' : False
}

tried = {
    'r' : False,
    'h' : False,
    'g' : False,
    's' : False
}

# suppress log messages that appear every time someone lands on a page
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# define '/' route
@app.route('/')
def welcome():
    return render_template('index.html')

# define 'submitName' route
@app.route('/submitName', methods=['POST'])
def submitName():
    global name
    name = request.form.get('user_name')
    if(name.strip() == ''):
        name = 'Player'
    return redirect('room')

# define 'room' route
@app.route('/room')
def room():
    global name, locks, tried, timer_duration, start_time
    if(start_time == None):
        start_time = time.time()
    elapsed = int(time.time() - start_time)
    remaining = max(0, timer_duration - elapsed)
    if(remaining <= 0):
        return redirect(url_for('failed_escape'))
    return render_template('room.html', user_name = name, the_timer = remaining,
                           r_solved = locks['ravenclaw_solved'], r_tried = tried['r'],
                           h_solved = locks['hufflepuff_solved'], h_tried = tried['h'],
                           g_solved = locks['gryffindor_solved'], g_tried = tried['g'],
                           s_solved = locks['slytherin_solved'], s_tried = tried['s'])

# define Ravenclaw route => RAVEN
@app.route('/ravenclaw', methods=['POST'])
def ravenclaw():
    global locks
    ans = request.form.get('ans1').strip().lower()
    if(ans == 'raven'):
        locks['ravenclaw_solved'] = True
    tried['r'] = True
    return redirect('room')

# define Hufflepuff route => TEAMWORK
@app.route('/hufflepuff', methods=['POST'])
def hufflepuff():
    global locks
    ans = request.form.get('ans2').strip().lower()
    if(ans == 'teamwork'):
        locks['hufflepuff_solved'] = True
    tried['h'] = True
    return redirect('room')

# define Gryffindor route => BRAVERY
@app.route('/gryffindor', methods=['POST'])
def gryffindor():
    global locks
    ans = request.form.get('ans3').strip().lower()
    if(ans == 'bravery'):
        locks['gryffindor_solved'] = True
    tried['g'] = True
    return redirect('room')

# define Slytherin route => 13 or THIRTEEN
@app.route('/slytherin', methods=['POST'])
def slytherin():
    global locks
    ans = request.form.get('ans4').strip().lower()
    if(ans == '13' or ans == 'thirteen'):
        locks['slytherin_solved'] = True
    tried['s'] = True
    return redirect('room')   

# define 'secret_passage' route
@app.route('/secret_passage', methods=['GET', 'POST'])
def secret_passage():
    global timer_duration, start_time
    elapsed = int(time.time() - start_time)
    remaining = max(0, timer_duration - elapsed)
    if(remaining <= 0):
        return redirect(url_for('failed_escape'))
    return render_template('secret_passage.html', user_name = name, the_timer = remaining)

# define 'escape' route for successful escape
@app.route('/escape', methods=['GET', 'POST'])
def escape():
    return render_template('escape.html', user_name = name)

# define 'failed_escape' route if player did not escape in time
@app.route('/failed_escape', methods=['GET', 'POST'])
def failed_escape():
    return render_template('failed_escape.html', user_name = name)

# turn on debug mode
app.debug = True

# start the server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=100)