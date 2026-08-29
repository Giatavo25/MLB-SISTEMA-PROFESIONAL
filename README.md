# Calculadora MLB - Moneyline y Totales

App en Flask que consulta el Stats API público de la MLB (statsapi.mlb.com)
y calcula probabilidades de moneyline y over/under de carreras usando
distribución de Poisson.

## Estructura
```
mlb-betting-app/
  app.py              -> rutas Flask
  mlb_api.py          -> llamadas al Stats API de la MLB
  calculations.py      -> Poisson, cuotas, edge
  templates/index.html -> interfaz web
  requirements.txt
  Procfile
```

## Correr localmente
```
pip install -r requirements.txt
python app.py
```
Abre http://localhost:5000

## Desplegar en Render
1. Sube esta carpeta a un repositorio de GitHub.
2. En Render: New -> Web Service -> conecta el repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Deploy.
# MLB-SISTEMA-PROFESIONAL
