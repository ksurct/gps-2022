#ifndef __GPS_HPP__
#define __GPS_HPP__
#include <ArduinoJson.h>
#include "Json.hpp"
#include <TinyGPS.h>

using namespace json;

#define Uart Serial1
void init();
void getGpsData(Data &data);
void gpsUpdate();
bool isDataReady();

#endif