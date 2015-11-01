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

#define TIME_HEADER  "T"   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 

int flag = 0; // Controls transmission start

// anolog storage
int sensorValue = 0; 
int cont = 0;
int send_freq = 5; // sending frequency is 100/send_freq (timer1)
String pkg = "";

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
  setSyncProvider(requestSync);  //set function to call when sync required
  Serial.println("Waiting for sync message");
  flag = 0;

}//end setup
  

//----------------------------------- INTERRUPTS DECLARATION -----------------------------------//

ISR(TIMER1_COMPA_vect){//timer1 interrupt 100Hz reads analog sensor and sends at 10 Hz
//generates pulse wave of frequency 1Hz/2 = 0.5kHz (takes two cycles for full wave- toggle high then toggle low)
  if(flag) {

    cont++;
     
    // Reads sensor and assembles package to send (at a rate of 100 Hz)
    sensorValue = analogRead(A0);
    //time_t t = now(); // Store the current time in time variable t
    pkg += String(now()) + "," + String(sensorValue) + ";";
    //pkg += String(sensorValue) + ";";
    
    //Sends the package with a return carriage character
    // This operation runs at a rate of 100/send_freq
    if (cont>=send_freq) {
      
      pkg = pkg.substring(0,pkg.length()-1); // remove last comma
      pkg += "\\r";
      
      Serial.println(pkg);  //Sends data package via serial
      
      cont = 0; // reset variables
      pkg =  "";
    }
  }
}

  

void loop(){    
  
  if (Serial.available()) {
    processSyncMessage();
  }
  if (timeStatus()!= timeNotSet) {
    //digitalClockDisplay();
    flag = 1; 
  }
  if (timeStatus() == timeSet) {
    digitalWrite(13, HIGH); // LED on if synced
  } else {
    digitalWrite(13, LOW);  // LED off if needs refresh
  }
  //delay(1000);
}

void digitalClockDisplay(){
  // digital clock display of the time
  Serial.print(hour());
  printDigits(minute());
  printDigits(second());
  Serial.print(" ");
  Serial.print(day());
  Serial.print(" ");
  Serial.print(month());
  Serial.print(" ");
  Serial.print(year()); 
  Serial.println(); 
}

void printDigits(int digits){
  // utility function for digital clock display: prints preceding colon and leading 0
  Serial.print(":");
  if(digits < 10)
    Serial.print('0');
  Serial.print(digits);
}


void processSyncMessage() {
  unsigned long pctime;
  const unsigned long DEFAULT_TIME = 1357041600; // Jan 1 2013

  if(Serial.find(TIME_HEADER)) {  
     pctime = Serial.parseInt();
     if( pctime >= DEFAULT_TIME) { // check the integer is a valid time (greater than Jan 1 2013)
       setTime(pctime); // Sync Arduino clock to the time received on the serial port
     }
  }
}

time_t requestSync()
{
  Serial.write(TIME_REQUEST);  
  return 0; // the time will be sent later in response to serial mesg
}

