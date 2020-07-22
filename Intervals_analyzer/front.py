from flask import Flask, render_template, request
import logger
app = Flask(__name__)


log = logger.logger
log.error ("Front started")


@app.route("/")

def main():
    log = logger.logger
    log.error("Front started")
    return render_template('index.html', link="https://www.strava.com/oauth/authorize?client_id=50434&redirect_uri=http://localhost:5000/StravaAuthReturn&response_type=code&scope=activity:read_all")
    log.error("returned index.html")

#todo refactor variable names to align to convention

@app.route("/StravaAuthReturn")
def state():
    stravaAuthCode = request.args.get('code', default = None, type = str)
    stravaAuthScope = request.args.get('scope', default = None, type = str)
    print(stravaAuthCode, stravaAuthScope)
    log.error("Auth completed with code", stravaAuthCode)
    return render_template('StravaAuthReturn.html', code = stravaAuthCode)
if __name__ == "__main__":
    app.run()


if __name__ == '__main__':
    main()

