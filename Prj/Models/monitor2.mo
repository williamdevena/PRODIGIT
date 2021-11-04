class Monitor2   // MONITOR DEL REQUISITO NON FUNZIONALE

InputReal aula_tempo;

OutputBoolean y;

Boolean z;

initial equation
y = false;

equation

// controlla se 
// l' intervallo di tempo tra quando l' aula torna agibile e quando il controller1 riapre le prenotazioni è maggiore di un ' ora 

z = aula_tempo>60;


algorithm

when edge(z) then
y := true;
end when;

end Monitor2;
