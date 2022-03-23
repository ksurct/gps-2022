#include "Sensors.hpp"
#include "Json.hpp"

using namespace json;
static json::Data* data;

IntervalTimer timer;
unsigned long echoFRTime;
unsigned long echoRTime;
unsigned long echoLTime;
unsigned long echoFLTime;
unsigned long echoFTime;
Adafruit_FXOS8700 accelmag = Adafruit_FXOS8700(0x8700A, 0x8700B);

void sensorsInit(Data* dataReference){
    pinMode(trigPinF1, OUTPUT);
    pinMode(trigPinF2, OUTPUT);
    pinMode(trigPinF3, OUTPUT);
    pinMode(trigPinF4, OUTPUT);
    pinMode(trigPinF5, OUTPUT);
    timer.begin(sensorTrigger, 150000);
    attachInterrupt(echoPinF1, frReceived, CHANGE);
    attachInterrupt(echoPinF2, rReceived, CHANGE);
    attachInterrupt(echoPinF3, lReceived, CHANGE);
    attachInterrupt(echoPinF4, flReceived, CHANGE);
    attachInterrupt(echoPinF5, fReceived, CHANGE);
    data = dataReference;
    if (!accelmag.begin()) {
        /* There was a problem detecting the FXOS8700 ... check your connections */
        Serial.println("Ooops, no FXOS8700 detected ... Check your wiring!");
        while (1)
            ;
    }
}

void getAccelData(){
  Serial.println("AccelData");
  sensors_event_t aevent, mevent;

  /* Get a new sensor event */
  accelmag.getEvent(&aevent, &mevent);

  data->accelX = aevent.acceleration.x;
  data->accelY = aevent.acceleration.y;
  data->accelZ = aevent.acceleration.z;
  
  data->magX = mevent.magnetic.x;
  data->magY = mevent.magnetic.y;
  data->magZ = mevent.magnetic.z;
}

void sensorTrigger(){
  digitalWriteFast(trigPinF1, LOW);
  digitalWriteFast(trigPinF2, LOW);
  digitalWriteFast(trigPinF3, LOW);
  digitalWriteFast(trigPinF4, LOW);
  digitalWriteFast(trigPinF5, LOW);
  delayMicroseconds(2);
  digitalWriteFast(trigPinF1, HIGH);
  digitalWriteFast(trigPinF2, HIGH);
  digitalWriteFast(trigPinF3, HIGH);
  digitalWriteFast(trigPinF4, HIGH);
  digitalWriteFast(trigPinF5, HIGH);
  delayMicroseconds(10);
  digitalWriteFast(trigPinF1, LOW);
  digitalWriteFast(trigPinF2, LOW);
  digitalWriteFast(trigPinF3, LOW);
  digitalWriteFast(trigPinF4, LOW);
  digitalWriteFast(trigPinF5, LOW);

}

void frReceived(){
  if(digitalReadFast(echoPinF1)){ // HIGH
    echoFRTime = micros();
  }
  else{
    data->fr_data = (micros() - echoFRTime) * .034 / 2;
    if(data->fr_data > 1000){
      data->fr_data = -1;
    }
  }
}

void rReceived(){
  if(digitalReadFast(echoPinF2)){ // HIGH
    echoRTime = micros();
  }
  else{
    data->r_data = (micros() - echoRTime) * .034 / 2;
    if(data->r_data > 1000){
      data->r_data = -1;
    }
  }
}

void lReceived(){
  if(digitalReadFast(echoPinF3)){ // HIGH
    echoLTime = micros();
  }
  else{
    data->l_data = (micros() - echoLTime) * .034 / 2;
    if(data->l_data > 1000){
      data->l_data = -1;
    }
  }
}

void flReceived(){
  if(digitalReadFast(echoPinF4)){ // HIGH
    echoFLTime = micros();
  }
  else{
    data->fl_data = (micros() - echoFLTime) * .034 / 2;
    if(data->fl_data > 1000){
      data->fl_data = -1;
    }
  }
}

void fReceived(){
  if(digitalReadFast(echoPinF5)){ // HIGH
    echoFTime = micros();
  }
  else{
    data->f_data = (micros() - echoFTime) * .034 / 2;
    if(data->f_data > 1000){
      data->f_data = -1;
    }
  }
}

// int sensorDataFunction(int sizeOfDistances, int epin, int tpin){

// long duration1; // variable for the duration of sound wave travel
// int distance1; // variable for the distance measurement

//  int distance[sizeOfDistances];
//   for(int i = 0; i < sizeOfDistances; i++){
//   digitalWriteFast(tpin, LOW);
//   delayMicroseconds(2);
//   // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
//   digitalWriteFast(tpin, HIGH);
//   delayMicroseconds(1);
//   digitalWriteFast(tpin, LOW);
//   // Reads the echoPin, returns the sound wave travel time in microseconds
//   // Calculating the distance
//   distance[i] = pulseIn(epin, HIGH, 3000) * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
//   // Displays the distance on the Serial Monitor
//   }
//   int average = 0;
//   int elements = 0;
//   for(int i = 0; i < sizeOfDistances; i++){
//     if(distance[i] <= 200 && distance[i] != 0){
//       average += distance[i];
//       elements++;
//     }
//   }
//   if(elements != 0){
//     average = average / elements;
//     return average;
//   }else{
//     return -1;
//   }
// }

// void updateSensorData(int sizeOfDistances){
//   // data.fr_data = sensorDataFunction(sizeOfDistances, echoPinF1, trigPinF1);
//   // data.r_data = sensorDataFunction(sizeOfDistances, echoPinF2, trigPinF2);
//   // data.l_data = sensorDataFunction(sizeOfDistances, echoPinF3, trigPinF3);
//   // data.fl_data = sensorDataFunction(sizeOfDistances, echoPinF4, trigPinF4);
//   data.f_data = sensorDataFunction(sizeOfDistances, echoPinF5, trigPinF5);
// }