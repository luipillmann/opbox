#include <Servo.h> 

int pin = 2;
int led = 13;
int flag = 0;
volatile int reward = LOW;

Servo myservo;  // create servo object to control a servo 

void setup() {
    pinMode(led, OUTPUT);
    attachInterrupt(digitalPinToInterrupt(pin), toggle, RISING);

    myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
}

void loop() {
    
    
    if (!flag) {
      myservo.write(0); // sets servo to 0 position at the beginning
      delay(2000);  
      //flag = 1;
    }

    if(reward) { // polls reward for a change. If high, activates the motor
      giveReward();
      digitalWrite(led, reward);
    }
    
}

void toggle () {
  reward = HIGH;
  flag = 1;
}

void giveReward() {
    //state = !state;
    //digitalWrite(led, state);
    myservo.write(180);
    delay(2000);
    myservo.write(0);
    reward = LOW;
}
