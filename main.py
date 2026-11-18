import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def run_etl():
    # Place ici ou appelle ta fonction principale d'extraction / transformation / chargement
    print("Exécution du pipeline ETL...")
    # ton_code_etl()
    print("Pipeline ETL terminé avec succès.")

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/run":
            threading.Thread(target=run_etl, daemon=True).start()
            message = "Relance du pipeline ETL déclenchée en arrière-plan."
        else:
            message = "Pipeline ETL opérationnel sur Render."

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""
        <html>
          <body style="font-family: sans-serif; padding: 2rem; background: #0f172a; color: #f8fafc;">
            <h1>Data Pipeline ETL</h1>
            <p>{message}</p>
            <a href="/run" style="color: #34d399;">Relancer le pipeline manuellement</a>
          </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    # Exécute le pipeline dans tous les cas (CI et Render)
    run_etl()

    # Sur Render uniquement, garde un serveur HTTP actif sur le port attendu
    if os.environ.get("RENDER"):
        port = int(os.environ.get("PORT", 10000))
        server = HTTPServer(("0.0.0.0", port), StatusHandler)
        print(f"Serveur de statut actif sur le port {port}")
        server.serve_forever()
