/*
* Hieronder staan de functies die ervoor zorgen dat de Ardiuno geconfiguurt wordt.
* Zo krijgt hij onder andere een ID opgeslagen.
* Ook maximal uitrol en inrol stand wordt opgeslagen en kan aangepast worden
* ID van de ardiuno wordt altijd op adres 0x00 opgeslagen
*
*/



#include <avr/eeprom.h>
#include <stdlib.h>

const ID_address = 0x00;
const maxRoll_address = 0x01;
const minRoll_address = 0x02;


#define max_rollout;
#define min_rollout;
// weet niet zo goed waarom ik dit doe :p


/* Deze functie is zo geschreven dat er maar 1 keer een ID gegeven kan worden aan een Arduino. */

uint8_t giveID(){
	// Is er nog geen ID gegeven?
	if (eeprom_read_byte(ID_address) == '')
	{
		uint8_t randVal = 1000; // Ik wil dat elke ardiuno een vier cijfer ID krijgt
		randVal += rand() % 9000; // een willekeurig getal tussen 0 en 8999
		
		eeprom_write_byte(ID_address,randVal);
		return 1;
	} 
	// Is er al wel een ID gegeven:
	else
	{
		return 0;
	}
	
}

uint8_t getArduinoID(){
	uint8_t ardID = eeprom_read_byte(ID_address);
	return ardID;
}


uint8_t setMaxRoll(uint8_t userInput){
	eeprom_write_byte(maxRoll_address, userInput);
	
}






