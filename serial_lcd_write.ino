#include <Wire.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd( 8, 9, 4, 5, 6, 7 );

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  Serial.begin(9600);
}

void loop() {
  String content = "";
  char character;

  while(Serial.available()) {
    delay(10);
    character = Serial.read();
    content.concat(character);
  }
  if(content != "") {
    Serial.println(content);
    // Clear out the LCD...
    lcd.setCursor(0, 0);
    lcd.print("                ");
    lcd.setCursor(0, 1);
    lcd.print("                ");
    // Print the stuff!
    lcd.setCursor(0, 0);
    lcd.print(content.substring(0,16));
    lcd.setCursor(0, 1);
    lcd.print(content.substring(16));
  }
}
