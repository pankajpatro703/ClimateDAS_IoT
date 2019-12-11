/*
  Arduino code to display the data received serially from Bolt module
  The data is displayed on a 16x2 LCD display using 4 parallel lines
*/

#include <LiquidCrystal.h>
#define MAX_DATA 4     //Maximum number of data read from Bolt
//1st 2 integers are fixed(i.e, light intensity and temperature)
//3rd integer changes depending on the season
//4th integer is used to denote the season

const int rs = 12, en = 11, d4 = 10, d5 = 9, d6 = 8, d7 = 7;  //LCD pin configuration

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  lcd.begin(16,2);    //16x2 LCD
  delay(200);
  Serial.begin(9600);   //Baud rate 9600bps
}

int digit=0,i=0,val,sign=1;
int data[MAX_DATA];     //retrieved data
char message[16];       //LCD message

void loop() {
  while(Serial.available()>0) {
    char inChar = Serial.read();
    if (isDigit(inChar)) {
      val = int(inChar)-48;   //convert ascii value to number
      digit=digit*10+val*sign;
    }
    else if(inChar==' ' || (inChar=='\n' && i==MAX_DATA-1)) {
      data[i]=digit;       //store data
      i++;                 //for next data
      digit=0;
    }
    else if(inChar =='\n') {
      lcd.setCursor(0,0);                                 //for first line in LCD
      sprintf(message,"L:%dlux T:%dC",data[0],data[1]);   //light intensity, temperature
      lcd.print(message);                                 //print message
      lcd.setCursor(0,1);                                 //for second line in LCD
      if(data[3]==0)					  //during summers
	      sprintf(message,"Maximum temp:%dC",data[2]);
      else if(data[3]==1)                                 //during monsoon
        sprintf(message,"Rain chances:%d%c",data[2],37);  //37 is ASCII for %
      else if(data[3]==2)                                 //during winters
        sprintf(message,"Minimum temp:%dC",data[2]); 
      lcd.print(message);                                 //print message
      i=0;
      digit=0;
    }
    sign=(inChar=='-')?(-sign):(sign);                    //if '-' sign is found
  }
}
