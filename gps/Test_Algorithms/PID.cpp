//This is example code of a PID controller that could be translated to python if needed - Jackson


int P;
int I;
int D;

int lastError = 0;


void PID_control() {
  //uint16_t position = qtr.readLineBlack(sensorValues);
  
            // v this number might be different below 'v'
  int error = 3500 - position; //need to figure out error function (read in current position and figure out what it is suppose to be)

  P = error;
  I = I + error;
  D = error - lastError;
  lastError = error;
  int motorspeed = P*Kp + I*Ki + D*Kd;
  
  int motorspeeda = basespeeda + motorspeed;
  int motorspeedb = basespeedb - motorspeed;
  

//need to make left and right motors the same speed
  if (motorspeeda > maxspeeda) {
    motorspeeda = maxspeeda;
  }
  if (motorspeedb > maxspeedb) {
    motorspeedb = maxspeedb;
  }
  if (motorspeeda < 0) {
    motorspeeda = 0;
  }
  if (motorspeedb < 0) {
    motorspeedb = 0;
  } 
  //Serial.print(motorspeeda);Serial.print(" ");Serial.println(motorspeedb);
  //forward_brake(motorspeeda, motorspeedb);
}