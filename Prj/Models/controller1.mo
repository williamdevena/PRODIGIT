
block Controller1

parameter Real T = 1;

InputInteger gomp_state;		// stato del gomp (1 UP, 2 DOWN)
InputInteger gomp_agibilita; 		// agibilità (1 AGIBILE, 2 INAGIBILE)			
OutputBoolean u1_1; 			// se Prodigit è Down
OutputBoolean u1_2; 			// se l' aula è inagibile
OutputInteger state;
OutputReal tempo_down;	

initial equation
u1_1=true;
u1_2=true;
tempo_down=0;

equation

when sample(0,T) then

	
	state=gomp_state;
	
	if (state==2) then
		u1_1=false;
		tempo_down=pre(tempo_down)+T;
	else
		tempo_down=pre(tempo_down);
		u1_1=true;
	end if;	
	
	if (gomp_agibilita==2) then
		u1_2=false;
	else
		u1_2=true;
	end if;
	
end when;

	


end Controller1;

