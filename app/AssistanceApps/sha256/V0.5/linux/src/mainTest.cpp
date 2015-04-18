/**
 * Slight modification of the original main file
 * This program will open the parameter-1 file and SHA256 it the parameter-2 number of times
 *
 */
#include <iostream>

#include <string>
#include <fstream>
#include <streambuf>
#include <stdlib.h>
#include <string.h>

#include "sha256.h"

using std::string;
using std::cout;
using std::endl; 
using std::ifstream;
using std::istreambuf_iterator;

int main(int argc, char *argv[]) {
	int verbose = 0;
	int report = 100000;
	if ((argc > 3) && (strcmp(argv[3], "-verbose") == 0)) {verbose = 1;}
	if ((argc > 4)) {report = atoi(argv[4]);}

	if(verbose == 1) {cout << "Calculating the SHA256 of file " << argv[1] << ", " << argv[2] << " times.\n";}
	ifstream t(argv[1]);
	string str;

	t.seekg(0, std::ios::end);   
	str.reserve(t.tellg());
	t.seekg(0, std::ios::beg);

	str.assign((istreambuf_iterator<char>(t)),
    istreambuf_iterator<char>());

    string input = str;
    string output0 = sha256(input);
	string outputNow;

	int current, total;
	total = atoi(argv[2]);
	for (current = 0; current < total; current++){
		outputNow = sha256(input);
		if (output0.compare(outputNow)!=0){
			cout << "ERROR! STRINGS DO NOT MATCH!\n";
			break;
		}
		if ((verbose == 1) && (current % report == 0)) {cout << "Calculated " << current << " out of " << total << "\n"; }
	}
 
    //cout << "sha256('"<< input << "'): " << output1 << "\n\n";

	if (verbose == 1) {cout << "ALL CALCULATIONS SUCCESSFULLY DONE!\n";}

	return 0;
}
