from app import app
from oboeware import OboeMiddleware

app.wsgi_app = OboeMiddleware(app.wsgi_app)

import truculent_query
import thousand_queries
import noisy_neighbor
# import memory_grenade

application = app

if __name__ == "__main__":
    app.run()
