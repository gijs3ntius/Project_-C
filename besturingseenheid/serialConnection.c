/*
 * SerialConnectionLib.c
 *
 * Created: 27-10-2017 14:10:58
 * Author : Gijs
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <util/delay.h>
#include <avr/sfr_defs.h>
#include "EEPROMconfig.h"
#include "sensorIO.h"
#define UBBRVAL 51
#define F_CPU 16E6

/************************************************************************/
/* Functions for the commands and the handling of the commands          */
/************************************************************************/

void serialReactor(){
	uint8_t command = receiveSerial() & 0b00001111;
	uint8_t  data = receiveSerial();
	if(command <= 8 && command != 0){
		if (command == 0) {
			setArduinoID(data);
		}
		if (command == 1) {
			rolledInOrOut(command, getMaxRoll());
			_delay_ms(1000);
		}
		if (command == 2) {
			rolledInOrOut(command, getMinRoll());
			_delay_ms(1000);
		}
		if (command == 3) {
			setMaxRoll(data);
		}
		if (command == 4) {
			setMinRoll(data);
		}
		if (command == 5) {
			setMinTemp(data);
		}
		if (command == 6) {
			setMaxTemp(data);
		}
		if (command == 7) {
			setMinLight(data);
		}
		if (command == 8) {
			setMaxLight(data);
		}
	}
	_delay_ms(20);
}

/************************************************************************/
/* Functions to read data from the serial connection                    */
/************************************************************************/

void initSerial() {
	UBRR0H = 0; // set the baud rate
	UBRR0L = UBBRVAL;
	UCSR0A = 0; // disable U2X mode
	UCSR0B = (1<<TXEN0) | (1<<RXEN0); // enable receiver en transmitter
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00); // set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
}

int receiveSerial() {
	while ( !(UCSR0A & (1 << RXC0)) ); // wait for data to be received
	return UDR0; // get and return received data from buffer
}

void transmitSerial(uint8_t data) {
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	UDR0 = data; // send the data
}