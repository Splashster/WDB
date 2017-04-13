#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdlib.h>

using namespace std;

struct Records {
	string server;
	string date;
	string time;
	string file_request;
	int size;
	int uv_score;
};

Records *record;

int getLineCount (string filename){
	string line;
	string token;
	ifstream file;
	file.open(filename.c_str());
	int line_count = 0;

	while(getline(file,line)){
		stringstream ss(line);
		getline(ss, token, ' ');
		if(token == "clark" || token == "epa"){
			line_count++;
		}
	}
	return line_count;
	file.close();
}

void storeRecords(string filename) {
	string line;
	string token;
	ifstream file;
	file.open(filename.c_str());
	int i = 0;
	int num = 0;
	string tokens[5];
	
	while(getline(file,line)){
		stringstream ss(line);
		getline(ss, token, ' ');
		if(token == "clark" || token == "epa"){
			tokens[i] = token;
			i++;
			while(getline(ss, token, ' ')){
				tokens[i] = token;
				i++;
			}
			i = 0;
			record[num].server = tokens[0];
			record[num].date = tokens[1];
			record[num].time = tokens[2];
			record[num].file_request = tokens[3];
			record[num].size = atoi(tokens[4].c_str());
			num++;
			
		}
	
	}
	file.close();
//	cout << tokens[0] << " " << record[0].server << endl;
	cout << "Record 4 size: " << record[3].size << endl;
	cout << "Record 5 file requested: " << record[4].file_request << endl;
}

//void generateUVScores(){
//	for(int i = 0; i < ]
//}

int main(int argc, char *argv[]){
	int epa_bw;
	int epa_cd;
	int clark_bw;
	int clark_cd;
	int wb;
	int wf;
	int cache_size;
	string filename;
	int num_lines = 0;
	
	filename = argv[1];

	num_lines = getLineCount(filename);

	record = new Records[num_lines];
	//epa_bw = strtol(argv[2], NULL, 10);
	//epa_cd = strtol(argv[3], NULL, 10);
	//clark_bw = strtol(argv[4], NULL, 10);
	//clark_cd = strtol(argv[5], NULL, 10);
	//wb = strtol(argv[6], NULL, 10);
	//wf = strtol(argv[7], NULL, 10);
	//cache_size = strtol(argv[8], NULL, 10);
	storeRecords(filename);
	//generateUVScores();
	//string clark_cache[cache_size];
	//string epa_cache[cache_size];
	
	record[5].server = "Done";	

	cout << "num_lines: " << num_lines << endl;
	cout << "Item: " << record[5].server << endl;

	delete[] record;
	
}
