/*
 * project_arduino.c
 *
 * Created: 29-10-2017 10:45:52
 * Author : Gijs
 */ 

#include <avr/io.h>
#include "sensorIO.h"
#include "serialConnection.h"


int main(void)
{
    /* Replace with your application code */
    while (1) 
    {
		transmitSerial(getDistance());
		_delay_ms(1000);
		transmitSerial(getLight());
		_delay_ms(1000);
		transmitSerial(getTemp());
		_delay_ms(1000);
    }
}

