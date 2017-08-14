#include <Wire.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(1); // join i2c bus (address optional for master)
}

void loop() {
  // put your main code here, to run repeatedly:
  Wire.requestFrom(2, 1); // request 4 bytes from slave 2
  byte tempAmbientDataSize = 0;
  if (Wire.available() <= 1){
    tempAmbientDataSize = Wire.read();
  }
  Wire.requestFrom(2, tempAmbientDataSize);
  char tempAmbient[tempAmbientDataSize];
  if (Wire.available() <= tempAmbientDataSize){
    for (byte i = 0; i < tempAmbientDataSize; i++){
      tempAmbient[i] = Wire.read();
    }
  }
  
  else {
    Serial.println("Request unavailable");
  }
  delay(100);
}
