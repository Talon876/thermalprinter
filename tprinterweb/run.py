#!/usr/bin/env python
from app import app
from config import PORT

app.run(debug=True, port=PORT)

