#include <Wire.h>

/*
 * Receive accelerometer data from Pi ()
 * Receive sensor data from slaves (almost done)
 * Send final data to Pi ()
 * Send acceleromter data to actuator slave ()
 */
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(1); // join i2c bus (address optional for master)
  //Wire.onRequest();
}

// temp1,2,3
// BMS: i1, i2, v1, v2
// Actuator dist (and voltage?): s0,s1,b0,b1,b2,b3
void loop() {
  // put your main code here, to run repeatedly:
  finalSlaveData[52];
  
  // request all temp data from slave 2
  Wire.requestFrom(2, 12); 
  char finalTemp[12];
  memset(finalTemp, 0, sizeof(finalTemp));
  if (Wire.available() <= 12){
    for (byte i = 0; i < 12; i++){
      finalTemp[i] = Wire.read();
      finalSlaveData[i] = finalTemp[i];
    }
  }
  Serial.print("final temp data: ");Serial.println(finalTemp);

  // request 16 bytes from actuators
  Wire.requestFrom(3, 24); // request 4 bytes from slave 2
  // request all BMS data from slave 4
  char finalActDist[24];
  memset(finalActDist, 0, sizeof(finalActDist));
  if (Wire.available() <= 24){
    for (byte i = 0; i < 24; i++){
      finalActDist[i] = Wire.read();
      finalSlaveData[i+12] = finalActDist[i];
    }
  }
  Serial.print("final act data: ");Serial.println(finalActDist);

  Wire.requestFrom(4, 16); // request 4 bytes from slave 2
  // request all BMS data from slave 4
  char finalBMS[16];
  memset(finalBMS, 0, sizeof(finalBMS));
  if (Wire.available() <= 16){
    for (byte i = 0; i < 16; i++){
      finalBMS[i] = Wire.read();
      finalSlaveData[i+12+24] = finalActDist[i];
    }
  }
  Serial.print("final BMS data: ");Serial.println(finalBMS);

  Serial.print("final slave data: ");Serial.println(finalSlaveData);
  
  delay(10);

}
