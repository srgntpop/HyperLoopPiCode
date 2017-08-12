#include <Wire.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(1); // join i2c bus (address optional for master)
}

void loop() {
  // put your main code here, to run repeatedly:
  Wire.requestFrom(2,4); // request 4 bytes from slave 2
  char tempIn[4] = {0,0,0,0};
  if (Wire.available() <= 4){   // check if 4 bytes are available
    for (byte i = 0; i < 4; i++){
      char byteIn = Wire.read();    // receive byte as an integer
      tempIn[i] = byteIn;
      Serial.print(byteIn);
    }
    Serial.println();
//    Serial.print("tempIn: ");
//    Serial.println(tempIn);
  }
  
  else {
    Serial.println("Request unavailable");
  }
  delay(100);
}
