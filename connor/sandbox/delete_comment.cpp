#include <stdio.h>
#include <fstream> 
#include <iostream>
#include <string>
#include <cstdlib>
//Ece 402
using namespace std;


int main(int argc, char ** argv) {
  if (argc != 2) {
    cout << "Please specify input file." << endl;
    exit(1);
  }

	ifstream file;
	//open code file
	file.open(argv[1]);


	if(!file) {
		cout << "cant open file";
    exit(1);
	}

	char a1,a2,b;
	b = '\0';
	while (file.get(a1)) {
		if (a1 == '#') {
			file.get(a2);
			if (a2 == '\n') {
				break;
			}
		}
		else if (a1 == '/') {
			file.get(a2);
			if (a2 == '/') {
				while (file.get(a1)) {
					if (a1 == '\n') {
						break;
					}
				}
			}
			else if (a2 == '*') {
				while (file.get(a1)) {
					if (a1 == '/'&& b == '*') {
						break;
					}
					b = a1;
				}
			}
		}

		else
			cout << a1;
	}
	file.close();

	return 0;
}
