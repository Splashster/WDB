/*
	The purpose of this program is to simulate the Hybrid replacement scheme for caching.
*/

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


//Gets total number of lines in the file
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

//Stores each item in the file 
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
}

//Generates the UV score for each requested item
float generateUVScore(string server, int frequency_req, int size){
	float score = 0.0;
	if(server == "clark"){
		score = ((clark_cd+(wb/clark_bw))*(pow(frequency_req,wf)))/size;
	}else{
		score = ((clark_cd+(wb/clark_bw))*pow(frequency_req,wf))/size;
	}
	return score;
}

//Adds a requested item into the cache if it is not already there
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

//Replaces x item(s) in the cache depending on how much space is in the cache
//Replace algorithm works as follows
//First a check is done to see what the lowest UV score in the cache currently is
//Second a check is done to see which items have that UV score
//If only one item has that score, that item is marked to be removed from the cache
//If multiple items have that score, the items' last date accessed are used as tiebreakers and if they are the same,
//the last time accessed is used as a tiebreaker
//Third the marked item is removed and a check is done to see if the new item can fit into the cache
//If it cannot, the next lowest scored item in the cache is removed until it can fit
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

//Acquires and stores the uv score for the requested it
//Checks to see if the requested item is in the cache
//Increments the hit or miss variables depending on if the item is in the cache
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

	storeRecords(filename);
	for(int i = 0; i < num_lines; i++){
		cacheStoring(i);
	}
	
	hit_ratio = ((float)hits/(float)num_lines)*100;

	cout << "Number of cache hits: " << hits << endl;
	cout << "Number of cache misses: " << misses << endl;
	cout << "Cache hit ratio as a percentage: " << hit_ratio << "%" << endl;
	cout << "Number of times the replacement algorithm was called: " << num_replace_alg_called << endl;
	cout << "Maximum number of objects replaced in a single call of the replacement algorithm: " << max_objs_replaced << endl;
	cout << "Lowest UV for a cached object: " << lowest_uv << endl;
	cout << "Highest UV for a cached object: " << highest_uv << endl;



	delete[] record;
	
}
