#ifndef __SENSORS_HPP__
#define __SENSORS_HPP__
#include <ArduinoJson.h>
#include <Adafruit_FXAS21002C.h>
#include <Adafruit_FXOS8700.h>
#include <Adafruit_Sensor.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include "Json.hpp"

using namespace json;

void sensorsInit(Data* dataReference);
void setNorm();
void getAccelData();
void sensorTrigger();
void frReceived();
void rReceived();
void lReceived();
void flReceived();
void fReceived();

//void basicInterruptFunction();
//int sensorInterruptFunction(int epin, int tpin);
//int sensorDataFunction(int sizeOfDistances, int epin, int tpin);
//void getSonsorData(Data& data);
//void updateSensorData(int sizeOfDistances, Data& data);


#define echoPinF1 32 // fr
#define trigPinF1 29 // fr
#define echoPinF2 30 // r
#define trigPinF2 28 // r
#define echoPinF3 38 // l
#define trigPinF3 37 // l
#define echoPinF4 39 // fl
#define trigPinF4 36 // fl
#define echoPinF5 34 // f
#define trigPinF5 33 // f

#endif