void setup() {
  // put your setup code here, to run once:
 pinMode(2, OUTPUT);
 Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(2, HIGH);
  digitalWrite(2,LOW); // start
  funca();
  digitalWrite(2,HIGH);
  funca();
  digitalWrite(2,LOW);
  funca();
  digitalWrite(2,HIGH);
  funca();
  digitalWrite(2,LOW);
  funca();
  digitalWrite(2,LOW);
  funca();
  digitalWrite(2,HIGH);
  funca();
  digitalWrite(2,HIGH);
  funca();
  digitalWrite(2,LOW);
  funca();
  digitalWrite(2,LOW); // paridade
  funca();
  digitalWrite(2,HIGH); //stop
  delay(2000);
}

void funca(){
    for(int i = 0; i < 2187; i++)
      asm("NOP");
  }

// digitalWrite()
// digitalRead()
//
