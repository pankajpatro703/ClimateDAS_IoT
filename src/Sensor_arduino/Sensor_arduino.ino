/*
	Arduino code to send sensor data to ESP8266 over serial
*/
#define ADC_size 10;

String light1,temp1;
int m=0,light,temp;
float slope=0.555,intercept=-19.82;	  //obtained by plotting lux vs ADC values

void setup() {
  Serial.begin(9600);     //baudrate for communication with ESP8266
}

void loop() {
  light=analogRead(A0)*slope+intercept;   //Calibration to read light intensity in Lux
  temp=analogRead(A1)*500/(pow(2,ADC_size)-1);  //Read temperature in degree celsius
  light1=String(light);
  m=light1.length();
  while(m<3){
    light1=String(0)+light1;      //Obtain fixed size (3 digit) value
    m++;
  }
  temp1=String(temp);
  m=temp1.length();
  while(m<2){
    temp1=String(0)+temp1;        //Obtain fixed size (2 digit) value
    m++;
  }
  if(light1.length()==3 && temp1.length()==2)
    Serial.println("*"+light1+temp1+"#");   //Serial transfer to ESP8266
  delay(30000);                             //wait for 30 seconds
}
