#include "src/Json.hpp"
#include "src/Sensors.hpp"

json::Data data;

void setup()
{
    Serial.begin(115200);
    sensorsInit();
    data.latitude = 90;
}

void loop()
{
    delay(1000);
    gpsUpdate();
    if(isDataReady()){
        getGpsData(data);
    }
    collectData(5, data);
    data.sendJson();
    Serial.println("New data: ");
}
