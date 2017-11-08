/*
 * Ultrasenoorsensor
 *
 * Onderstaande code zorgt ervoor dat de HC-SR04 sensor uitgelezen kan worden.
 *
 * De sensor zendt een geluid uit op 40 000 Hz. 
 * Dit reist door de lucht. Als er een object is stuit dit signaal weer terug naar de sensor. 
 * Door te kijken hoe lang de reis duurt en de snelheid van geluid kun je de afstand in centimeters berekenen.
 * Formule = afstand = tijd * 0.034 (snelheid geluid in ms) / 2
 * bron: http://howtomechatronics.com/tutorials/arduino/ultrasonic-sensor-hc-sr04/
 */ 

#include "pinIO.h"
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
//#inculde distance_sensor

#define redLight 11
#define greenLight 12
#define yellowLight 13

#define HIGH 1
#define LOW 0
#define IN 0
#define OUT 1


/* Temperatuursensor
* verander het 10 bits getal in het voltage 
***************************************************************************************************************/

/* Deze functie zorgt ervoor dat de gemeten voltage omgezet wordt naar temperatuur */
float temperatureInC(uint16_t analog){
	float volt = analog * 5.0 / 1024;
	// keer 5.0 omdat het om 5 volt gaat en gedeelt door 1024 omdat het een 10 bits getal is
	// voorbeeld: 2.5 volt = 512 * 5.0 / 1024. Je krijgt 512(0x200) binnen
	float temperatureC = (volt - 0.5) * 100;
	// de formule die ervoor zorgt dat het omgezet wordt.
	// voorbeeld: (1.2 - 0.5) * 100 = 70 graden Celsius.
	return temperatureC;
	
}


uint8_t getTemp(){
	uint8_t tempInC = temperatureInC(analog_read(0)); // lees ADC uit (A0) en maak er volt van en dan Celsius
	return tempInC;
}


/* Photocell sensor 
*********************************************************************************************************************/


uint8_t getLight(){
	uint8_t light = (analog_read(1)>>2); 
	// lees A1 uit, met een shift /4 
	// Je krijgt een 10 bits getal. We schuiven hem twee keer naar rechts zodat je 8 bits hebt.
	// Je verliest hier alleen de waarden 0-3 mee. Voor dit project niet erg.
	
	return light;
}

/* Uit en inrol lampjes
*******************************************************************************************************************/


void setUpLights(){
	digital_config(redLight, OUT);
	digital_config(greenLight, OUT);
	digital_config(yellowLight, OUT);
}


uint8_t rolledInOrOut(uint8_t command){
	uint8_t i = 0;
	
	if (command == 2)
	{
		digital_write(redLight, LOW);
		digital_write(greenLight, HIGH);
		digital_write(yellowLight, LOW);
		
		for (i = 0; i < 10; i++)
		{
			digital_write(yellowLight, HIGH);
			_delay_ms(5000);
			digital_write(yellowLight, LOW);
			_delay_ms(5000);
		}
	}
	
	if (command == 1)
	{
		digital_write(greenLight, LOW);
		digital_write(redLight, HIGH);
		digital_write(yellowLight, LOW);
		
		for (i = 0; i < 10; i++){
			digital_write(yellowLight, HIGH);
			_delay_ms(5000);
			digital_write(yellowLight, LOW);
			_delay_ms(5000);	
		}
	}
}

/*Deze functie is er puur voor een simulatie. Om te testen */
void turnOnLights(){
	
	rolledInOrOut(1);
	_delay_ms(10000);
	rolledInOrOut(2);
	
}



void resetLights(){
	digital_write(redLight, LOW);
	digital_write(greenLight, LOW);
	digital_write(yellowLight, LOW);
}

