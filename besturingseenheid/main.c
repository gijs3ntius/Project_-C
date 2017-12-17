#define F_CPU 16E6

#include <avr/io.h>
#include "sensorIO.h"
#include "serialConnection.h"
#include "nieuwe_distance.h"
#include "AVR_TTC_scheduler.h"
#include "pinIO.h"
#include <util/delay.h>
#include <avr/eeprom.h>

#define redLight 11
#define greenLight 12
#define yellowLight 13

uint8_t rolledOut = 0;

uint8_t licht;
uint8_t temp;
uint8_t dist;

void Light(){
	uint8_t command = 0b00010001;
	licht = getLight(2);
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(licht);
	_delay_ms(10);
}

void Temperature(){
	uint8_t command = 0b00010010;
	temp = getTemp(1);
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(temp);
	_delay_ms(10);

}

void Distance(){
	uint8_t command = 0b00110011;
	dist = calcDistance();
	transmitSerial(command);
	_delay_ms(50);
	transmitSerial(dist);
	_delay_ms(10);
}

void setUpLeds(){
	digital_config(redLight, OUT);
	digital_config(greenLight, OUT);
	digital_config(yellowLight, OUT);
}

void rolledInOrOut(uint8_t command, uint8_t maxOut){
	uint8_t i = 0;
	if (rolledOut == 0 && command == 2) {
		rolledOut = 1;
		digital_write(redLight, LOW);
		digital_write(greenLight, HIGH);
		digital_write(yellowLight, LOW);
		for (i = 0; i < 10; i++)
		{
			digital_write(yellowLight, HIGH);
			_delay_ms(500);
			digital_write(yellowLight, LOW);
			_delay_ms(500);
		}
		return;
	}	
	if (rolledOut == 1 && command == 1) {
		rolledOut = 0;
		digital_write(greenLight, LOW);
		digital_write(redLight, HIGH);
		digital_write(yellowLight, LOW);
		for (i = 0; i < 10; i++){
			digital_write(yellowLight, HIGH);
			_delay_ms(500);
			digital_write(yellowLight, LOW);
			_delay_ms(500);
		}
		return;
	}
	return;
}

void settingsChecker(){
	if (licht <= getMinLight()) {
		rolledInOrOut(1, getMaxRoll());
	}
	if (temp <= getMinTemp()) {
		rolledInOrOut(1, getMaxRoll());
	}
	if (licht >= getMaxLight()) {
		rolledInOrOut(2, getMaxRoll());
	}
	if (temp >= getMaxTemp()) {
		rolledInOrOut(2, getMaxRoll());
	}
	_delay_ms(200);
	
}

int main(void)
{
	initSerial();
	analog_config();
	setDefaultValues();
	setUpLeds();
	_delay_ms(1000);
	SCH_Init_T1();
	SCH_Add_Task(Temperature, 100, 400);
	SCH_Add_Task(Light, 200, 400);
	SCH_Add_Task(Distance, 60, 120);
	SCH_Add_Task(settingsChecker, 50, 100);
	//SCH_Add_Task(serialReactor, 10, 20);
	SCH_Start();// start de scheduler
    while (1)
    {
		SCH_Dispatch_Tasks(); // verzend de taken
	}
}
