block Controller2

parameter Real T = 0.5;

InputInteger ctr1_state;			// stato del gomp (1 UP, 2 DOWN)
InputInteger gomp_max;    			// posti massimi
InputInteger num_pre;				// Numero prenotazioni	
InputInteger input_studente;		// input dello studente (prenotazione (+1), niente (0), cancellazione (-1)
OutputInteger prenotazione;	
OutputInteger state;
				
Boolean u2_1;  			// se permettere prenotazioni
Boolean u2_2;			// se permettere cancellazioni



initial equation
u2_1=true;
u2_2=false;

equation

when sample(0,T) then

	state=ctr1_state;
	
	u2_1 = ((delay(num_pre,0.1) < gomp_max) and (state==1));
	u2_2 = ((delay(num_pre,0.1) > 0) and (state==1));
	
	if (u2_1==true and u2_2==true) then
		prenotazione=input_studente;
	elseif (u2_1==true) then
		if (input_studente>=0) then
			prenotazione=input_studente;
		else
			prenotazione=0;
		end if;
	elseif (u2_2==true) then
		if (input_studente<0) then
			prenotazione=input_studente;
		else
			prenotazione=0;
		end if;
	else
		prenotazione=0;
	end if;
	
end when;

	


end Controller2;
