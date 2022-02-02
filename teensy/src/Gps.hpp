#ifndef __SENSORS_HPP__
#define __SENSORS_HPP__
#include <ArduinoJson.h>
#include "Json.hpp"
#include <TinyGPS.h>


using namespace json;

#define Uart Serial2
void init();
void getGpsData(Data &data);
void gpsUpdate();
bool isDataReady();

#endif