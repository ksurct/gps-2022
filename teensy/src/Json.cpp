
#include "Json.hpp"

json::Data::Data() {
    #define clr(x) memset(x, 0, sizeof(x))
    clr(encoderSpeeds);
    clr(sensors);
    #undef clr
}


void json::Data::sendJson() {
    StaticJsonDocument<1000> doc;
    auto encoderArray = doc.createNestedArray("encoders");
    for (int i = 0; i < NUM_ENCODERS; i++) {
        encoderArray.add(encoderSpeeds[i]);
    }
    // Array of Distance Sensors
    auto sensorArray = doc.createNestedArray("sensors");
    for (int i = 0; i < NUM_SENSORS; i++) {
        sensorArray.add(sensors[i]);
    }
    // Hall's Effect Sensor
    doc["hallEffect"] = hallEffect;

    serializeJsonPretty(doc, Serial);
}