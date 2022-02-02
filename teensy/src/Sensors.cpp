#include "Sensors.hpp"
#include "Json.hpp"

using namespace json;

void sensorsInit(){
    pinMode(trigPinF1, OUTPUT);
    pinMode(trigPinF2, OUTPUT);
    pinMode(trigPinF3, OUTPUT);
    pinMode(trigPinF4, OUTPUT);
    pinMode(trigPinF5, OUTPUT);
}

int sensorDataFunction(int sizeOfDistances, int epin, int tpin){

long duration1; // variable for the duration of sound wave travel
int distance1; // variable for the distance measurement

 int distance[sizeOfDistances];
  for(int i = 0; i < sizeOfDistances; i++){
  digitalWriteFast(tpin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWriteFast(tpin, HIGH);
  delayMicroseconds(1);
  digitalWriteFast(tpin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  // Calculating the distance
  distance[i] = pulseIn(epin, HIGH, 3000) * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  }
  int average = 0;
  int elements = 0;
  for(int i = 0; i < sizeOfDistances; i++){
    if(distance[i] <= 200 && distance[i] != 0){
      average += distance[i];
      elements++;
    }
  }
  if(elements != 0){
    average = average / elements;
    return average;
  }else{
    return -1;
  }
}

void collectData(int sizeOfDistances, Data& data){
  data.fr_data = sensorDataFunction(sizeOfDistances, echoPinF1, trigPinF1);
  data.r_data = sensorDataFunction(sizeOfDistances, echoPinF2, trigPinF2);
  data.l_data = sensorDataFunction(sizeOfDistances, echoPinF3, trigPinF3);
  data.fl_data = sensorDataFunction(sizeOfDistances, echoPinF4, trigPinF4);
  data.f_data = sensorDataFunction(sizeOfDistances, echoPinF5, trigPinF5);
}