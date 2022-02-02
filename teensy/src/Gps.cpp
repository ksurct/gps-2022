#include "Gps.hpp"
#include "Json.hpp"

static bool dataReady = false;
static TinyGPS gps;

void init(){
    Uart.begin(9600);
    gps
}

bool isDataReady(){
    return dataReady;
}

void gpsUpdate(){

    unsigned long start = millis();

    // Every 5 seconds we print an update
    while (millis() - start < 5000) {
        if (Uart.available()) {
        char c = Uart.read();
        Serial.print(c);  // uncomment to see raw GPS data
        if (gps.encode(c)) {
        dataReady = true;
        // break;  // uncomment to print new data immediately!
      }
    }

  }
}

void getGpsData(Data &data){
    unsigned long age
    gps.get_position(&data.latitude, &data.longitude, age);
    data.speed = gps.f_speed_mps();
}