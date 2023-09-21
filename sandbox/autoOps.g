
Print(aut1);
aut2 := MinimalAutomaton(aut1);
Print("\nMinimal Automaton: ");
Print(aut2);

Print("\nTransition Semigroup: ");
ss2 := TransitionSemigroup(aut1);
ss3 := SemigroupByGenerators(ss2);
Print(ss3); 
gen := GeneratorsOfSemigroup(ss3);
Print("\nGenerators:");
Print(gen);

Print("\nSyntactic Semigroup: ");
ss1 := SyntacticSemigroupAut(aut1);
Print(ss1);

Print("\n Is it aperiodic? ");
Print(IsAperiodicSemigroup(ss3));
Print("\n");

Print("\n Monoid: ");
mon := MonoidByGenerators(gen);
Print(mon);
Print("\n");

Print("\nMultiplication Table: \n");
mult := MultiplicationTable(mon);
Print(mult);
Print("\n");

Print("\nSubgroup: \n");
# subgp := IsMonoid(mon);
subgp := Subsemigroup(mon, [Transformation([2,3,3])] );
Print(subgp);
Print("\n");



#     l   p  p2 p3  s
# [  [ 1, 2, 3, 4, 5 ], 
# p  [ 2, 3, 4, 2, 2 ], 
# p2 [ 3, 4, 2, 3, 3 ], 
# p3 [ 4, 2, 3, 4, 4 ],
# s  [ 5, 2, 3, 4, 1 ] ] 
