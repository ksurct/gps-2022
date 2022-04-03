#include "Json.hpp"
#include <string.h>


json::Data::Data() {
    memset((uint8_t*)this, 0, sizeof(Data));
    fr_data = -1;
    f_data = -1;
    fl_data = -1;
    r_data = -1;
    l_data = -1;
}


void json::Data::sendJson() {
    StaticJsonDocument<1000> doc;
    // Distance Sensors
    
    doc["magCourse"] = magCourse;
    
    doc["fr_data"] = fr_data;
    doc["fl_data"] = fl_data;
    doc["f_data"] = f_data;
    doc["l_data"] = l_data;
    doc["r_data"] = r_data;

    //GPS Course (Heading)
    doc["course"] = course;

    // Hall's Effect Sensor
    doc["longitude"] = longitude;
    doc["latitude"] = latitude;
    doc["altitude"] = altitude;

    //GPS Speed (in mps)
    doc["speed"] = speed;

    //Accel Data (in m/s^2)
    doc["accelX"] = accelX;
    doc["accelY"] = accelY;
    doc["accelZ"] = accelZ;

    //Accel Data (in uT)
    doc["magX"] = magX;
    doc["magY"] = magY;
    doc["magZ"] = magZ;

    

    serializeJson(doc, Serial);
    Serial.println("");
}