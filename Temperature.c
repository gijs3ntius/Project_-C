/*
 * Sensorenlezen.c
 *
 * Onderstaande code zorgt ervoor dat de TMP36GT9Z Low Voltage temperature sensor uitgelezen kan worden.
 *
 * Deze sensor werkt met voltage om temperatuur te meten. 
 * Hoe meer voltage hoe hoger de temperatuur. Daarom moet je de voltage omzetten in temperatuur in Celsius.
 * En omdat de ADC een 10 bits getal binnen krijgt moet je dit eerst omzetten in voltage.
 *
 */ 


#include <avr/io.h> 
#include <stdlib.h> 
#include <avr/sfr_defs.h> 
#define F_CPU 16E6 
#include <util/delay.h> 


/* initialiseer de analog to digital converter */
void ADC_init(){
	// AREF = AVcc
	// De ADC heeft een 'reference' voltage nodig. Wij willen de Vcc gebruiken (5v)
	// ADMUX staat voor ADC multiplexer
	ADMUX = (1<<REFS0); // we zetten bit REFS0 op 1 (zie datasheet)
	
	// ADC Enable en een prescaler van 128
	// 16000000/128 = 125000
	// ADC control en status register A
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0); // enable ADC, zet ADC prescaler select bits
	
	/* bron code: http://maxembedded.com/2011/06/the-adc-of-the-avr/  */
}

/* lees de ADC uit. Verwacht als parameter het kanaal - dus A0-A5 */
uint16_t read_Analog(uint8_t adcPoort)
{
	// we 'masken' de input. De waarde die het kanaal doorgeeft blijft hetzelfde.
	adcPoort &= 0b00000101;  // een AND met 5 (want 6 inputs)
	// MUX 3:0 er zijn 4 bits. Dus 2^4 combinaties. Je hebt alleen de eerste 6 combi's nodig.
	ADMUX = (ADMUX & 0xF8)|adcPoort; // de laatste 3 bits worden op 0 gezet. Daarna wordt de juiste poort gepakt met een OR.
	
	// start single convertion
	// write ’1? to ADSC
	ADCSRA |= (1<<ADSC);
	
	// wait for conversion to complete
	// ADSC becomes ’0? again
	// till then, run loop continuously
	while(ADCSRA & (1<<ADSC));
	
	return (ADC);
	
	/* bron code: http://maxembedded.com/2011/06/the-adc-of-the-avr/  */
}






/* verander het 10 bits getal in het voltage */
float voltage(analog){
	float voltage = analog * 5.0 / 1024;
	// keer 5.0 omdat het om 5 volt gaat en gedeelt door 1024 omdat het een 10 bits getal is
	// voorbeeld: 2.5 volt = 512 * 5.0 / 1024. Je krijgt 512(0x200) binnen
	return voltage;
	
}


/* Deze functie zorgt ervoor dat de gemeten voltage omgezet wordt naar temperatuur */
float temperatureInC(voltage){
	float temperatureC = (voltage - 0.5) * 100;
	// de formule die ervoor zorgt dat het omgezet wordt.
	// voorbeeld: (1.2 - 0.5) * 100 = 70 graden Celsius.
	return temperatureC;
	
}


float measure_Temp(){
	float tempInC = temperatureInC(voltage(read_Analog(0))); // lees ADC uit (A0) en maak er volt van en dan Celsius
	return tempInC;

}


int getTemp() {  
	int temperature;
	temperature= measure_Temp(); // roep de functie aan die temperatuur uitleest
	return temperature;
}

