#include <Time.h>

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

#define LOG_HEADER  "L"         // Header tag for logging messages
#define STARTTIME_HEADER  "S"   // Header tag for start time message
#define MEASUREMENT_HEADER  "M" // Header tag for serial measurement message
#define CMD_HEADER  "C"         // Header tag for serial command message
#define TIME_HEADER  "T"        // Header tag for serial time sync message
#define TIME_REQUEST  7         // ASCII bell character requests a time sync message 

int flag = 0; // Controls transmission start
int start = 0; // Gets transmission start
int start_millis = 0;
String start_txt = "";


// anolog storage
int sensorValue = 0; 
int cont = 0;
int send_freq = 100; // sending frequency is 100/send_freq (timer1)
String pkg = MEASUREMENT_HEADER;

void setup(){

//----------------------------------- INTERRUPTS SETUP -----------------------------------//

cli();//stop interrupts

//set timer1 interrupt at 100Hz -- (Alterado para 100 Hz)
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 624;// = (16*10^6) / (100*256) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 bit for 256 prescaler
  TCCR1B |= (1 << CS12);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  
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

}//end setup
  

//----------------------------------- INTERRUPTS DECLARATION -----------------------------------//

ISR(TIMER1_COMPA_vect){//timer1 interrupt 100Hz reads analog sensor and sends at 10 Hz
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
      sensorValue = analogRead(A0);
      
      pkg += String(millis()) + "," + String(sensorValue) + ";";
      //pkg += String(sensorValue) + ";";
        
      pkg = pkg.substring(0,pkg.length()-1); // remove last comma
      //pkg += "\\r";
      
      Serial.println(pkg);  //Sends data package via serial
      
      cont = 0; // reset variables
      pkg =  MEASUREMENT_HEADER; // resets with first character as the header
    }
  }
}

  

void loop()
{
  while (!Serial.available()) {} // wait for data to arrive
  
  // serial read section
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      processCommand(); // checks for any commands received
    }
  }
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

//time_t requestSync()
//{
//  Serial.write(TIME_REQUEST);  
//  return 0; // the time will be sent later in response to serial mesg
//}

