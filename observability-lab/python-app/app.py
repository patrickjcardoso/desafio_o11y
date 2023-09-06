from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

app = Flask(__name__)

# Métrica para contar erros
error_count = Counter('app_errors_total', 'Total number of errors')

# Métrica para medir o tempo de execução de uma função
function_duration = Histogram('app_function_duration_seconds', 'Time spent in function execution', ['function_name'])

# Rota para página inicial com mensagem de boas-vindas
@app.route('/')
def welcome():
    welcome_message = """
    <html>

<head>
    <style>
        body {
            background-color: #6a5acd; /* Define a cor de fundo azul petróleo */
        }

        .center {
            text-align: center;
            font-size: 90px;
            color: white; /* Define a cor do texto como branco */
            margin-top: 50vh; /* Centraliza verticalmente usando margem superior */
            transform: translateY(-50%); /* Ajusta a posição verticalmente */
        }

        .links {
            text-align: center;
            margin-top: 20px;
            font-size: 24px;
        }

        .links a {
            color: white;
            text-decoration: underline;
            margin: 0 10px;
        }
        
    </style>
</head>

<body>
    <div class="center">
        <p>Bem-vindo ao desafio de Observabilidade da O2B Academy</p>
    </div>
    <div class="links">
        <a href="/generate-error">Gerar Erro</a>
        <a href="/calculate-duration">Calcular Duração</a>
        <a href="/metrics">Métricas</a>
    </div>
</body>

</html>
    """
    return welcome_message

# Rota para gerar erros intencionalmente
@app.route('/generate-error')
def generate_error():
    try:
        # Simulando uma exceção
        1 / 0
    except Exception as e:
        # Incrementando a métrica de erros
        error_count.inc()
        return f"Erro gerado: {str(e)}", 500

# Rota para medir o tempo de execução
@app.route('/calculate-duration')
def calculate_duration():
    start_time = time.time()
    # Simulando uma operação demorada
    time.sleep(2)
    function_duration.labels(function_name='calculate_duration').observe(time.time() - start_time)
    return "Tempo de execução medido com sucesso"

# Rota para expor métricas do Prometheus com quebras de linha
@app.route('/metrics')
def metrics():
    metrics_data = generate_latest(REGISTRY)
    return Response(metrics_data, content_type='text/plain; version=0.0.4')

# Rota para mostrar métricas no formato prometheus
@app.route('/metrics-text')
def metrics_text():
    return MetricsHandler(REGISTRY).do_GET(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
