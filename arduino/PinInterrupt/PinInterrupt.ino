#include <Servo.h> 

int pin = 2;
int led = 13;
int flag = 0;
volatile int state = LOW;

Servo myservo;  // create servo object to control a servo 

void setup() {
    pinMode(led, OUTPUT);
    attachInterrupt(digitalPinToInterrupt(pin), blink, RISING);

    myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
}

void loop() {
    digitalWrite(led, state);
    if (!flag) {
      myservo.write(0);
      delay(2000);  
      flag = 1;
    }

    if(state) {
      giveReward();
      digitalWrite(led, state);
    }
    
}

void blink () {
  state = HIGH;
}

void giveReward() {
    //state = !state;
    //digitalWrite(led, state);
    myservo.write(180);
    delay(2000);
    myservo.write(0);
    state = LOW;
}
