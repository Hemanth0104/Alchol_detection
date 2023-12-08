/*
  Alcohol Detection
*/

#include<LiquidCrystal.h>

#define buzzer 2
#define LED 3
#define sensorAnalog A1
#define button 8
#define LED2 13

int limit = 400;
int count = 0;
int timer = 20;
int emergency = false;

LiquidCrystal lcd(12, 11, 7, 6, 5, 4);

void setup() 
{
  pinMode(sensorAnalog, INPUT);
  pinMode(LED, OUTPUT);
  pinMode(buzzer, OUTPUT);
  lcd.begin(16, 2); 
  pinMode(LED2, OUTPUT);
  pinMode(button, INPUT); 
  Serial.begin(9600);
}

void loop() 
{
  int val = analogRead(sensorAnalog);
  Serial.print("Analog value : ");
  Serial.print(val);
  Serial.print("\n");
  
  if(emergency==true)
  {
    digitalWrite(LED2, HIGH);
    lcd.setCursor(1,0);          
    lcd.print("Emergency Mode");
    lcd.setCursor(3,1);          
    lcd.print("Activated!");
  } 
  else if(val > limit) 
  {
    count = count + 1;
    tone(buzzer, 650);
    digitalWrite(LED, HIGH);
    delay(250);
    noTone(buzzer);
    digitalWrite(LED, LOW);
    delay(250);
  } 
  else 
  {
    count = 0;
    timer = 20;
    lcd.setCursor(0,0);          
    lcd.print("                ");
    lcd.setCursor(0,1);          
    lcd.print("                ");
    emergency = false;
    digitalWrite(LED2, LOW);
    digitalWrite(LED, LOW);
    digitalWrite(buzzer, LOW);
  }
  
  if(count>=40 && count%2==0 && count<80 && emergency==false)
  {
    lcd.setCursor(0,0);          
    lcd.print("Emergency Mode??");
    lcd.setCursor(5,1);          
    lcd.print("00:");
    if(timer>=10)
    {
      lcd.setCursor(8,1);
      lcd.print(timer);
    }
    else
    {
      lcd.setCursor(8,1);
      lcd.print("0");
      lcd.setCursor(9,1);
      lcd.print(timer);
    }
    timer = timer - 1;
  }
  
  if(count>=40 && count<80)
  {
    if (digitalRead(button) == HIGH) 
    {
      emergency = true;
      digitalWrite(LED2, HIGH);
      lcd.setCursor(0,0);          
      lcd.print("                ");
      lcd.setCursor(0,1);          
      lcd.print("                ");
      lcd.setCursor(1,0);          
      lcd.print("Emergency Mode");
      lcd.setCursor(3,1);          
      lcd.print("Activated!");
    } 
    while(digitalRead(button) == true);
    delay(50);
  }
  
  if(count==80)
  {
    lcd.setCursor(0,0);          
    lcd.print("                ");
    lcd.setCursor(0,1);          
    lcd.print("                ");
    lcd.setCursor(5,0);          
    lcd.print("Danger");
    lcd.setCursor(1,1);          
    lcd.print("Engine Locked!");
  }
  
  
  
   
}