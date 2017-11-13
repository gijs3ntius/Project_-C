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
#include "EEPROMconfig.h"
#include "pinIO.h"
#include "nieuwe_distance.h"
#include <util/delay.h>
#include <avr/eeprom.h>

uint8_t data1;
uint8_t data2;
uint8_t data3;

void Light(){

	uint8_t command = 0b00010001;

	uint8_t data1 = getLight(2);

	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(data1);
	_delay_ms(10);
}

void Temperature(){

	uint8_t command = 0b00010010;

	uint8_t data2 = getTemp(1);
	
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(data2);
	_delay_ms(10);

}


void Distance(){
	uint8_t command = 0b00110011;
	data3 = calcDistance();
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(data3);
	_delay_ms(20);
}

void turnOnLights2(){
	turnOnLights();

}


void testkutkloteding(){
	transmitSerial(1);
}



void settingsChecker(){
	// data1 is licht
	// data2 is temperatuur
	if (data1 <= getMinLight())
	{
		rolledInOrOut(1, getMaxRoll());
	}
	
	if (data2 <= getMinTemp())
	{
		rolledInOrOut(1, getMaxRoll());
	}
	
	if (data1 >= getMaxLight())
	{
		rolledInOrOut(2, getMaxRoll());
	}
	
	if (data2 >= getMaxTemp())
	{
		rolledInOrOut(2, getMaxRoll());
	}
	
}





int main(void)
{
	
	analog_config();
	
	//setUpLeds();
	_delay_ms(1000);
	
	//setDefaultValues();
	
	
	initSerial();
	
	SCH_Init_T1(); // stel de scheduler in
	
	//SCH_Add_Task(Temperature, 0, 200); // temp zit op A1.
	SCH_Add_Task(Light, 100, 200); // Voeg taken toe aan de scheduler Light zit op A0.
	//SCH_Add_Task(settingsChecker, 200, 200); // misschien om de minuut
	//SCH_Add_Task(serialReactor,0,1);
	
	//SCH_Add_Task(Distance, 0, 200);
	//SCH_Add_Task(testkutkloteding,100,200);
	
	
	SCH_Start();// start de scheduler 
	
	
    while (1)
    {
		SCH_Dispatch_Tasks(); // verzend de taken
		
		
	}

}
