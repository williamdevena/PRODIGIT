class Student

OutputInteger x;

parameter Real T = 1.0;
parameter Integer globalSeed = 98753;  
parameter Integer localSeed = 123991;  

Real r1024;
Integer state1024[Modelica.Math.Random.Generators.Xorshift1024star.nState];

parameter Real A[3] = {0.01, 0.97, 0.02};

initial equation
state1024 = Modelica.Math.Random.Generators.Xorshift1024star.initialState(localSeed, globalSeed);
r1024=0;
x=0;


equation
	
when sample(0,T) then
        (r1024,state1024) = Modelica.Math.Random.Generators.Xorshift1024star.random(pre(state1024));     

	if (r1024<=A[2]) then
		x=0;
	elseif (r1024<=A[2]+A[3]) then
		x=1;
	else
		x=-1;
	end if;
      
end when;



end Student;
