#include<stdio.h>
#include<iostream>
#include<cstdlib>
#include<vector>
#include<string>
#include<fstream>
#include<sstream>
#include<ostream>

using namespace std;

// struct automaton_str{ // oh this is probably not required unless coding from scratch
//     char type;                  // d, n, e
//     int num_states;             // |Q|
//     int num_alpha;              // |Sigma|
//     vector<int> init_states;    // Q_0
//     vector<int> final_states;   // F
//     vector<vector<vector<int>>> transition_table;
//     // ex.  (all this is in a vector)
//     //    alphabet|states->  1     2     3     4
//     //          a       <   <3>,  <>,   <3>,   <4>  >,
//     //          b       <   <3>,  <4>,  <>,    <4>  >
//     //
//     // 
// };

// struct automaton_str *create(char Type, int Num_states, int Num_alpha, vector<int> Init_states, vector<int> Final_states, vector<vector<vector<int>>> Transition_table){
//     struct automaton_str *mc = (struct automaton_str *)malloc(sizeof(automaton_str));
//     mc->type = Type;
//     mc->num_states = Num_states;
//     mc->num_alpha = Num_alpha;
//     mc->init_states = Init_states;
//     mc->final_states = Final_states;
//     mc->transition_table = Transition_table;
//     return mc;
// }

int main(int argc, char *argv[]){
    // // automata specs
    // automaton_type, num_states, num_alpha, init_states, final_states, transition_table 

    // FILE *fp;                          // to empty the output file
    // fp = fopen("output.txt", "w");
    // fclose(fp);
 
    if(argc>2)                         // argc contains argument count. Argument count should be 2 for execution to proceed in this case
    {                                  // the arguments are stored using pointer array *argv[] 
        printf("too many arguments. enter exactly one file name.");
        exit(1);
    }
    else if(argc<2)
    {
        printf("too few arguments. enter exactly one file name.");
        exit(2);
    }
    
    // read input file line-by-line
    // FILE *in;
    // in = fopen(argv[1], "r"); // file containing automaton information
    ifstream MyReadFile(argv[1]);

    // get type, num_st, num_alpha
    string type;
    getline(MyReadFile, type);
    int n_states, n_alpha;
    string ns, na;
    getline(MyReadFile, ns);
    getline(MyReadFile, na);
    n_states = stoi(ns);
    n_alpha = stoi(na);

    // one line for each letter in alphabet (assume a,b,c,... or a1,a2,a3,...)
    vector<vector<vector<int>>> full_table;
    vector<int> init_states;
    vector<int> fin_states;
    string init_states_str, fin_states_str;

    if(type == "DFA"){
        for(int i=0; i<n_alpha; i++){
            string tLine;
            getline(MyReadFile, tLine);

            // tLine looks like "6 2 3 4 5 1"
            istringstream ss(tLine);
            int num;
            vector<vector<int>> table_line;
            while(ss >> num){
                vector<int> table_ele;
                table_ele.push_back(num);
                // cout<<num;
                table_line.push_back(table_ele); // ex. <<6>, <2>> -> <<6>, <2>, <3>>
            }
            // cout<<endl;
            full_table.push_back(table_line); // push line to fulltable vector
        }

        

        // variables to consider: type, n_states, n_alpha, full_table, init_states, fin_states
        // time to format! (can do after nfa/enfa case)

    } else if(type == "NFA"){ // nfa, enfa cases
        for(int i=0; i<n_alpha; i++){
            string tLine;
            getline(MyReadFile, tLine);

            // tLine looks like "6,2 2,3 3 4 5 1" => want <<6,2>,<2,3>,<3>,<4>,<5>,<1>>
            istringstream ss(tLine);
            string token;
            vector<string> token_vec;
            vector<vector<int>> table_line;
            while(getline(ss, token, ' ')){
                istringstream subs(token);
                string token_smaller;
                vector<int> table_ele;
                while(getline(subs, token_smaller, ',')){
                    table_ele.push_back(stoi(token_smaller));
                }
                table_line.push_back(table_ele);
            }
            full_table.push_back(table_line); // push line to fulltable vector
        }

    } else if(type == "ENFA"){
        // // need to do
    }

    // read start and finish states
    getline(MyReadFile, init_states_str);
    getline(MyReadFile, fin_states_str);
    // init_states.push_back(stoi(init_states_str)); // only one init state in DFA

    istringstream is(init_states_str);
    int num;
    while(is >> num){
        init_states.push_back(num);
    }
    istringstream fs(fin_states_str);
    int num2;
    while(fs >> num2){
        fin_states.push_back(num2);
    }
    MyReadFile.close();
    

    // start constructing instruction
    string instructionRHS = "aut1 := Automaton(";
    if(type == "DFA"){
        instructionRHS.append("\"det\"");
        instructionRHS.append(",");
        instructionRHS.append(to_string(n_states));
        instructionRHS.append(",");
        instructionRHS.append(to_string(n_alpha));
        instructionRHS.append(",");
        // 0 means no transition
        
        string tempstr;
        instructionRHS.append("[");
        for (int i = 0; i < full_table.size(); i++){
            instructionRHS.append("[");
            for (int j = 0; j < full_table[i].size(); j++)
            {
                string temp = to_string(full_table[i][j][0]);
                instructionRHS.append(temp);//
                if(j == full_table[i].size()-1){
                    break;
                }
                instructionRHS.append(",");
            }
            instructionRHS.append("]");
            if(i == full_table.size() - 1){
                break;
            }
            instructionRHS.append(",");
        }
        instructionRHS.append("]");
        // instructionRHS.append(to_string(init_states[0]));

    } else if(type == "NFA"){
        instructionRHS.append("\"nondet\"");
        instructionRHS.append(",");
        instructionRHS.append(to_string(n_states));
        instructionRHS.append(",");
        instructionRHS.append(to_string(n_alpha));
        instructionRHS.append(",");
        // 0 means no transition
        
        string tempstr;
        instructionRHS.append("[");
        for (int i = 0; i < full_table.size(); i++){
            instructionRHS.append("[");
            for (int j = 0; j < full_table[i].size(); j++){
                instructionRHS.append("[");
                for(int k = 0; k < full_table[i][j].size(); k++){
                    string temp = to_string(full_table[i][j][k]);
                    instructionRHS.append(temp);
                    if(k == full_table[i][j].size()-1){
                        break;
                    }
                    instructionRHS.append(",");
                }
                instructionRHS.append("]");
                if(j == full_table[i].size()-1){
                    break;
                }
                instructionRHS.append(",");
            }
            instructionRHS.append("]");
            if(i == full_table.size() - 1){
                break;
            }
            instructionRHS.append(",");
        }
        instructionRHS.append("]");

    } else if(type == "ENFA"){
        // // need to do

    }

    instructionRHS.append(",[");
    for(int i = 0; i < init_states.size(); i++){
        instructionRHS.append(to_string(init_states[i]));
        if(i == init_states.size()-1){
            break;
        }
        instructionRHS.append(",");
    }
    instructionRHS.append("],[");
    
    for(int i = 0; i < fin_states.size(); i++){
        instructionRHS.append(to_string(fin_states[i]));
        if(i == fin_states.size()-1){
            break;
        }
        instructionRHS.append(",");
    }
    instructionRHS.append("]");
    
    instructionRHS.append(");");
    cout<<instructionRHS<<endl;

    ofstream OutputFile("sandbox/inputAutomaton.g");
    OutputFile.write(instructionRHS.c_str(), instructionRHS.length());


    OutputFile.close();
    // instructionRHS ready to use.
    // managing LHS/
}
