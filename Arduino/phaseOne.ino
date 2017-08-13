// AutoGrow Project
// Phase One: Power light and fans on unique cycles. Record states of each to Serial.
// ==================================================================================

// Assign output pins for fan and light
const int fanPin = 9;
const int lightPin = 10;

// Initiate light and fan states
int lightState = 0;
int fanState = 0;

// Initiate clocks for fan and light
float previousLightTime = 0.0;
float previousFanTime = 0.0;

// Set times for each cycle
float hour = 3600000.0;
float lightCycle = 6 * hour;
float fanCycle = 0.75 * hour;

void setup() {

  // Assign output pins for fan and light
  pinMode(fanPin, OUTPUT);
  pinMode(lightPin, OUTPUT);

  // Start with light and fan OFF
  digitalWrite(lightPin, HIGH);
  digitalWrite(fanPin, HIGH);

  // Open Serial port
  Serial.begin(9600);
  Serial.println("AutoGrow Initiated");
  Serial.println("=======================================");
  Serial.println("Fan off");
  Serial.println("Light off");

}


void loop() {

  // Get time in milliseconds since Arduino powered on
  long unsigned currentMillis = millis();

  // If duration of the light cycle has been exceeded..
  if(currentMillis - previousLightTime >= lightCycle){

    // Change the state of the light
    toggleLight();

    // Reset the light cycle counter
    previousLightTime = currentMillis;
    
  }

  if(lightState == 1){
    if(currentMillis - previousFanTime >= fanCycle){

      toggleFan();
      previousFanTime = currentMillis;
    }
  }

  // If the light is off, keep the fan off
  else if(lightState == 0){
    digitalWrite(fanPin, HIGH);
    fanState = 0;
  }

}

void toggleFan(){

  // If the fan is on, turn it off for 45 minutes
  if(fanState == 1){
    digitalWrite(fanPin, HIGH);
    fanState = 0;
    fanCycle = 0.75 * hour ;
    Serial.println("Fan off");
  }

  // If the fan is off, turn it on for 15 minutes
  else if(fanState == 0){
    digitalWrite(fanPin, LOW);
    fanState = 1;
    fanCycle = 0.25 * hour;
    Serial.println("Fan on");
  }  
}

void toggleLight(){
  if(lightState == 1){
    digitalWrite(lightPin, HIGH);
    lightState = 0;
    Serial.println("Light off");
  }

  else if(lightState == 0){
    digitalWrite(lightPin, LOW);
    lightState = 1;
    Serial.println("Light on");
  }  
}

