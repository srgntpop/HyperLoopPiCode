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

void loop() {
  // final data array 
  // sensor data: numbytes
  // temperature: 4
  // color: ???(4 for RGB?)
  // BMS: ??? (12?)
  // actuator x 6: 4 * 6 = 24
  // ------------------------
  // total Bytes = 44; --> padded to 44
  
//  char finalData[44];
//  memset(finalData, 0, sizeof(finalData));

  // request temperature data 
  Wire.requestFrom(2, 1);
  if (Wire.available() <= 4){
    byte dataSize2 = Wire.read();
  }
  Wire.requestFrom(2, dataSize2); // request 4 bytes from slave 2
  char tempIn[dataSize2];
  memset(tempIn, 0, sizeof(tempIn));
  if (Wire.available() <= dataSize2){   // check if 4 bytes are available
    for (byte i = 0; i < dataSize2; i++){
      char byteIn = Wire.read();    // receive byte as an integer
      tempIn[i] = byteIn;
      finalData[i] = byteIn;
//      Serial.print(byteIn);
    }
//    Serial.println();
    Serial.print("tempIn: ");
    Serial.println(tempIn);
  }

  Wire.requestFrom(3, 1);
  if (Wire.available() <= 1){
    byte dataSize3 = Wire.read();
  }
  // request actuator data 
  Wire.requestFrom(3,24); // request 4 bytes from slave 2
  char tempIn[4] = {0,0,0,0};
  if (Wire.available() <= 4){   // check if 4 bytes are available
    for (byte i = 0; i < 4; i++){
      char byteIn = Wire.read();    // receive byte as an integer
      tempIn[i] = byteIn;
      finalData[i] = byteIn;
//      Serial.print(byteIn);
    }
//    Serial.println();
    Serial.print("tempIn: ");
    Serial.println(tempIn);
  }

  
  /*
   * wire.requestFrom(4, 1);
   * byte dataSize = Wire.read();
   * wire.requestFrom(4, dataSize);
   * if (wire.available <= dataSize);
   */
  // request battery current and voltage data
  Wire.requestFrom(4,16); // request 4 bytes from slave 2
  char bmsIn[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  // CHECK IF IT IS ALWAYS 16 BYTES
  if (Wire.available() <= 16){   // check if 4 bytes are available
    for (byte i = 0; i < 16; i++){
      char byteIn = Wire.read();    // receive byte as an integer
      bmsIn[i] = byteIn;
      finalData[i+4] = byteIn;        // HARD-CODED from the previous bytes received
    }

    Serial.print("bmsIn: ");
    Serial.println(bmsIn);
  }

  
  else {
    Serial.println("Request unavailable");
  }
  delay(100);
}


