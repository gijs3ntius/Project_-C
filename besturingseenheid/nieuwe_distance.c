
#include <avr/io.h>
#include <util/delay.h>
#include "serialConnection.h"

#define F_CPU 16E6			     // 16.0 Mhz clock

#define HIGH 0x1
#define LOW 0x0
#define IN 0
#define OUT 1

// Delay between measures (on msec) , may occur problem if delay is short.Check datasheet

#define trigPin 8
#define echoPin 9

uint8_t pulsie = 0;

uint8_t calcDistance()
{
		
		digital_write(echoPin, LOW);
		digital_write(trigPin, HIGH);
	
		int counter = 0;
	
		digital_write(trigPin, LOW); // zorg ervoor dat trigger leeg is!
		_delay_us(2);
		digital_write(trigPin, HIGH);
		
		_delay_us(10);
		digital_write(trigPin, LOW);

		//
		while(!digital_read(echoPin)){}
		
		//
		while(digital_read(echoPin)){
			counter += 1;
		}
		
		// Bereken de afstand
		pulsie = (counter >> 2)/ 5.7; // dit hebben we gekalibreerd.
		// Bereken de afstand
		
		return pulsie;
	
}
