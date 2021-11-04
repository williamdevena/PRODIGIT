
class Monitor1     //MONITOR DEI REQUISITI FUNZIONALI

InputInteger gomp_max;
InputInteger gomp_agibilita;
InputInteger num_pre;

OutputBoolean y;

Boolean z;
Integer errore;

initial equation
y = false;

equation

// controlla se 
// 1. il numero delle prenotazioni supera i posti disponibili  (errore=-2)
// 2. il numero di prenotazioni scende sotto zero  (errore=-3)
// 3. viene fatta una prenotazione quando l' aula è inagibile (errore=-4)


z = (num_pre > gomp_max) or (num_pre < 0) or (gomp_agibilita==2 and (pre(num_pre)<num_pre));

// per debuggare
if (num_pre > gomp_max) then
	errore=-2;
elseif (num_pre < 0) then
	errore=-3;
elseif (gomp_agibilita==2 and (pre(num_pre)<num_pre)) then
	errore=-4;
else
	errore=-5;
end if;



algorithm

when edge(z) then
y := true;
end when;

end Monitor1;
