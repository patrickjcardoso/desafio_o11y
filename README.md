# Atividade Prática Observabilidade

## Objetivo do Laboratório:

Criar um ambiente de observabilidade usando Prometheus e Grafana para monitorar uma aplicação de exemplo.

## Technologies Used:

* Linux (Ubuntu based)
* Python Application
* Prometheus
* Grafana

## Pré-requisitos:

* Você precisará de uma máquina Linux (pode ser uma VM, um servidor ou mesmo uma máquina local com Docker instalado).
* Conhecimento básico de linha de comando do Linux.
* Docker instalado na máquina.
* Uma aplicação de exemplo para monitorar (exemplo simples em Python).
* Clonar o repositório da atividade.

## Passos:

### Passo 1: Instalação do Prometheus e Grafana

1.1. Baixe o Docker Compose e instale-o em sua máquina se você ainda não o tiver:

  
   ```console
    $ sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    $ sudo chmod +x /usr/local/bin/docker-compose
   ```
  
    
1.2. Clone o repositório ou crie um diretório para o seu projeto e vá para ele:

    $ mkdir observability-lab
    $ cd observability-lab

1.3. Crie um arquivo **docker-compose.yml** para definir os serviços Prometheus e Grafana:


```yaml
    version: '3'
    services:
    prometheus:
        image: prom/prometheus
        volumes:
        - ./prometheus:/etc/prometheus
        command:
        - '--config.file=/etc/prometheus/prometheus.yml'
        ports:
        - '9090:9090'

    grafana:
        image: grafana/grafana
        ports:
        - '3000:3000'
```

1.4. Crie um diretório chamado **prometheus** e, dentro dele, crie um arquivo **prometheus.yml** para configurar o Prometheus:

  ```yaml
    global:
    scrape_interval:     15s

    scrape_configs:
    - job_name: 'prometheus'
        static_configs:
        - targets: ['localhost:9090']
    - job_name: 'your-app'
        static_configs:
        - targets: ['your-app-container:your-app-port']
  ```

### Passo 2: Configurando a Aplicação de Exemplo

2.1 Certifique-se de que você tenha o **Flask** e o **Prometheus Client** Python instalados. Você pode instalá-los usando o pip:

    pip install Flask prometheus_client

2.2 Acesso o diretório da aplicação:

    $ cd python-app

* Abra o arquivo **app.py** e analise o código fonte, perceba que existem algumas rotas criadas.
* A porta que está sendo exposta sua aplicação é a 3001, você pode alterar caso seja necessário.


2.3 Inicie sua aplicação e exponha-a em uma porta específica.

```console
python app.py
```

2.5 Testando a aplicação python.

Sua aplicação estará disponível em http://localhost:3001. Você pode acessar a página inicial e também verificar as métricas expostas em http://localhost:3001/metrics.

### Passo 3: Configurar o Prometheus no Laboratório 

No arquivo **prometheus.yml** no diretório prometheus (conforme configurado anteriormente), adicione ou ajuste a seguinte seção sob **scrape_configs** para coletar métricas da sua aplicação python:


```yaml
- job_name: 'nodejs-app'
  static_configs:
    - targets: ['your-app-container:your-app-port']
```

* Certifique-se de substituir **'your-app-container:your-app-port'** pelo host e porta onde sua aplicação python está sendo executada.

### Passo 4: Iniciando o Ambiente de Observabilidade

4.1 Volte para o diretório raiz do seu projeto e execute o seguinte comando para iniciar os serviços Prometheus e Grafana:

```console
$ cd ..
$ docker-compose up -d
```

4.2 Certifique-se que os containers do Prometheus e do Grafana subiram e estão funcionando:

```console
$ docker-compose ps
```

### Passo 5: Acessando o Promethues e verificando as métricas da aplicação

5.1 Acesse o painel Promethues em seu navegador em http://localhost:9090.

5.2 Verifique so o Prometheus está conseguindo acessar os dados da sua aplicação. 