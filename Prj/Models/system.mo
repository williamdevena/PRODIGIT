

model System

Gomp gomp;
Controller1 ctr1;
Controller2 ctr2;
Aula aula;
Student student;
Monitor1 monitor1;
Monitor2 monitor2;

equation

// STATO GOMP
connect(gomp.state, ctr1.gomp_state);
connect(ctr1.state, ctr2.ctr1_state);

// AGIBILITA'
connect(gomp.agibilita_aula, aula.state);
connect(gomp.agibilita, ctr1.gomp_agibilita);

// POSTI MAX
connect(gomp.max, ctr2.gomp_max);

// POSTI PRENOTATI
connect(ctr2.num_pre, aula.num_pre);

// INPUT STUDENTE
connect(ctr2.input_studente, student.x);

// CONTROLLER - AULA
connect(aula.u1_1, ctr1.u1_1);
connect(aula.u1_2, ctr1.u1_2);
//connect(aula.u2_1, ctr2.u2_1);
//connect(aula.u2_2, ctr2.u2_2);
connect(ctr2.prenotazione, aula.prenotazione);

// MONITOR
connect(gomp.max, monitor1.gomp_max);
connect(aula.num_pre, monitor1.num_pre);
connect(gomp.agibilita, monitor1.gomp_agibilita);
//connect(ctr2.u2_1, monitor1.u2_1);
//connect(ctr2.state, monitor1.gomp_state);
//connect(monitor.gomp_tempo_down, gomp.tempo_down);
//connect(monitor.ctr1_tempo_down, ctr1.tempo_down);

// MONITOR2 
connect(aula.tempo, monitor2.aula_tempo);



end System;
