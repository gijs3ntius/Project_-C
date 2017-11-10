/*
 * CFile1.c
 *
 * Created: 10-10-2017 19:28:18
 *  Author: Gijs
 */ 

#include <avr/io.h>
#include <stdio.h>

#define HIGH 1
#define LOW 0
#define IN 0
#define OUT 1

/*
 * Sets a digital pin to get input or output
 */
void digital_config(int pin, int value) {
	if(pin < 8) {
		if(value == 0) {
			DDRD = DDRD & ~(1 << pin);
		} else {
			DDRD = DDRD | (1 << pin);
		}
		
	} else {
		if(value == 0) {
			DDRB = DDRB & ~(1 << (pin%8));
		} else {
			DDRB = DDRB | (1 << (pin%8));
		}
	}
	return;
}

/*
 * Sets a digital pin to 0 or 1
 */
void digital_write(int pin, int value) {
	if(pin < 8) {
		if(value == 0) {
			PORTD = PORTD & ~(1 << pin);
		} else {
			PORTD = PORTD | (1 << pin);
		}
		
	} else {
		if(value == 0) {
			PORTB = PORTB & ~(1 << (pin%8));
		} else {
			PORTB = PORTB | (1 << (pin%8));
		}
	}
	return;
}

/*
 * Gets a value from a digital pin 1 or 0
 */
int digital_read(int pin) {
	if (pin < 8)
	{
		return (PIND & (1 << (pin%8)));
	} else {
		return (PINB & (1 << (pin%8)));
	}
}

/*
 * Configures an ADC pin in this case pin 0
 */
void analog_config() {

	//AREF = AVcc
	// De ADC heeft een 'reference' voltage nodig. Wij willen de Vcc gebruiken (5v)
	// ADMUX staat voor ADC multiplexer
	ADMUX |= (1<<REFS0); // we zetten bit REFS0 op 1 (zie datasheet)
	//ADMUX |= (1 << ADLAR);
	
	// ADC Enable en een prescaler van 128
	// 16000000/128 = 125000
	// ADC control en status register A
	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2); // enable ADC, zet ADC prescaler select bits
	ADCSRA |= (1<<ADEN);
	
	/* bron code: http://maxembedded.com/2011/06/the-adc-of-the-avr/  */
}



uint16_t analog_read(uint8_t ) {
	
	ADCSRA |= (1<<ADEN);
	
	ADMUX |= (1<<REFS0);

	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2);
	
	ADMUX = (ADMUX & 0xF8) & ~(1 << MUX0);
	
	
	

	ADCSRA |= (1<<ADSC);
	

	loop_until_bit_is_set(ADCSRA,ADSC);
	ADCSRA &= ~(1<<ADEN);
	
	return (ADC);
	
}





/*
 * Gets a value from an analog pin
 * TODO before reading setup the ADMUX and ADCSRA registers
 */
uint16_t analog_read0() {
	
	ADCSRA |= (1<<ADEN);
	
	ADMUX |= (1<<REFS0); 

	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2); 
	
	ADMUX = (ADMUX & 0xF8) & ~(1 << MUX0);
	
	
	

	ADCSRA |= (1<<ADSC);
	

	loop_until_bit_is_set(ADCSRA,ADSC);
	ADCSRA &= ~(1<<ADEN);
	
	return (ADC);
	
}

uint16_t analog_read1() {
	
	ADCSRA |= (0<<ADEN);
	
	ADMUX |= (1<<REFS0);

	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2);
	
	ADMUX = (ADMUX & 0xF8)|(1 << MUX1);
	
	
	ADCSRA |= (1<<ADEN);

	ADCSRA |= (1<<ADSC);
	

	loop_until_bit_is_set(ADCSRA,ADSC);
	
	return (ADC);
	
}


	
	/*
	uint8_t low;
	
	//ADMUX = (ADMUX & 0xF0)|(adcPoort & 0x0F)// get the right channel
	
	ADMUX |= (1<<REFS0); // set reference voltage
	
	ADMUX = (ADMUX & 0xF0)|(adcPoort & 0x0F);// get the right channel
	
	
	ADCSRA |= (1<<ADEN); // turn on
	
	ADCSRA |= (1<<ADSC); // start conversion
	
	while(ADCSRA & (1<<ADSC)); // wait until input
	
	ADCSRA |= (0<<ADEN); // turn off
	
	low = ADCL; // put ADCL in low
	
	return (ADCH << 8) | low; // return value
	
}
	
	*/
	/*
	
	
	// we 'masken' de input. De waarde die het kanaal doorgeeft blijft hetzelfde.
	//adcPoort &= 0x0F;  // een AND met 15 (want 6 inputs)
	// MUX 3:0 er zijn 4 bits. Dus 2^4 combinaties. Je hebt alleen de eerste 6 combi's nodig.
	ADMUX = (ADMUX & 0xF0)|(adcPoort & 0x0F); // de laatste 3 bits worden op 0 gezet. Daarna wordt de juiste poort gepakt met een OR.
	
	// start single conversion
	// write ’1? to ADSC
	ADCSRA |= (1<<ADSC);
	
	
	// wait for conversion to complete
	// ADSC becomes ’0? again
	// till then, run loop continuously
	//while(ADCSRA & (1<<ADSC));
	loop_until_bit_is_set(ADCSRA,ADSC);
	
	return (ADC);

	*/
	/* bron code: http://maxembedded.com/2011/06/the-adc-of-the-avr/  */ 

