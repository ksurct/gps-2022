
int sensorDataFunction(int echoPin, int trigPin, int sizeOfDistances){



#define echoPin1 echoPin // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin1 trigPin  //attach pin D3 Arduino to pin Trig of HC-SR04
pinMode(trigPin1, OUTPUT); // Sets the trigPin as an OUTPUT
 int distance[sizeOfDistances];
  for(int i = 0; i < sizeOfDistances; i++){
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(1);
  digitalWrite(trigPin1, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration1 = pulseIn(echoPin1, HIGH);
  // Calculating the distance
  distance[i] = duration1 * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  }
  int average = 0;
  int elements = 0;
  for(int i = 0; i < sizeOfDistances; i++){
    if(distance[i] <= 200){
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
