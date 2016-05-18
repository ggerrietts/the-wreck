from app import app
from oboeware import OboeMiddleware
import logging

app.wsgi_app = OboeMiddleware(app.wsgi_app)

import truculent_query
import thousand_queries
import noisy_neighbor
import memory_grenade

application = app

# Log errors.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

if __name__ == "__main__":
    app.run()
