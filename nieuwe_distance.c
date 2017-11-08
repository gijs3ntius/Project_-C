

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define F_CPU 16E6			     // 16.0 Mhz clock

#define HIGH 0x1
#define LOW 0x0


#define Delay_Until_New_Measure 60		// Delay between measures (on msec) , may occur problem if delay is short.Check datasheet

volatile char Ultra_is_on = 0;
volatile char is_measuring = 0;
volatile uint32_t Timer0_counter = 0 ;
volatile uint16_t distance;

volatile long echo_start = 0;
volatile long echo_duration = 0;


#define trigPin 0
#define echoPin 3


/* Ultrasenoorsensor
*********************************************************************************************************************/

void setUpUltra(){
	digital_config(trigPin, OUT); // trigger pin wordt output
	digital_config(echoPin, IN); // echo pin is input
}

void setUpInterrupt(){
	PORTD |= (1<<echoPin);		// Enable PD2 pull-up resistor. // digital_write(echoPin, 1)
	
	EIMSK  |= (1<<INT1);			// Enable INT1 interrupts.
	
	EICRA |= (1<<ISC11) ;		// The rising edge of INT1 generates an interrupt request.
	// dit betekent: als er iets binnenkomt op de echopin wordt er een interrupt gegeven.
}

void setUpTimer0(){
	
    TCCR1A = 0;
	TCCR0B |= (1<<CS00);						   // NO prescaller , every tick is 1us  - START
	TCNT0 = 0;								   // Clear counter
	TIMSK0 |= (1<<TOIE0);					   // Enable Timer0-Overflow interrupts
	sei();										// Global interrupts Enabled.
}

void startPulse(){
	digital_write(trigPin, LOW); // zorg ervoor dat trigger leeg is!
	_delay_ms(2);
	
	digital_write(trigPin, HIGH);
	
	_delay_us(10);
	digital_write(trigPin, LOW);
	
}


	/* dit is een soort van de main functie. Hierdoor krijg je de juiste afstand terug. Dit in scheduler gooien */
	
uint8_t getDistance(){
		if (is_measuring == 0)
		{
			startPulse();
			calcDistance(echo_duration);
	
		}

		return distance;	
}
	
	
/
ISR(TIMER0_OVF_vect)  // Here every time Timer0 Overflow
{
	
	
	

} 


uint16_t calcDistance(uint16_t counter){
	
	distance = counter * 0.034 / 2;
	return distance;
	
}



ISR(INT1_vect)
{
	
	if (echo_start = 0)
	{
		TCNT0 = 0; // clear counter
		echo_start = 1;
	}
	if (echo_start = 1)
	{
		echo_duration += TCNT0; // sla de counter op
	}
	
	//echo_start = 1;
	//echo_duration = TCNT0; // sla de counter op
	//TCNT0 = 0; // clear counter

}

