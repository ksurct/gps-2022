#ifndef __JSON_HPP__
#define __JSON_HPP__
#include <ArduinoJson.h>

namespace json {
    struct Data {
        Data();
        int fr_data;
        int fl_data;
        int f_data;
        int l_data;
        int r_data;
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
