HakiGuard – Módulo Inteligente de Detecção e Mitigação de Ataques DDoS
###
#25/11/25
######
###Parte integrante do projeto project_software_router

    O HakiGuard é um módulo de segurança baseado em inteligência artificial projetado para rodar dentro do ambiente OpenWRT como parte de um software router avançado.
    
    Ele tem como função:
    
        capturar o tráfego da rede
        
        extrair flows usando CICFlowMeter
        
        aplicar modelos de IA treinados para identificar tráfego malicioso
        
        gerar alertas em tempo real ## Ainda vendo essa parte
        
        enviar esses alertas ao núcleo do roteador via UNIX Socket
        
        aplicar mitigação automática com regras em nftables
        
        O sistema foi projetado para ser altamente modular, eficiente e fácil de atualizar, permitindo que novos modelos de IA sejam    treinados e substituídos sem modificar o módulo de produção.

###Arquitetura do Sistema

A arquitetura do HakiGuard é dividida em duas partes:

1. Ambiente de Produção (rodando no OpenWRT,)

    captura de tráfego
    
    geração de flows via CICFlowMeter
    
    inferência IA usando modelos prontos
    
    envio de alertas via UNIX socket
    
    listener/mitigação automática
    
    serviço init.d para execução automática no roteador

2. Ambiente de Treinamento (rodando via Docker, isolado)


    script de treinamento
    
    requirements específicos
    
    dataset (Portmap.csv, CICIDS etc.)
    
    geração automatizada dos modelos
    
    exportação para hakiguard/models/
    
    Esse ambiente não roda no OpenWRT, sendo utilizado apenas quando há necessidade de atualizar ou evoluir a IA.


Estrutura Completa do Projeto

        hakiguard/
        ├── README.md
        ├── .env
        │
        ├── models/
        │   ├── random_forest_model.pkl
        │   ├── linear_regression_model.pkl
        │   ├── scaler.pkl
        │   └── metadata.json
        │
        ├── capture/
        │   ├── capture.sh
        │   └── interface.conf
        │
        ├── cicflowmeter/
        │   ├── CICFlowMeter.jar
        │   ├── run_cicflow.sh
        │   └── output/
        │
        ├── inference/
        │   ├── inference.py
        │   ├── config.json
        │   └── utils/
        │       ├── preprocess.py
        │       └── load_flow.py
        │
        ├── bridge/
        │   └── send_result.py
        │
        ├── listener/
        │   ├── hakiguard-listener.py
        │   └── rules/
        │       └── default_rule.sh
        │
        ├── init/
        │   └── hakiguard
        │
        ├── var/
        │   ├── run/hakiguard.sock
        │   └── log/hakiguard.log
        │
        └── training/              (somente para desenvolvimento)
            ├── dataset/Portmap.csv
            ├── output/grafico.png
            ├── src/train.py
            ├── Dockerfile
            ├── docker-compose.yml
            └── requirements.txt


Descrição de Cada Diretório 
 
 O que cada um faz

      models/
      
      Armazena todos os modelos de IA treinados, utilizados em produção.
      
      Contém:
      
      modelos preditivos .pkl
      
      scaler de normalização
      
      metadados da versão do modelo

      Atualizado automaticamente pelo módulo de treinamento (Docker).


##############################

      capture/
      
      Responsável por capturar tráfego real da interface configurada.
      
      capture.sh
      Script para capturar tráfego via tcpdump ou redirect para CICFlowMeter
      
      interface.conf
      Define qual interface será monitorada (eth0, br-lan, etc.)

##############################

      cicflowmeter/
      
      Realiza a extração de flows do tráfego capturado.
      
      CICFlowMeter.jar → extrator oficial
      
      run_cicflow.sh → script para iniciar o extrator
      
      output/ → onde os flows CSV são salvos
      
      Esses flows alimentam o módulo de inferência.

##############################

      inference/
      
      Aplica o modelo de IA treinado para analisar os flows gerados.
      
      Arquivos principais:
      
      inference.py
      
      lê modelo(s) em /models
      
      processa novo fluxo
      
      roda a inferência
      
      detecta possíveis ataques
      
      envia resultado para bridge/send_result.py
      
      config.json
      Parâmetros de threshold, caminhos, tuning de IA
      
      utils/preprocess.py
      Normaliza features igual ao treinamento
      
      utils/load_flow.py
      Lê o último flow CSV para inferência

##############################
      
      bridge/
      
      Faz a comunicação entre a IA e o sistema principal via UNIX socket.
      
      send_result.py
      Envia um JSON contendo o resultado da inferência:
      
      {
        "attack": true,
        "prob": 0.95,
        "source_ip": "10.0.0.55"
      }

##############################

      listener/
      
      Responsável por:
      
      ouvir o socket
      
      receber alertas da IA
      
      aplicar mitigação automática usando nftables
      
      registrar logs
      
      executar scripts personalizados
      
      Arquivos principais:
      
      hakiguard-listener.py
      Servidor socket que toma decisões
      
      rules/default_rule.sh
      Regra padrão de firewall usada na mitigação automática

##############################

      init/
      
      Contém o script init.d para o OpenWRT.
      
      hakiguard → inicia/para/restarta o listener no boot

##############################

      var/
      
      Arquivos de runtime do módulo.
      
      run/hakiguard.sock
      Socket UNIX para comunicação
      
      log/hakiguard.log
      Log persistente das ações do HakiGuard

##############################


      Ambiente de Treinamento (Docker)
      
      O treinamento da IA é totalmente separado do módulo de produção.
      
      Ele contém:
      
      dataset (ex.: Portmap.csv)
      
      ambiente Python isolado
      
      src/train.py com todo o pipeline de:
      
      limpeza de dados
      
      seleção de features
      
      escalonamento
      
      treino dos modelos
      
      avaliação
      
      exportação dos modelos para /hakiguard/models/
      
      renderização do gráfico da performance (grafico.png)
      
      instalação de dependências via Dockerfile

##############################

Como funciona o fluxo completo


OpenWRT → captura → CICFlowMeter → inference → socket → firewall

Continuar detalhamento 