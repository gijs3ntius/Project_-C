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
/* Struct that defines an arduino interface                             */
/************************************************************************/

//struct arduino
//{
//	int ID;
//} besturings_eenheid;

/************************************************************************/
/* Functions to set and get a connection                                */
/************************************************************************/

// Function to check if a given number is valid as an ID
//int isValidID(int number) {
	// TODO what else need to be checked
//	if (number <= 0) // number needs to be bigger then 0
//	{
//		return 0;
//	}
//	return 1; // number is valid
//}

// Connect function sets ID of an arduino interface
// Needs to pass an pointer to an ID of an arduino interface and an number to set the id
// Pointer is used, because this function is called within an arduino interface
//int connect(int ID* ,int number) {
//	if (ID != NULL && isValidID(number)) // check if the number is valid and the ID is not null
//	{
//		*ID = number;
//		return 1;
//	} else {
//		return 0;
//	}
//}

//int getConnected(int ID*) {
//
//}

/************************************************************************/
/* Functions to get data from the arduino                               */
/************************************************************************/

// Get data from arduino
//int getData() {

//}

// sent data from arduino via serial
//int sentData() {

//}

/************************************************************************/
/* Functions for the commands and the handling of the commands          */
/************************************************************************/



/************************************************************************/
/* Functions to read data from the serial connection                    */
/************************************************************************/

void initSerial() {
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable receiver en transmitter
	UCSR0B = (1<<TXEN0) | (1<<RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

uint8_t receiveSerial() {
	// wait for data to be received

	while ( !(UCSR0A & (1 << RXC0)) );
	// get and return received data from buffer
	return UDR0;
}

void transmitSerial(uint8_t data) {
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

void serialReactor(){
	uint8_t command;
	uint8_t  data;

	command = receiveSerial();
	data = receiveSerial();

	command &= 0b00001111;

	if(command <= 8 && command != 0){

		if (command == 0){
			setArduinoID(data);
		}

		if (command == 1){
			rolledInOrOut(command, getMaxRoll());
			_delay_ms(1000);
		}

		if (command == 2){
			rolledInOrOut(command, getMinRoll());
			_delay_ms(1000);
		}

		if (command == 3){
			setMaxRoll(data);
		}

		if (command == 4){
			setMinRoll(data);
		}

		if (command == 5){
			setMinTemp(data);
		}

		if (command == 6){
			setMaxTemp(data);
		}

		if (command == 7){
			setMinLight(data);
		}

		if (command == 8){
			setMaxLight(data);
		}
	}

	_delay_ms(20);


}
