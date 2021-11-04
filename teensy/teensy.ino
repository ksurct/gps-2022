#include <ArduinoJson.h>
int enPin = 10;
int state;
int lastState = HIGH;
unsigned long lastTime;

enum stat {
  triggered,
  wait,
  high,
  low
};

stat curSt = high;
stat lastSt = high;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // Array of Encoders
  JsonArray encoder = doc.createNestedArray("encoder");
  encoder.add(1.234);
  encoder.add(5.678);
  encoder.add(8.765);
  encoder.add(4.321);

  // Array of Distance Sensors
  JsonArray dist = doc.createNestedArray("distance");
  dist.add(1);
  dist.add(2);
  dist.add(3);

  // Hall's Effect Sensor
  doc["magnet"] = 1.03;

  //serializeJson(doc, Serial);

  pinMode(enPin, INPUT);
}

void loop() {
  state = digitalRead(enPin);

  switch(curSt) {
    case high:
      if(state == LOW){
        curSt = wait;
        lastTime = millis();
      }
      break;
     case low:
      if(state == HIGH){
        curSt = wait;
        lastTime = millis();
      }
      break;
     case wait:
      if(state != lastSt){
        if (millis() - lastTime >= 50){
          lastState = state;
          if (state == HIGH)
            curSt = triggered;
          else
            curSt = low;
        }
      } else
        curSt = lastSt;
      break;
     case triggered:
      serializeJson(doc, Serial);
      Serial.println();
      curSt = high;
      break;

  }
}