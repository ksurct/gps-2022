#include "Json.hpp"

json::Data::Data() {
    
}


void json::Data::sendJson() {
    StaticJsonDocument<1000> doc;
    // Distance Sensors
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