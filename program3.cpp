#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <math.h>

using namespace std;

struct Records {
	string server;
	string date;
	string time;
	string file_request;
	int size;
	int frequency_requested;
	float uv_score;
};

Records *record;
float epa_bw;
float epa_cd;
float clark_bw;
float clark_cd;
float wb;
float wf;
int cache_size;

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
			record[num].frequency_requested = 1;
			num++;
			
		}
	
	}
	file.close();
//	cout << tokens[0] << " " << record[0].server << endl;
	//cout << "Record 4 size: " << record[3].size << endl;
	//cout << "Record 5 file requested: " << record[4].file_request << endl;
}

float generateUVScore(string server, int frequency_req, int size){
	float score = 0.0;
	if(server == "clark"){
		//cout << server << " " << frequency_req << " " << size << endl;
		score = ((clark_cd+(wb/clark_bw))*(pow(frequency_req,wf)))/size;
		//cout << score << endl;
	}else{
		score = ((clark_cd+(wb/clark_bw))*pow(frequency_req,wf))/size;
	}
	return score;
}

void cacheStoring(int i, string cache[]){
	record[i].uv_score = generateUVScore(record[i].server, record[i].frequency_requested, record[i].size);
	
}

int main(int argc, char *argv[]){
	string filename;
	//set frequency back to 1
	int num_lines = 0;
	
	filename = argv[1];
	num_lines = getLineCount(filename);
	record = new Records[num_lines];
	epa_bw = stof(argv[2]);
	epa_cd = stof(argv[3]);
	clark_bw = stof(argv[4]);
	clark_cd = stof(argv[5]);
	wb = stof(argv[6]);
	wf = stof(argv[7]);
	cache_size = strtol(argv[8], NULL, 10);
	string cache[num_lines];

	storeRecords(filename);
	for(int i = 0; i < num_lines; i++){
		cacheStoring(i, cache);
		cout << "UV Score: " << record[i].uv_score << endl;
		
	}
	
	
	//cout << "num_lines: " << num_lines << endl;
	

	delete[] record;
	
}
