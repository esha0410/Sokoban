from flask import *
from collections import deque
import json


data = []
nrows = 0
px = py = 0
sdata = ""
ddata = ""

def init(board):
    global data, nrows, sdata, ddata, px, py
    data = [_f for _f in board.split('x') if _f]
    nrows = max(len(r) for r in data)
 
    maps = {' ':' ', '.': '.', '@':' ', '#':'#', '$':' '}
    mapd = {' ':' ', '.': ' ', '@':'@', '#':' ', '$':'*'}
 
    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            sdata += maps[ch]
            ddata += mapd[ch]
            if ch == '@':
                px = c
                py = r
 
def push(x, y, dx, dy, data):
    if sdata[(y+2*dy) * nrows + x+2*dx] == '#' or \
       data[(y+2*dy) * nrows + x+2*dx] != ' ':
        return None
 
    data2 = list(data)
    data2[y * nrows + x] = ' '
    data2[(y+dy) * nrows + x+dx] = '@'
    data2[(y+2*dy) * nrows + x+2*dx] = '*'
    return "".join(data2)
 
def is_solved(data):
    for i in range(len(data)):
        if (sdata[i] == '.') != (data[i] == '*'):
            return False
    return True
 
def solve():
    open = deque([(ddata, "", px, py)])
    visited = set([ddata])
    dirs = ((0, -1, 'u', 'U'), ( 1, 0, 'r', 'R'),
            (0,  1, 'd', 'D'), (-1, 0, 'l', 'L'))
 
    lnrows = nrows
    while open:
        cur, csol, x, y = open.popleft()
 
        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]
 
            if temp[(y+dy) * lnrows + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and temp not in visited:
                    if is_solved(temp):
                        return csol + di[3]
                    open.append((temp, csol + di[3], x+dx, y+dy))
                    visited.add(temp)
            else:
                if sdata[(y+dy) * lnrows + x+dx] == '#' or \
                   temp[(y+dy) * lnrows + x+dx] != ' ':
                    continue
                
                data2 = list(temp)
                data2[y * lnrows + x] = ' '
                data2[(y+dy) * lnrows + x+dx] = '@'
                temp = "".join(data2)
 
                if temp not in visited:
                    if is_solved(temp):
                        return csol + di[2]
                    open.append((temp, csol + di[2], x+dx, y+dy))
                    visited.add(temp)
 
    return "No solution"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/index' ,methods=['GET','POST'])
def index_page():
    name=request.form["username"]
    return redirect(url_for("user",usr=name))

@app.route('/<usr>')
def user(usr):
    return render_template('index.html',usr=usr)



@app.route('/processUserInfo/<string:userInfo>', methods=['POST'])
def processUserInfo(userInfo):
    userInfo=json.loads(userInfo)
    level=userInfo['level']
    level=level.replace('w','#')

    init(level)
    answer=solve()
    return answer

if (__name__=='__main__'):
    app.run(debug=True)
