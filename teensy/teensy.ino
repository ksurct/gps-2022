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
bool constantOut = false;
unsigned long constantOutTimer;
uint16_t constantOutInterval = 200;

void loop()
{
    gpsUpdate();
    getAccelData();
    if (Serial.available()){
        while (Serial.available()) {
            if (Serial.read() == 'c') {
                constantOut = !constantOut;
                constantOutTimer = millis();
            }
        }
        if(isDataReady()){
            getGpsData(data);
        }
        // getSesnorData();
        data.sendJson();
        time += interval;
    }
    if (constantOut && millis() - constantOutTimer > constantOutInterval) {
        data.sendJson();
    }
}



