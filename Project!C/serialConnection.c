/*
 * SerialConnectionLib.c
 *
 * Created: 27-10-2017 14:10:58
 * Author : Gijs
 */ 

#include <avr/io.h>

/************************************************************************/
/* Struct that defines an arduino interface (maybe not even necessary)                                                                    */
/************************************************************************/

struct arduino  
{
	int ID;
} besturings_eenheid;

/************************************************************************/
/* Functions to set and get a connection                                */
/************************************************************************/

// Function to check if a given number is valid as an ID
int isValidID(int number) {
	// TODO what else need to be checked
	if (number <= 0) // number needs to be bigger then 0
	{
		return 0;
	}
	return 1; // number is valid
}

// Connect function sets ID of an arduino interface
// Needs to pass an pointer to an ID of an arduino interface and an number to set the id
// Pointer is used, because this function is called within an arduino interface
int connect(int ID* ,int number) {
	if (ID != NULL && isValidID(number)) // check if the number is valid and the ID is not null
	{
		*ID = number;
		return 1;
	} else {
		return 0;
	}
}

int getConnected(int ID*) {
	
}

/************************************************************************/
/* Functions to get data from the arduino                               */
/************************************************************************/

// Get data from arduino
int getData() {
	
}

// sent data from arduino via serial
int sentData() {
	
}

/************************************************************************/
/* Functions for the commands and the handling of the commands          */
/************************************************************************/

int command() {
	
}

/************************************************************************/
/* Functions to get data from sensors                                   */
/************************************************************************/

int readSensor() {
	
}