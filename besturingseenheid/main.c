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
	uint8_t command = 0b0001;
	uint8_t data1 = getLight();
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(data1);
	_delay_ms(10);
}

void Temperature(){
	uint8_t command = 0b0010;
	uint8_t data2 = getTemp();
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(data2);
	_delay_ms(10);

}


void Distance(){
	uint8_t command = 0b00110011;
	uint8_t data = getDistance();
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(data);
	_delay_ms(10);
}

void turnOnLights2(){
	turnOnLights();

}


int main(void)
{

	//analog_config();
	//setUpUltra(); // voor de afstand
	//setUpInterrupt(); // voor de afstand
	//setUpTimer0(); // voor de afstand
	//setUpLights();
	initSerial();
	SCH_Init_T1(); // stel de scheduler in
	SCH_Add_Task(Temperature, 0, 200); // temp zit op A0.
	SCH_Add_Task(Light, 100, 200); // Voeg taken toe aan de scheduler Light zit op A1.
	//SCH_Add_Task(Distance, 0, 60); // je wilt 60 ms wachten totdat je opnieuw meet. Dit staat in de datasheet
	//SCH_Add_Task(turnOnLights2, 0, 100);
	SCH_Start();// start de scheduler
    while (1)
    {
		SCH_Dispatch_Tasks(); // verzend de taken
		/*
		Distance();
		_delay_ms(60);
		transmitSerial(1);*/
	}

}
