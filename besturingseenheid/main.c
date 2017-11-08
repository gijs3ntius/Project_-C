/*
 * project_arduino.c
 * 19200 baudrate 
 *
 */ 

#define F_CPU 16E6

#include <avr/io.h>
#include "sensorIO.h"
#include "serialConnection.h"
#include "AVR_TTC_scheduler.h"
#include "pinIO.h"
#include <util/delay.h>
#include <avr/eeprom.h>



void Light(){
	transmitSerial(getLight());
	_delay_ms(10);
}

void Temperature(){
	transmitSerial(getTemp());
	
}

void Distance(){
	transmitSerial(getDistance());
}

void turnOnLights2(){
	turnOnLights();
	
}


int main(void)
{
	
	analog_config();
	
	//setUpInterrupt(); // voor de afstand

	//setUpUltra(); // voor de afstand
	
	//setUpTimer0(); // voor de afstand
	
	setUpLights();

	initSerial();
	
	SCH_Init_T1(); // stel de scheduler in

	//SCH_Add_Task(Light, 0, 200); // Voeg taken toe aan de scheduler Light zit op A1.
	// 200 = 30000 dus om de 30 seconden
	// om de 60 seconden deze waarden naar centrale sturen.
	
	//SCH_Add_Task(Temperature, 100, 200); // temp zit op A0.
	// 200 = 40000 dus om de 40 seconden
	
	//SCH_Add_Task(Distance, 0, 60); // je wilt 60 ms wachten totdat je opnieuw meet. Dit staat in de datasheet
	
	SCH_Add_Task(turnOnLights2, 0, 100);
	


	SCH_Start();// start de scheduler
   
    while (1) 
    {
		SCH_Dispatch_Tasks(); // verzend de taken
		
	}
	
} 


