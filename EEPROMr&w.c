/* EEPROM read en write 
*
* Bron code : http://www.scienceprog.com/atmega-eeprom-memory-writing/
*
*
*
*
*/

#include <EEPROM.h>



void EEPROM_write(unsigned int dataAddress, unsigned char Data)

{
	
	/* Eerst wachten we totdat de vorige schrijf cyclus gedaan is. 
	* EECR staat voor EEPROM control register
	* EEWE EEPROM write enable. Die zetten we op 1. Als control register ook 1 is geworden (dit navragen)
*/
	
	while(EECR & (1<<EEWE));
	
	/* We zorgen ervoor dat het adres wordt gezet en de data. 
	* EEPROM Adress register
	* EEPROM Data register
	*/
	
	EEAR = dataAddress;
	
	EEDR = Data;
	
	/* Nu zetten we de EEPROM Master Write Enable op 1! */
	
	EECR |= (1<<EEMWE);
	
	/* Nu starten we het schrijven naar de EEPROM. Als je ervoor zorgt dat EEWE binnen 4 cycles op 1 staat,
	* wordt er geschreven.
	*/
	
	EECR |= (1<<eewe);
	
}


unsigned char EEPROM_read(unsigned int dataAddress)

{
	
	/* Eerst wachten we eerst weer totdat de schrijf cyclus klaar is */
	
	while(EECR & (1<<eewe));
	
	/* Vanaf welk adres wil je de data hebben? Zet die waarde in het Adress register */
	
	EEAR = dataAddress;
	
	/* We zetten de EEPROM Read Enable op 1. In het control register*/
	
	EECR |= (1<<eere);
	
	/* Geef de data die in het dataregister terecht komt terug*/
	
	return EEDR;
	
}


