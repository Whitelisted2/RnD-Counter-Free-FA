LoadPackage("automata");
LoadPackage("semigroup");

aut1 := Automaton("det",5,2,[[5,2,3,4,1],[2,3,4,2,2]],[1],[5]);

LogTo("output.txt");
Print(aut1);
ss1 := SyntacticSemigroupAut(aut1);
Print(ss1);
Print(IsAperiodicSemigroup(ss1));
