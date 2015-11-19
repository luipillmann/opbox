#include <Time.h>
#include <Servo.h> 

//timer interrupts
//by Amanda Ghassaei
//June 2012
//http://www.instructables.com/id/Arduino-Timer-Interrupts/

/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
*/

// TimeSerial example
/* 
 * TimeSerial.pde
 * example code illustrating Time library set through serial port messages.
 *
 * Messages consist of the letter T followed by ten digit time (as seconds since Jan 1 1970)
 * you can send the text on the next line using Serial Monitor to set the clock to noon Jan 1 2013
 T1357041600  
 *
 * A Processing example sketch to automatically send the messages is inclided in the download
 * On Linux, you can use "date +T%s\n > /dev/ttyACM0" (UTC time zone)
 */ 

//timer setup for timer0, timer1, and timer2.
//For arduino uno or any board with ATMEL 328/168.. diecimila, duemilanove, lilypad, nano, mini...

//this code will enable arduino timer interrupts.
//timer1 will interrupt at 100 Hz

#define LOG_HEADER          "L" // Header tag for logging messages
#define STARTTIME_HEADER    "S" // Header tag for start time message
#define MEASUREMENT_HEADER  "M" // Header tag for serial measurement message
#define CMD_HEADER          "C" // Header tag for serial command message
#define TEMPERATURE_HEADER  "T" // Header tag for temperature value
#define FORCE_BAR_HEADER    "F" // Header tag for bar force value
#define LIGHT_HEADER        "I" // Header tag for light intensity value
#define START_HEADER        "A" // Header tag for logging messages
#define STOP_HEADER         "P" // Header tag for logging messages
#define TIME_REQUEST         7         // ASCII bell character requests a time sync message 

volatile int flag = 0; // Controls transmission start
volatile int start = 0; // Gets transmission start
int start_millis = 0;
String start_txt = "";

// Reward variables
int pin = 2; // interrupt pin
volatile int reward = LOW;
Servo myservo;  // create servo object to control a servo 

// anolog storage
int tmpValue = 23.0; 
int barValue = 0.0; 
int ldrValue = 0; 
int cont = 0;
int send_freq = 100; // sending frequency is 100/send_freq (timer1)
String pkg = MEASUREMENT_HEADER;

void setup(){

//----------------------------------- INTERRUPTS SETUP -----------------------------------//

cli();//stop interrupts

  //set timer2 interrupt at 8kHz
  TCCR2A = 0;// set entire TCCR2A register to 0
  TCCR2B = 0;// same for TCCR2B
  TCNT2  = 0;//initialize counter value to 0
  // set compare match register for 8khz increments
  OCR2A = 77;// = (16*10^6) / (8000*8) - 1 (must be <256)
  // turn on CTC mode
  TCCR2A |= (1 << WGM21);
  // Set CS21 bit for 8 prescaler
  TCCR2B |= (1 << CS20) | (1 << CS21) | (1 << CS22);   
  // enable timer compare interrupt
  TIMSK2 |= (1 << OCIE2A);

  
  sei();//allow interrupts

//----------------------------------- SERIAL SETUP -----------------------------------//
// initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  while (!Serial) ; // Needed for Leonardo only
  pinMode(13, OUTPUT);
  //setSyncProvider(requestSync);  //set function to call when sync required
  Serial.println("Waiting for command message");
  flag = 0;
  start = 0;

  attachInterrupt(digitalPinToInterrupt(pin), toggle, RISING); // sets interrupt at pin 2 on rising, calls toggle function
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 

}//end setup

//----------------------------------- INTERRUPTS DECLARATION -----------------------------------//

ISR(TIMER2_COMPA_vect){//timer0 interrupt 100Hz reads analog sensor and sends at 10 Hz
//generates pulse wave of frequency 1Hz/2 = 0.5kHz (takes two cycles for full wave- toggle high then toggle low)
  if(flag) {
       
    cont++;
    
    //Sends the package with a return carriage character
    // This operation runs at a rate of 100/send_freq
    if (cont>=send_freq) {

//      if(!start) { // Runs once to get start time of the first measurement
//        start_millis = millis();
//        start = 1;
//        start_txt += STARTTIME_HEADER + String(start_millis); //sends start time in ms with "S"  first
//        Serial.println(start_txt);
//      }
//      
      // Reads sensor and assembles package to send (at a rate of 100 Hz)
      ldrValue = analogRead(A0); // reads LDR value
      
      pkg += String(millis()) + ",";        // adds time value
      pkg += TEMPERATURE_HEADER + String(tmpValue) + ",";  // adds temperature value
      pkg += FORCE_BAR_HEADER   + String(barValue) + ",";  // adds bar force value
      pkg += LIGHT_HEADER       + String(ldrValue);        // adds LDR value
      //pkg += String(sensorValue) + ";";
        
      //pkg = pkg.substring(0,pkg.length()-1); // remove last comma
      //pkg += "\\r";
      
      Serial.println(pkg);  //Sends data package via serial
      
      cont = 0; // reset variables
      pkg =  MEASUREMENT_HEADER; // resets with first character as the header
    }
  }
}

  

void loop()
{
  //Serial.println("1");
  if (!flag) {
    myservo.write(0); // sets servo to 0 position at the beginning
    delay(2000);  
    //flag = 1;
  }
  
  while (!Serial.available()) { // wait for data to arrive
    /*Serial.println("2");*/
      if(reward) { // polls reward for a change. If high, activates the motor
        giveReward();
      }
  } 

  //Serial.println("3");
  // serial read section
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {
    //Serial.println("4");
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      //Serial.println("5");
      processCommand(); // checks for any commands received
      //Serial.println("52");
    }

      if(reward) { // polls reward for a change. If high, activates the motor
        giveReward();
      }
  }

   //Serial.println("6");
}



int aquisitionStatus() {
  return flag;
}

void startAquisition() {
  if(!aquisitionStatus()) {
    Serial.println(String(LOG_HEADER) + "Aquisition has started");
    flag = 1;
  }
    
}

void stopAquisition() {
  if(aquisitionStatus()) {
    Serial.println(String(LOG_HEADER) + "Aquisition has stopped.");
    flag = 0;
  }
    
} 

void processCommand() { // Waits for command, which has to start with C
                        // 'C1' starts aquisition; 'C0' stops aquisition
  int cmd;
  
  if(Serial.find(CMD_HEADER)) {  
     cmd = Serial.parseInt();
     switch(cmd) {
      
      case 0:
       stopAquisition();
       break;
       
      case 1: 
       startAquisition(); // Sync Arduino clock to the time received on the serial port
       break;
      default:
        Serial.println("Command does not exist.");
     }     
  }
}

void toggle() {
  reward = HIGH;
}

void giveReward() {
    //state = !state;
    //digitalWrite(led, state);
    myservo.write(180);
    delay(2000);
    myservo.write(0);
    reward = LOW;
}
