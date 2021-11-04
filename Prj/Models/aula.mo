
class Aula

parameter Integer x0 = 0;     		    // PARTE DA ZERO PRENOTAZIONI
parameter Real T = 1.0;   

parameter Integer N = 2; 
parameter Integer x_0 = 1;  					// stato iniziale (AGIBILE)  
parameter Real samplePeriod = 1.0;
parameter Integer globalSeed = 29351;
parameter Integer localSeed = 18467;
Real r1024;

discrete Integer state1024[Modelica.Math.Random.Generators.Xorshift1024star.nState];


// Matrice di transizione degli stati dell' aula
parameter Real A[N, N] =
{
{0.99999, 0.00001},
{0.001, 0.999}
};


InputBoolean u1_1; 			  						// input Controller1 (Prodigit è up o down)
InputBoolean u1_2;			 							// input Controller1 (Aula è agibile o inagibile)

InputInteger prenotazione;          	// input di prenotazione, cancellazione o niente
OutputInteger num_pre;    						// Numero prenotazioni
OutputInteger state;           				// agibile o inagibile
OutputReal tempo;											// tempo in cui aula è agibile ma il controller ancor ablocca prenotazioni (serve per verificare req. non funz.)


initial equation
num_pre=x0;
state1024 = Modelica.Math.Random.Generators.Xorshift1024star.initialState(localSeed, globalSeed);
r1024     = 0;
state = x_0;
tempo=0;


equation

when sample(1,T) then

	(r1024,state1024) = Modelica.Math.Random.Generators.Xorshift1024star.random(pre(state1024));
        state = pick(r1024, pre(state), A);
        
        if (state==1 and u1_2==false) then
        	tempo=pre(tempo)+T;
        elseif (state==1) then
        	tempo=0;
        else
        	tempo=pre(tempo);
        end if;
        

	if (u1_1==false) then
		num_pre=pre(num_pre);
	elseif (u1_2==false) then            	// elseif perché se Prodigit è down non si può sapere se l' aula diventa inagibile
		num_pre=0;
	else
		num_pre=pre(num_pre)+prenotazione;
	end if;
		
end when;

end Aula;


function  pick
input Real z;   
input Integer x;  
input Real[:,:] A;   
output Integer w;  

protected
Integer i;
Real y;

algorithm


i := 1;
y := A[x, i];

while ((z > y) and (i < size(A, 1))) loop
  i := i + 1;
  y := y + A[x, i];
end while;

w := i;

end pick;




