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
        double angle;//gps.course (10^-2 deg)
        double latitude;
        double longitude;
        double speed;//gps.f_speed_mps()
        void sendJson();
    };
}



#endif
