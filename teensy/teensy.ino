#include "src/Json.hpp"
#include "src/Gps.hpp"
#include "src/Sensors.hpp"

json::Data data;

void setup()
{
    Serial.begin(115200);
    sensorsInit(&data);
    init();
}

unsigned long time = millis();
unsigned long interval = 5000;

void loop()
{
    gpsUpdate();
    getAccelData();
    if (Serial.available()){
        while (Serial.available()) {
            Serial.read();
        }
        if(isDataReady()){
            getGpsData(data);
        }
        // getSesnorData();
        data.sendJson();
        time += interval;
    }
    
}



