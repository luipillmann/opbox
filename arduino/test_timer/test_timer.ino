#include <Servo.h> 

int cont = 0;
int flag = 0;
Servo myservo;

void setup() {
  // put your setup code here, to run once:
  cli();//stop interrupts

//set timer0 interrupt at 2kHz --> 100 Hz
  TCCR0A = 0;// set entire TCCR2A register to 0
  TCCR0B = 0;// same for TCCR2B
  TCNT0  = 0;//initialize counter value to 0
  // set compare match register for 2khz increments
  OCR0A = 77;// = (16*10^6) / (2000*64) - 1 (must be <256)
  // turn on CTC mode
  TCCR0A |= (1 << WGM01);
  // Set CS02 and CS00 bits for 1024 prescaler
  TCCR0B |= (1 << CS02) | (1 << CS00);   
  // enable timer compare interrupt
  TIMSK0 |= (1 << OCIE0A);

  sei();//allow interrupts

  Serial.begin(9600);
  flag=0;
}

ISR(TIMER0_COMPA_vect){//timer0 interrupt 2kHz toggles pin 8
//generates pulse wave of frequency 2kHz/2 = 1kHz (takes two cycles for full wave- toggle high then toggle low)
 if(flag) {
 
 cont++;
 if (cont>=1) {
    Serial.println("sad");
    cont=0; 
 }
 }
}



void loop() {
  // put your main code here, to run repeatedly:
Serial.println("1");
  
  while (!Serial.available()) {Serial.println("2");} // wait for data to arrive

  Serial.println("3");
  // serial read section
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {
    Serial.println("4");
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      Serial.println("peido"); // checks for any commands received
      Serial.println("5");
      flag = 1;
    }
  }

//  if(reward) { // polls reward for a change. If high, activates the motor
//      giveReward();
//  }

   Serial.println("6");
  
  
}
