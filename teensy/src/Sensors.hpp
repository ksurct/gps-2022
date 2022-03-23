#ifndef __SENSORS_HPP__
#define __SENSORS_HPP__
#include <ArduinoJson.h>
#include "Json.hpp"

using namespace json;

void sensorsInit();
int sensorDataFunction(int sizeOfDistances, int epin, int tpin);
void collectSensorData(int sizeOfDistances, Data& data);

#define echoPinF1 32 
#define trigPinF1 31 
#define echoPinF2 30
#define trigPinF2 29
#define echoPinF3 38
#define trigPinF3 37
#define echoPinF4 36
#define trigPinF4 35
#define echoPinF5 34
#define trigPinF5 33

#endif