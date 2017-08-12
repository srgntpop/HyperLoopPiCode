#include <Wire.h>
/*
 * Temperature Sensor Arduino Slave Code
 * I2C comm: slave address = 2
 * convert analogIn to temperature
 * write to master when data is requested
 */
 
void writeString(String stringData);
float analogToTemp();
void requestEvent(float temperature);

int tempSenseIndex = 0;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(2);                // join i2c bus with address #2
  Wire.onRequest(requestEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()
  byte dataSize = stringData.length();
  Wire.write(dataSize);
  for (int j = 0; j < stringData.length(); j++)
  {
    Wire.write(stringData[j]);   // Push each char 1 by 1 on each loop pass
  }
}// end writeString

float analogToTemp(){
  //  voltage = analogIn(analogPin=x)*5.0 / 1023.0;
  float temperature = 0.0;
  float voltage = 0.0;
  if (tempSenseIndex == 0){
      voltage = analogRead(A0) * 5.0 / 1023.0;
      Serial.print("transistor 1: "); 
  } else if (tempSenseIndex == 1) {
      voltage = analogRead(A1) * 5.0 / 1023.0;
      Serial.print("transistor 2: "); 
  } else if (tempSenseIndex == 2) {
      voltage = analogRead(A2) * 5.0 / 1023.0;
      Serial.print("transistor 3: ");
  } else {
      Serial.print("incorrect temp index: ");
      tempSenseIndex = 0;  
  }
  Serial.println(voltage);
  //  scaleFactor = degrees/volt
  temperature = ((voltage - 0.5) / 0.01 * 1.8) + 32.0;
  //  temperature = voltage * scaleFactor;
  tempSenseIndex++;
  return temperature;
}

void requestEvent(){
  float temperature = analogToTemp();
  if (tempSenseIndex >= 3) {
    tempSenseIndex = 0;
  }
  String tempStr = String(temperature, 2);
  writeString(tempStr);  
}
