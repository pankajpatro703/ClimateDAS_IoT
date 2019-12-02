//Code for Arduino UNO connected with sensors

char data[15];
String light1,temp1;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int light=analogRead(A0)*(52/12)+5;
  int temp=analogRead(A1)*500/1023;
  if(light<10)
    light1=String(0)+String(light);
  else
    light1=String(light);
  if(temp<10)
    temp1=String(0)+String(temp);
  else
    temp1=String(temp);
  Serial.println("*"+light1+temp1+"#");
  delay(30000);
}
