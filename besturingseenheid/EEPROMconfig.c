/*
* Hieronder staan de functies die ervoor zorgen dat de Ardiuno geconfiguurt wordt.
* Zo krijgt hij onder andere een ID opgeslagen.
* Ook maximal uitrol en inrol stand wordt opgeslagen en kan aangepast worden
* ID van de ardiuno wordt altijd op adres 0x00 opgeslagen
*
*/
#include <avr/eeprom.h>
#include <stdlib.h>

/* we gebruiken vaste adressen. Dan haal je altijd de goede van de juiste plek */
const ID_address = 0x00;
const maxRoll_address = 0x01;
const minRoll_address = 0x02;
const maxTemp_address = 0x03;
const minTemp_address = 0x04;
const maxLight_address = 0x05;
const minLight_address = 0x06;

void setArduinoID(uint8_t userinput){
	eeprom_read_byte(ID_address);
}

uint8_t getArduinoID(){
	uint8_t ardID = eeprom_read_byte(ID_address);
	return ardID;
}

void setMaxRoll(uint8_t userInput){
	eeprom_write_byte(maxRoll_address, userInput);
}

uint8_t getMaxRoll(){
	uint8_t maxRoll = eeprom_read_byte(maxRoll_address);
	return maxRoll;
}

void setMinRoll(uint8_t userInput){
	eeprom_write_byte(minRoll_address, userInput);
}

uint8_t getMinRoll(){
	uint8_t minRoll = eeprom_read_byte(minRoll_address);
	return minRoll;
}

void setMaxTemp(uint8_t userInput){
	eeprom_write_byte(maxTemp_address, userInput);
}

uint8_t getMaxTemp(){
	uint8_t maxTemp = eeprom_read_byte(maxTemp_address);
	return maxTemp;
}

void setMinTemp(uint8_t userInput){
	eeprom_write_byte(minTemp_address, userInput);
}

uint8_t getMinTemp(){
	uint8_t minTemp = eeprom_read_byte(minTemp_address);
	return minTemp;
}


void setMaxLight(uint8_t userInput){
	eeprom_write_byte(maxLight_address, userInput);
}

uint8_t getMaxLight(){
	uint8_t maxLight = eeprom_read_byte(maxLight_address);
	return maxLight;
}

void setMinLight(uint8_t userInput){
	eeprom_write_byte(minLight_address, userInput);
}

uint8_t getMinLight(){
	uint8_t minLight = eeprom_read_byte(minLight_address);
	return minLight;
}

void setDefaultValues(){
	setMaxRoll(200);
	setMinRoll(2);
	setMaxTemp(25);
	setMinTemp(10);
	setMaxLight(255);
	setMinLight(1);
}