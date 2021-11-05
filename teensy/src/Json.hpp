#ifndef __JSON_HPP__
#define __JSON_HPP__
#include <ArduinoJson.h>

namespace json {
    struct Data {
        static const int NUM_ENCODERS = 4;
        static const int NUM_SENSORS = 8;
        double sensors[NUM_SENSORS];
        double encoderSpeeds[NUM_ENCODERS];
        void sendJson();
    private:
        Data();
    };
}

#endif
