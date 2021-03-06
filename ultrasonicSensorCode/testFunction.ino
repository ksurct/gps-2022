

struct SensorData {
   int fr_data;
   int fl_data;
   int f_data;
   int l_data;
   int r_data;
};
void setup(){
Serial.begin(115200);
/*
On current board
fr (front-right) = TOF1
fl (front-left) = TOF4
f (front) = TOF5
l (left) = TOF3
r (right) = TOF2
*/
#define echoPinF1 32 
#define trigPinF1 31 
#define echoPinF2 30
#define trigPinF2 29
#define echoPinF3 38
#define trigPinF3 37
#define echoPinF4 36
#define trigPinF4 35
#define echoPinF5 34
#define trigPinF5 33

//sets the trig pins as outputs
pinMode(trigPinF1, OUTPUT);
pinMode(trigPinF2, OUTPUT);
pinMode(trigPinF3, OUTPUT);
pinMode(trigPinF4, OUTPUT);
pinMode(trigPinF5, OUTPUT);
}
int sensorDataFunction(){

long duration1; // variable for the duration of sound wave travel
int distance1; // variable for the distance measurement

 int distance[sizeOfDistances];
  for(int i = 0; i < sizeOfDistances; i++){
  digitalWriteFast(tpin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWriteFast(tpin, HIGH);
  delayMicroseconds(1);
  digitalWriteFast(tpin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  // Calculating the distance
  distance[i] = pulseIn(epin, HIGH, 3000) * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  }
  int average = 0;
  int elements = 0;
  for(int i = 0; i < sizeOfDistances; i++){
    if(distance[i] <= 200 && distance[i] != 0){
      average += distance[i];
      elements++;
    }
  }
  if(elements != 0){
    average = average / elements;
    return average;
  }else{
    return -1;
  }
}

SensorData collectData(int sizeOfDistances){
  SensorData data;
  data.fr_data = sensorDataFunction(sizeOfDistances, echoPinF1, trigPinF1);
  data.r_data = sensorDataFunction(sizeOfDistances, echoPinF2, trigPinF2);
  data.l_data = sensorDataFunction(sizeOfDistances, echoPinF3, trigPinF3);
  data.fl_data = sensorDataFunction(sizeOfDistances, echoPinF4, trigPinF4);
  data.f_data = sensorDataFunction(sizeOfDistances, echoPinF5, trigPinF5);
  return data;
}

void loop(){
SensorData data = collectData(6);
Serial.print("right Distance: ");
Serial.print(data.r_data);
Serial.print(", ");
Serial.print("left Distance: ");
Serial.print(data.l_data);
Serial.print(", ");
Serial.print("right front Distance: ");
Serial.print(data.fr_data);
Serial.print(", ");
Serial.print("left front Distance: ");
Serial.print(data.fl_data);
Serial.print(", ");
Serial.print("front Distance: ");
Serial.println(data.f_data);

}
