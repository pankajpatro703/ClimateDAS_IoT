//Code for Arduino UNO at the LCD display end

#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 10, d5 = 9, d6 = 8, d7 = 7;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  lcd.begin(16,2);
  delay(200);
  Serial.begin(9600);
}

int n=0;
int val;
int i=0;
int a[3];
char data[16];

void loop() {
  while(Serial.available()>0) {
    char inChar = Serial.read();
    if (isDigit(inChar)) {
      val = int(inChar)-48;
      n=n*10+val;
    }
    else if(inChar==' ' || (inChar=='\n' && i==2))
    {
      a[i]=n;
      i++;
      n=0;
    }
    else if(inChar =='\n') {
      lcd.setCursor(0,0);
      sprintf(data,"L:%dlux T:%dC",a[0],a[1]);
      lcd.print(data);
      lcd.setCursor(0,1);
      sprintf(data,"Rain chances:%d%c",a[2],37);
      lcd.print(data);
      i=0;
      n=0;
    }
  }
}
