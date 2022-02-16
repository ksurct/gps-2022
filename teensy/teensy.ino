#include "src/Json.hpp"
#include "src/Gps.hpp"
#include "src/Sensors.hpp"

json::Data data;

void setup()
{
    Serial.begin(115200);
    sensorsInit(&data);
    init();
    data.latitude = 90;
}

void loop()
{
    data.sendJson();
    Serial.println(data.f_data);
    if (Serial.available()){
        // gpsUpdate();
        if(isDataReady()){
            getGpsData(data);
        }
        // getSesnorData();
        data.sendJson();
        delay(10);
    }
    delay(10);
}
