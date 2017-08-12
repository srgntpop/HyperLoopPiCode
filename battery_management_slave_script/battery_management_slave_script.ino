#include <Wire.h>

/*
 * Battery Management System Arduino Slave Code
 * I2C comm: slave address = 4
 * 2 Current Sensors --> output * (current/voltage)
 * 2 Voltage Sensors --> output * (voltage/voltage)
 * 
 * Send current and voltage of both batteries
 */

#define voltagePin1 A1
#define currentPin1 A0

#define voltagePin1 A3
#define currentPin1 A2

const int numReadings = 30;

float readings1[numReadings];      // the readings from the analog input
int index1 = 0;                  // the index of the current reading
float total1 = 0.0;                  // the running total
float average1 = 0.0;                // the average
float currentValue1 = 0.0;
float voltage1 = 0.0;

float readings2[numReadings];      // the readings from the analog input
int index2 = 0;                  // the index of the current reading
float total2 = 0.0;                  // the running total
float average2 = 0.0;                // the average
float currentValue2 = 0.0;
float voltage2 = 0.0;

void writeString(String stringData);
float analogToVoltage();
float analogToCurrent();
void requestEvent(float temperature);


void setup() {
  // put your setup code here, to run once:
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onRequest(requestEvent); // register event
  Serial.begin(9600);           // start serial for output
  for (int thisReading = 0; thisReading < numReadings; thisReading++){
    readings1[thisReading] = 0;   
    readings2[thisReading] = 0;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  total1 = total1 - readings1[index1];
  readings1[index1] = analogRead(currentPin1); //Raw data reading
  //Data processing:510-raw data from analogRead when the input is 0;
  
  // 5-5v; the first 0.04-0.04V/A(sensitivity); the second 0.04-offset val;
  readings1[index1] = (readings1[index1]-512)*5/1024/0.04+0.27;

  total1 = total1 + readings1[index1];       
  index1 = index1 + 1;                    
  if (index1 >= numReadings)              
    index1 = 0;                           
  average1 = total1/numReadings;   //Smoothing algorithm (http://www.arduino.cc/en/Tutorial/Smoothing)    
  currentValue1 = average1;
  
  Serial.print("current: ");
  Serial.println(currentValue1);
  Serial.print("voltage: "); 
  Serial.println(analogToVoltage(voltagePin1));
  delay(10);

  // put your main code here, to run repeatedly:
  total2 = total2 - readings2[index2];
  readings2[index2] = analogRead(currentPin2); //Raw data reading
  //Data processing:510-raw data from analogRead when the input is 0;
  
  // 5-5v; the first 0.04-0.04V/A(sensitivity); the second 0.04-offset val;
  readings2[index2] = (readings2[index2]-512)*5/1024/0.04+0.27;

  total2 = total2 + readings2[index2];       
  index2 = index2 + 1;                    
  if (index2 >= numReadings)              
    index2 = 0;                           
  average2 = total2/numReadings;   //Smoothing algorithm (http://www.arduino.cc/en/Tutorial/Smoothing)    
  currentValue2 = average2;
  
  Serial.print("current: ");
  Serial.println(currentValue2);
  Serial.print("voltage: "); 
  Serial.println(analogToVoltage(voltagePin2));
  delay(10);
}

// Used to serially push out a String with Serial.write()
// Push each char 1 by 1 on each loop pass
void writeString(String stringData) { 
  byte dataSize = stringData.length();
  Wire.write(dataSize);
  for (int j = 0; j < stringData.length(); j++)
  {
    Wire.write(stringData[j]);   
  }
}

// write 16 bytes - check it
void requestEvent(){
  String currentString1 = String(currentValue1, 2);
  writeString(currentString1);
  String voltageString1 = String(voltage1, 2);
  writeString(voltageString1);
  
  String voltageString2 = String(voltage2, 2);
  writeString(voltageString2);
  String voltageString2 = String(voltage2, 2);
  writeString(voltageString2);
}

float analogToVoltage(byte analogPin){
  voltage = 0.0;
  voltage = analogRead(analogPin)*22/1023.0;
  return voltage;
}

float analogToCurrent(byte analogPin){
  float current = 0.0;
  current = analogRead(analogPin); // * 25.0; // 40mV per 1A --> scaleFactor = 25
  return current;
}

