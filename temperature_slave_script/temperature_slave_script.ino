#include <Wire.h>
/*
 * Temperature Sensor Arduino Slave Code
 * I2C comm: slave address = 2
 * convert analogIn to temperature
 * write to master when data is requested
 */
#define ambientPin A0
#define batteryPin A1
#define piPin A2

void writeString(String stringData);
float analogToTemp(byte pinNum);
void requestEvent(float temperature);


void setup() {
  // put your setup code here, to run once:
  Wire.begin(2);                // join i2c bus with address #2
  Wire.onRequest(requestEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  // put your main code here, to run repeatedly:
  // WATCH OUT FOR AN INCORRECT DELAY
  delay(10);
}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()
//  byte dataSize = stringData.length();
//  Wire.write(dataSize);
  for (int j = 0; j < stringData.length(); j++)
  {
    Wire.write(stringData[j]);   // Push each char 1 by 1 on each loop pass
  }
}// end writeString

float analogToTemp(byte pinNum){
  float temperature = 0.0;
  float voltage = 0.0;
  voltage = analogRead(pinNum) * 5.0 / 1023.0; //voltage = analogIn(analogPin=x)*5.0 / 1023.0;
  Serial.println(voltage);
  temperature = ((voltage - 0.5) / 0.01 * 1.8) + 32.0; //scaleFactor = degrees/volt
  //  temperature = voltage * scaleFactor;
  return temperature;
}

void requestEvent(){
  float temperatureAmbient = analogToTemp(ambientPin);
  float temperatureBattery = analogToTemp(batteryPin);
  float temperaturePi = analogToTemp(piPin);
  String ambientStr = String(temperatureAmbient, 1);
  String batteryStr = String(temperatureBattery, 1);
  String piStr = String(temperaturePi, 1);
  String finalTempStr = ambientStr + batteryStr + piStr;
  writeString(finalTempStr);
}
