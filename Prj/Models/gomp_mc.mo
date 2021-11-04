
class Gomp


parameter Integer N = 2; 
parameter Integer x_0 = 1;  // stato iniziale (UP)

// Matrice di transizione degli stati del Gomp
parameter Real A[N, N] =
{
{0.99995, 0.00005},
{0.001, 0.999}
};

InputInteger agibilita_aula;
OutputInteger max = 60;					// posti massimi
OutputInteger agibilita = agibilita_aula;		// agibilità (1 AGIBILE, 2 INAGIBILE)
OutputInteger state;					// stato Gomp (1 UP, 2 DOWN)
OutputReal tempo_down;				
Integer size = N;


parameter Real samplePeriod = 1.0;
parameter Integer globalSeed = 165796;
parameter Integer localSeed = 31358;
Real r1024;

protected
      discrete Integer state1024[Modelica.Math.Random.Generators.Xorshift1024star.nState];

algorithm
      when initial() then

        state1024 := Modelica.Math.Random.Generators.Xorshift1024star.initialState(localSeed, globalSeed);
        r1024     := 0;
	state := x_0;
	tempo_down:=0;
	
      elsewhen sample(0,samplePeriod) then
       (r1024,state1024) := Modelica.Math.Random.Generators.Xorshift1024star.random(pre(state1024));
       state := pick(r1024, pre(state), A);
       
       if (state==2) then
           tempo_down:=pre(tempo_down)+samplePeriod;
       else
       	   tempo_down:=pre(tempo_down);
       end if;
       	
       
      end when;


end Gomp;



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


