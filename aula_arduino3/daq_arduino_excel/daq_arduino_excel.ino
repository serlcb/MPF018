// C++ code
//
//Circuito RC
//Habilidades EF08CI01 EF08CI02 EM13CNT106 EM13CNT107 da BNCC
//Prof. Sérgio Barroso, UESB. Disciplina MPF018 do POLO UESB/MNPEF.
//Arquivo livre para uso, mas favor citar a fonte ao utilizá-lo

//Inicializa variáveis globais
double v = 0;
double volt = 0;
unsigned long currentMillis = 0;
unsigned long ultimoMillis = 0;
unsigned long comecaMillis = 0;
String ssaida = "";
String entrada = "";
int atual=0;
int conta=0;

void setup() {
  // Aqui vai o setup, que o Arduíno roda antes de começar a função loop()

  //Configura o pino digital 8 do Arduino para modo de saída
  //Esse pino irá controlar a carga/descarga do capacitor
  pinMode(8, OUTPUT);

  //Configura o pino analógico 10 do Arduino para modo de entrada
  //Esse pino irá ler a tensão no capacitor pelo ADC
  pinMode(A0, INPUT);

  //Configura a porta serial do Arduino para 9600 bauds.
  //Outros parâmetros podem ser especificados (número de bits, paridade e bits de parada). 
  //Usamos os valores padrão (8, sem paridade e 1)
  Serial.begin(9600);

  delay(5000);

  do {
    Serial.println('OK');
    delay(100);
    entrada=Serial.readStringUntil('\n');
    delay(100);
  } while (entrada!="OK");


}

void loop() {
  // Aqui vai o código que o Arduino executa repetidamente.
  // Notar que esse código fica na memória do Arduino mesmo quando 
  // ele é desligado.

  if (conta==0) {
    ssaida = "CLEARDATA";
    Serial.println(ssaida);
    ssaida = "LABEL,TEMPO(ms),TENSAO(V)";
    Serial.println(ssaida);
  }  
  
  
  entrada="";
  // Faz um ciclo de descarga do capacitor, 
  // para garantir que o capacitor está descarregado antes de começar.
  // O capacitor pode ser descarregado manualmente antes do começo, para
  // encurtar este ciclo.
  digitalWrite(8,LOW);
  //Serial.println("Descarga inicial");
  //Esse loop lê a entrada A0 até que o valor seja 
  //menor ou igual a 1. Notar que o valor lido não está em volts, mas sim
  //em níveis do ADC:
  //1023 corresponde a 5V
  // 0 corresponde a 0V
  do {
  volt = analogRead(A0);
  } while (volt > 1);
  //Capacitor descarregado. Começa o ciclo de carga
  //Manda a string "Carregando" pela porta serial
  //Serial.println("Carregando");
  //Começa a carregar o capacitor colocando HIGH (5V) no pino 8
  digitalWrite(8, HIGH);
  if (conta==0) {
    //Armazena o instante inicial em milisegundos
    comecaMillis=millis();
  }
  //Esse loop do lê continuamente a entrada A0 até o nível
  // do ADC cheguar em 1020. Rigorosamente falando deveria ser 1023,
  // Mas, para não demorar e evitar efeitos de ruídos, usa-se 1020. 
  do {
    volt = analogRead(A0);
    //Converte o nível lido do ADC em volts
    v = (5*volt)/1023;
    //Calcula o tempo decorrido desde o início do ciclo de carga
    currentMillis = millis()-comecaMillis;    //Tempo atual em ms
    //Escreve na saída serial t e v
    ssaida = "DATA," + String(currentMillis) + "," + String(v);
    Serial.println(ssaida);
  } while (volt < 1020);
  //Inicia o ciclo de descarga do capacitor
  //Serial.println("Descarregando");
  //Começa a descarregar o capacitor colocando LOW (0V) no pino 8
  digitalWrite(8, LOW);
  //Esse loop do lê continuamente a entrada A0 até o nível
  // do ADC cheguar em 1. Rigorosamente falando deveria ser 0,
  // Mas, para não demorar e evitar efeitos de ruídos, usa-se 1.   
  do {
    volt = analogRead(A0);
    v = (5*volt)/1023;
    currentMillis = millis()- comecaMillis;    //Tempo atual em ms  
    ssaida = "DATA," + String(currentMillis) + "," + String(v);
    Serial.println(ssaida);
  } while (volt > 1);
  conta+=1;
  if (conta==5) {
    ssaida = "ROW,SET,2";
    Serial.println(ssaida);
    delay(5000);
    conta=0;
  }
  //Escreve 'FIM' na porta serial
  //Serial.println("FIM");
}
