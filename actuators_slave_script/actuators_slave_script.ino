#include <Wire.h>

/*
 * Actuator Arduino Slave Code
 * I2C comm: slave address = 3
 * Engage emergency breaks on master command
 * Disengage breaks on master command
 * Write actuator distance data to master on request (done)
 * Receive accelerometer data from master
 * Implement gain control logic
 */


/*
 * analog pins: motors
 * A6, A7: silver motors
 * A0, A1, A2, A3: black motors
 */
byte silverAct0 = A6;
byte silverAct1 = A7;
byte blackAct0 = A0;
byte blackAct1 = A1;
byte blackAct2 = A2;
byte blackAct3 = A3;
//----------------------[PID Coefficients]----------------------//
float Kp = 10.00; //Proportional Constant
float Ki = 0; //Integration Constant
float Kd = 0; //Derivative Constant



// prototype functions
void disengageBreaks();
void engageBreaks();
void writeString(String stringData);
float convertAnalogInToVolts(byte analogPinIn);
float convertVoltsToDistanceSilver(float voltageIn);
float convertVoltsToDistanceBlack(float voltageIn);
void gainControlFunction();
//void initialzeMotors();
float receiveAccFromMaster();
float pid(float kp, float ki, float kd, float e_k, float e_k1, float e_k2, float u_k1);

void setup() {
  // put your setup code here, to run once:
  // actuator slave takes address 3 on i2c
  Wire.begin(3);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);

  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(pos_ref, INPUT); //Reference Signal
  pinMode(pos1, INPUT); //Feedback from potentiometer 1
  pinMode(pos2, INPUT); //Feedback from potentiometer 2
}

/*
 * constantly check for disengage break bytes
 * from i2c master
 *
 * engage breaks when interrupt received
 */
void loop() {
  // put your main code here, to run repeatedly:

  delay(100);

}

///*
// * Move motors into correct starting position
// * get values at starting position
// *
// */
//void initializeMotors(){
//
//}

//----------------------[PID Function]--------------------------//
float pid(float kp, float ki, float kd, float e_k, float e_k1, float e_k2, float u_k1){
  float a = (kp + ki / 2 + kd);
  float b = ( ki / 2 - 2 * kd - kp);
  float c = kd;

  float control = u_k1 + a * e_k + b * e_k1 + c * e_k2;
  return control;
}

/*
 * Fully disengage the breaks
 * rate: ?
 */
void disengageBreaks() {
}

/*
 * Fully engage the breaks
 * rate: ?
 */
void engageBreaks() {
}

/*
 * send actuator distances
 */
void requestEvent() {
  // get voltages
  float silver0Volts = convertAnalogInToVolts(silverAct0);
  float silver1Volts = convertAnalogInToVolts(silverAct1);
  float black0Volts = convertAnalogInToVolts(blackAct0);
  float black1Volts = convertAnalogInToVolts(blackAct1);
  float black2Volts = convertAnalogInToVolts(blackAct2);
  float black3Volts = convertAnalogInToVolts(blackAct3);

//  // get distances
//  float silver0distance = convertVoltsToDistanceSilver(silverAct0);
//  float silver1distance = convertVoltsToDistanceSilver(silverAct1);
//  float black0distance = convertVoltsToDistanceBlack(blackAct0);
//  float black1distance = convertVoltsToDistanceBlack(blackAct1);
//  float black2distance = convertVoltsToDistanceBlack(blackAct2);
//  float black3distance = convertVoltsToDistanceBlack(blackAct3);

//  // convert distances to strings
//  String distanceSilver0str = String(silver0distance, 2);
//  String distanceSilver1str = String(silver1distance, 2);
//  String distanceBlack0str = String(black0distance, 2);
//  String distanceBlack1str = String(black1distance, 2);
//  String distanceBlack2str = String(black2distance, 2);
//  String distanceBlack3str = String(black3distance, 2);

  // write strings to master
  String finalVoltStr = silver0Volts + silver1Volts +
                        black0Volts + black1Volts +
                        black2Volts + black3Volts;
                        
  writeString(finalVoltStr);
}

  /*
   *
   */
  float receiveAccFromMaster() {

  }
  
  /*
   *
   */
  void applyControlEffort(float u, int pwm_pin, int dir_pin) {
    if (u > 153){
      analogWrite(pwm_pin, 153);
      digitalWrite(dir_pin, HIGH);
    } else if (u < -153){
      analogWrite(pwm_pin, 153);
      digitalWrite(dir_pin, LOW);
    } else{
      analogWrite(pwm_pin, (int)abs(u));
      if (u > 0){
        digitalWrite(dir_pin, HIGH);
      } else {
        digitalWrite(dir_pin, LOW);
      }
    }
    return;
  }



  /*
   *
   */
  void gainControlFunction() {
    float acceleration = receiveAccFromMaster();
    float aRef = -9.8; // -1g
    float accelError = aRef - aMeasured;
    float pos_ref = kp * accelError; // position reference calculated from the acceleration


    byte pwm1 = 2; // pwm pin
    byte dir1 = 3; // direction pin
    byte pos1 = A0;  // measured position of actuator

    byte pwm2 = 4; // pwm pin
    byte dir2 = 5; // direction pin
    byte pos2 = A1; // measured position of actuaotr

    float err_1 = 0;  // calculated position error
    float err_1_1 = 0;  // previously calculated position eror
    float err_1_2 = 0;  // 2 times ago position error
    float pid_1_out = 0;  // control effort
    float pid_1_out_prev = 0; // control effort previous

    float err_2 = 0;  // calculated position error
    float err_2_1 = 0;  // previous posititon error
    float err_2_2 = 0;  // 2 times ago position error
    float pid_2_out = 0;  // calculated control effort
    float pid_2_out_prev = 0; // control effort previous

    err_1 = analogRead(pos_ref) - analogRead(pos1);    // analogPotentiometerAct -
    err_2 = analogRead(pos_ref) - analogRead(pos2);

    pid_1_out = pid(Kp, Ki, Kd, err_1, err_1_1, err_1_2, pid_1_out_prev);
    pid_2_out = pid(Kp, Ki, Kd, err_2, err_2_1, err_2_2, pid_2_out_prev);
    applyControlEffort(pid_2_out, pwm2, dir2);
    applyControlEffort(pid_1_out, pwm1, dir1);


    err_2_2 = err_2_1;
    err_2_1 = err_2;
    pid_2_out_prev = pid_2_out;

    err_1_2 = err_1_1;
    err_1_1 = err_1;
    pid_1_out_prev = pid_1_out;

  }

  /*
   * convert analog input to voltage value
   */
  float convertAnalogInToVolts(byte analogPinIn) {
    float voltage = analogRead(analogPinIn) * 5.0 / 1023.0;
    return voltage;
  }

  /*
   * convert voltage to actuator distance for silver actuators
   */
  float convertVoltsToDistanceSilver(float voltageIn) {
    float actDist = 0.0;
    actDist = voltageIn; // * scaleFactor
    return actDist;
  }

  /*
   * convert voltage to actuator distance for black actuators
   */
  float convertVoltsToDistanceBlack(float voltageIn) {
    float actDist = 0.0;
    actDist = voltageIn; // * scaleFactor
    return actDist;
  }

  // Used to serially push out a String with Serial.write()
  // Push each char 1 by 1 on each loop pass
  void writeString(String stringData) {
    //  byte dataSize = stringData.length();
    //  Wire.write(dataSize);
    for (int j = 0; j < stringData.length(); j++)
    {
      Wire.write(stringData[j]);
    }
  }
