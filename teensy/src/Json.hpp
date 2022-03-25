#ifndef __JSON_HPP__
#define __JSON_HPP__
#include <ArduinoJson.h>

namespace json {
    struct Data {
        Data();
        float fr_data;
        float fl_data;
        float f_data;
        float l_data;
        float r_data;
        double course;//gps.course (10^-2 deg)
        float latitude;
        float longitude;
        float altitude;
        float speed;//gps.f_speed_mps()
        float accelX;
        float accelY;
        float accelZ;
        float magX;
        float magY;
        float magZ;
        float magCourse;
        void sendJson();
    };
}



#endif
