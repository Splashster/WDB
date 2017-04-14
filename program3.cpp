#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <math.h>
#include <vector>
#include <iomanip>

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
vector<Records> cached_item;

float epa_bw;
float epa_cd;
float clark_bw;
float clark_cd;
float wb;
float wf;
string h_s, l_s;
int h_size,l_size;
float h_f,h_uv,l_f,l_uv;
int init_cache_size;
int cache_size_left;
int hits = 0;
int misses = 0;
float hit_ratio = 0.0;
int num_replace_alg_called = 0;
int max_objs_replaced = 0;
float lowest_uv = 0.0;
float highest_uv = 0.0;

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

void addItem(int i){
	int index = 0;
	cached_item.push_back(record[i]);
	index = cached_item.size()-1;
	cache_size_left -= record[i].size; 
	
	if(cached_item[index].uv_score > highest_uv || highest_uv == 0.0){
		highest_uv = cached_item[index].uv_score;
		h_s = cached_item[index].server;
		h_size = cached_item[index].size;
		h_f = cached_item[index].frequency_requested;	
		h_uv = cached_item[index].uv_score;
			
	}
	if(cached_item[index].uv_score < lowest_uv || lowest_uv == 0.0){
		lowest_uv = cached_item[index].uv_score;
		l_s = cached_item[index].server;
		l_size = cached_item[index].size;
		l_f = cached_item[index].frequency_requested;	
		l_uv = cached_item[index].uv_score;		
	}
	index++;
}

void replace(int i){
	float low_score = 0;
	int remove_index = 0;
	string date;
	string time;
	int num_objs_replaced = 0;
	
	for(int c = 0; c < cached_item.size(); c++)
	{
		if(low_score > cached_item[c].uv_score || low_score == 0)
		{
			low_score = cached_item[c].uv_score;
			date = cached_item[c].date;
			time = cached_item[c].time;
			remove_index = c;
		}else if(low_score == cached_item[c].uv_score){
			if(cached_item[c].date < date){	
				low_score = cached_item[c].uv_score;
				date = cached_item[c].date;
				time = cached_item[c].time;
				remove_index = c;		
			}else if (cached_item[c].time < time){
				low_score = cached_item[c].uv_score;
				date = cached_item[c].date;
				time = cached_item[c].time;
				remove_index = c;			
			}	
		}
	}
	for(int c = 0; c < cached_item.size(); c++)
	{
		if(low_score == cached_item[c].uv_score)
		{
			cache_size_left += cached_item[remove_index].size;
			cached_item.erase(cached_item.begin()+remove_index);
			//index--;
			num_objs_replaced++;
			if(record[i].size < cache_size_left){
				addItem(i);
				break;
			}
		}
	}
	if(num_objs_replaced > max_objs_replaced){
		max_objs_replaced = num_objs_replaced;
	}
}

void cacheStoring(int i){
	record[i].uv_score = generateUVScore(record[i].server, record[i].frequency_requested, record[i].size);
	bool found = false;
	if(cache_size_left == init_cache_size){
		addItem(i);
		misses++;
	}else{
		for(int a = 0; a < cached_item.size(); a++){
			if(record[i].file_request == cached_item[a].file_request){
				cached_item[a].frequency_requested++;
				cached_item[a].date = record[i].date;
				cached_item[a].time = record[i].time;
				found = true;	
				break;		
			} 	
		}		
		if(found){
			hits++;	
				
		}else{
			if(record[i].size < cache_size_left && cache_size_left != 0){
				addItem(i);
			}else{
				replace(i);
				num_replace_alg_called++;			
			}
			misses++;
		}
	}
	
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
	init_cache_size = strtol(argv[8], NULL, 10) * 1000000;
	cache_size_left = init_cache_size;
	//cached_item = new cache[num_lines];

	storeRecords(filename);
	for(int i = 0; i < num_lines; i++){
		cacheStoring(i);
		//cout << "UV Score: " << record[i].uv_score << endl;
		
	}
	
	hit_ratio = ((float)hits/(float)num_lines)*100;
	
	//cout << "cache left " << cache_size_left << endl;
	cout << "Number of cache hits: " << hits << endl;
	cout << "Number of cache misses: " << misses << endl;
	cout << "Cache hit ratio as a percentage: " << hit_ratio << "%" << endl;
	cout << "Number of times the replacement algorithm was called: " << num_replace_alg_called << endl;
	cout << "Maximum number of objects replaced in a single call of the replacement algorithm: " << max_objs_replaced << endl;
	cout << "Lowest UV for a cached object: " << lowest_uv << endl;
	cout << "Highest UV for a cached object: " << highest_uv << endl;
	//cout << "Reqs " << cached_item[0].rec.frequency_requested << endl;
	
	cout << "High_s: " << h_s << endl;
	cout << "High_size: " << h_size << endl;
	cout << "High_f: " << h_f << endl;
	cout << "High_uv: " << h_uv << endl;
	cout << "Low_s: " << l_s << endl;
	cout << "Low_size: " << l_size << endl;
	cout << "Low_f: " << l_f << endl;
	cout << "Low_uv: " << l_uv << endl;


	delete[] record;
	//delete[] cached_item;
	
}
