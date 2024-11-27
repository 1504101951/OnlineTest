# -----------------------------------import------------------------------------
import traceback

from flask_app import app, scheduler
# -----------------------------------static------------------------------------


# ------------------------------------code------------------------- ------------
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3100, debug=True, threaded=True)
    scheduler.shutdown()
