  O projeto “Micro Kart” foi feito inspirado no jogo Mario Kart, visando trazer uma experiência no mundo real e que fosse mais interativa com o usuário. Tendo o objetivo de criar umas pista de corrida, na qual uma ou mais pessoas podem correr com um carrinho, também criado para o projeto, para disputar quem passa por todos os obstáculos do percurso no menor tempo, o projeto integrou as áreas de mecânica, eletrônica e computação para seu desenvolvimento. 

  O desenvolvimento do jogo foi dividido em 4 partes: Criação da interface, monitoramento dos comandos por controle, construção da pista e construção do carrinho. Cada uma das divisões do projeto é especificada abaixo juntamente com sua devida descrição e componentes caso necessário. 

 - Interface:
  Essa parte é a responsável por mostrar a parte computacional do jogo, mostrando na tela do computador os modos de jogo, jogadores, tempo decorrido, e quaisquer outros elementos necessários para configurar e iniciar o jogo ou que não são possíveis mostrar visualmente no mundo real (como a vantagem/desvantagem que o carrinho possui). Além disso a interface do jogo pode salvar os tempos das corridas em um banco de dados para criar um ranking que pode ser consultado futuramente.

- Controle:
Essa vertente do projeto foi focada na leitura dos comandos enviados pelo controle e na programação de tratamento dos mesmo antes de serem passados para o carrinho via mqtt. Limites de velocidade e de curva, inversão de comandos devido a efeitos do jogo são exemplos de dados que precisaram ser estipulados e tratados na programação do controle.

  Componentes utilizados:
    * Controle de xbox 360: Conectado ao computador por um cabo, envia os comandos que são lidos e enviados para o carrinho durante o jogo. 


- Pista:
  A pista é feita de madeira, com o percurso pintado com tinta em spray preta, e possui obstáculos intercambiáveis entre si. Nesses obstáculos são obtidas vantagens ou desvantagens para o carrinho, que podem resultar em um aumento/redução da velocidade, travamento do carrinho, entre outros efeitos.

  Componentes utilizados:
  * 7 ESPs 32: Responsáveis por captar e processar as informações dos sensores e transmitirem eventos via MQTT.

  * 6 sensor de presença HW 201: Está em todos os obstáculos, servindo para checar se o carrinho passou por um obstáculo específico.

  * 1 sensor de cor TCS230: Verifica se a cor do farol do carro é correspondente com a sorteada a cada início de partida.

  * 1 Servo motor MG90S: Movimenta uma haste, para simular uma cancela que é acionada em função da leitura do sensor TCS230.

  * 7 Baterias 9V: Alimentam os circuitos dos sensores e o ESP 32, assim tirando a necessidade de cabos usb para o funcionamento dos mesmo, facilitando a modularização.

  * 4 Leds RGB: Sinalizar o tipo de efeito aplicado ao carrinho caso passe por um obstáculo e a cor que o jogador deve expor para passar do obstáculo semelhante a uma cancela.

  * 3 Leds verdes: Sinalizar que um checkpoint está ativo.

- Carrinho:
  O carrinho é feito por impressões, parafusos e os componentes citados abaixo, contando com um sistema de tração traseira que o faz andar para frente e para trás e um sistema de curva com cremalheira que gira as rodas frontais. Ele é controlado por um controle que envia um sinal por mqtt, que será lido pelo ESP e interpretado no Arduino.

  Componentes utilizados:
  * 2 Motores DC: São utilizados para a locomoção do carrinho. São eles que fazem o carrinho andar para frente e para trás.

  * 1 Servo motor MG90S: Gira uma engrenagem que gira um eixo que vai mover uma cremalheira. Resumidamente, é ele que vai dar o movimento giratório das rodas dianteiras, possibilitando o carrinho de fazer curvas.

  * 1 Arduino MEGA: Processa informações recebidas pelas outras partes do projeto e roda o código principal do carrinho. Comanda os motores DC e o servo.

  * 1 Shield L293d: Usado para ligar os motores DC e o servo ao arduino.

  * 1 ESP 32: Usado para receber e enviar informações mandadas por outros componentes do projeto via mqtt.


  Além disso, todas as partes do projeto foram feitas para poderem ser transportadas, sendo de fácil montagem/desmontagem.


Abaixo seguem esquematicos dos circuitos utilizados

Nos obstáculos da pista:
![OBS_LUZ_bb](https://github.com/user-attachments/assets/d3ed7585-b829-4555-99d7-ffbdfaf42d97)
![lap_bb](https://github.com/user-attachments/assets/10139f64-4ed8-4e63-ae4c-8793894c88e1)
![Obstaculos1_2_3_bb](https://github.com/user-attachments/assets/84281de5-6879-43a1-92f4-ecbc9cc277c9)

No carrinho:
![circuito carrinho](https://github.com/user-attachments/assets/6a2fc6b9-6b1b-4c99-b89b-7b5e506cd8cc)
