#include "Sensors.hpp"
#include "Json.hpp"

using namespace json;
static json::Data* data;

IntervalTimer timer;
unsigned long triggerTime;
unsigned long echoFRTime;
unsigned long echoRTime;
unsigned long echoLTime;
unsigned long echoFLTime;
unsigned long echoFTime;

void sensorsInit(Data* dataReference){
    pinMode(trigPinF1, OUTPUT);
    pinMode(trigPinF2, OUTPUT);
    pinMode(trigPinF3, OUTPUT);
    pinMode(trigPinF4, OUTPUT);
    pinMode(trigPinF5, OUTPUT);
    timer.begin(sensorTrigger, 150000);
    attachInterrupt(echoPinF1, frReceived, RISING);
    attachInterrupt(echoPinF2, rReceived, RISING);
    attachInterrupt(echoPinF3, lReceived, RISING);
    attachInterrupt(echoPinF4, flReceived, RISING);
    attachInterrupt(echoPinF5, fReceived, RISING);
    data = dataReference;
}

// void basicInterruptFunction(){
//   Serial.println("tick");
// }

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
  delayMicroseconds(1);
  digitalWriteFast(trigPinF1, LOW);
  digitalWriteFast(trigPinF2, LOW);
  digitalWriteFast(trigPinF3, LOW);
  digitalWriteFast(trigPinF4, LOW);
  digitalWriteFast(trigPinF5, LOW);
  triggerTime = micros();

}

void frReceived(){
  unsigned long echoFRTime = micros();
  data->fr_data = (echoFRTime - triggerTime) * .034 / 2;
}

void rReceived(){
  unsigned long echoRTime = micros();
  data->r_data = (echoRTime - triggerTime) * .034 / 2;
}

void lReceived(){
  unsigned long echoLTime = micros();
  data->l_data = (echoLTime - triggerTime) * .034 / 2;
}

void flReceived(){
  unsigned long echoFLTime = micros();
  data->fl_data = (echoFLTime - triggerTime) * .034 / 2;
}

void fReceived(){
  unsigned long echoFTime = micros();
  data->f_data = (echoFTime - triggerTime) * .034 / 2;
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