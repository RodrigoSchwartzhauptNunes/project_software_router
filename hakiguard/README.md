1. hakiguard – módulo de análise baseada em IA

	O hakiguard é um módulo do projeto project_software_router responsável por executar detecção de tráfego suspeito e possíveis ataques DDoS utilizando 	inteligência artificial.
	Ele funciona como um componente desacoplado, rodando em containers, e se comunica com o software router principal através de uma API HTTP.

	O módulo contém duas áreas principais:

  	Ambiente de inferência (produção) – executa a IA treinada e expõe uma API que o router consome.

  	Ambiente de treinamento (desenvolvimento) – usado apenas para criação e atualização dos modelos de IA.

  	<img width="590" height="312" alt="image" src="https://github.com/user-attachments/assets/a681e24f-c3cc-49ed-931c-e02b80dba0b3" />



2. Descrição detalhada dos diretórios

  2.1 - models/

	Responsável por armazenar os modelos de IA já treinados e prontos para uso.
	A IA de produção lê exclusivamente os arquivos deste diretório.
	Normalmente contém arquivos como .tflite, .h5 ou .onnx, além de metadados de versão.

	Este diretório faz parte do ambiente de produção e deve estar sempre presente.


  2.2 - inference/

	Contém toda a estrutura utilizada para executar o modelo de IA em produção.
	Este ambiente é carregado pelo docker-compose.yml principal e expõe uma API HTTP para que o software router solicite análises.

	Conteúdo:

		Dockerfile
			Define a imagem do container de inferência e suas dependências.
			Aqui serão configurados os requisitos para carregar modelos, rodar a IA e iniciar o serviço da API.

		requirements.txt
			Lista as dependências de software necessárias para a execução do ambiente de inferência.

		src/inference.py
			Arquivo principal do módulo de inferência.
			Ele será responsável por:

			carregar o modelo presente em models/

			iniciar o serviço de inferência

			responder às requisições feitas pelo software router


  2.3 - training/

	Ambiente usado exclusivamente no processo de desenvolvimento para treinar modelos da IA.
	Esse diretório não faz parte da produção e nunca é carregado pelo router.

	Este ambiente terá seu próprio docker-compose.yml, permitindo criar uma estrutura isolada com dataset, notebooks e ferramentas de treinamento sem afetar o ambiente principal.

	Conteúdo:

		docker-compose.yml
			Compose exclusivo para o ambiente de desenvolvimento.
			Permite subir containers de treinamento, acesso ao dataset e ferramentas auxiliares.

		Dockerfile
			Define o ambiente onde o treinamento será executado, incluindo dependências e ferramentas específicas de machine learning.

		requirements.txt
			Lista de dependências necessárias para o processo de treinamento.

		src/train.py
			Ponto de entrada do ambiente de treinamento.
			Este arquivo será responsável por carregar o dataset, treinar o modelo e salvar os arquivos finais dentro do diretório models/.

3. Arquivos da raiz do módulo

  3.1 - docker-compose.yml

	Compose principal do módulo hakiguard.
	Ele monta o diretório models/ no container de inferência e utiliza as variáveis definidas no arquivo .env.
	É responsável por subir a API de IA que será utilizada pelo software router.

  3.2 - .env.example

	Arquivo contendo todas as variáveis necessárias para configurar o módulo.
	O usuário deve copiá-lo para .env antes de executar o módulo.

	Exemplos de variáveis que podem existir:

		porta da API

		caminho do modelo

		nome do arquivo do modelo

		parâmetros de execução

  3.3 - .gitignore

	Define arquivos e diretórios que não devem ser versionados.
	Inclui itens como:

		.env

		caches

		logs

		arquivos gerados automaticamente

		modelos grandes

  3.4 - README.md

	Documento que descreve a estrutura, propósito e funcionamento do módulo.



