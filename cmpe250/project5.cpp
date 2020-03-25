/*
Student Name: Giray Eryilmaz
*/

#include <iostream>
#include <fstream>
#include <vector>
//#include <queue>

using namespace std;

int NOCities; //number of cities
int ways; //number of ways
int start; //starting point 
int dest; //destination 

struct City{

	int dist;
	bool isMarked;
	vector<int> Neighbors;
	vector<int> Distances;

  	City(){  		   
       		isMarked=false;
		dist=-1;
  	}

};

int MaxDist(City* source, City* target , vector<City*>& Cities);

int main(int argc, char *argv[]){

	ifstream fin(argv[1]);

	fin >> NOCities;
  	fin >> ways;
  	fin >> start;
  	fin >> dest; 	

	vector<City*> Cities;

	for(int i =0 ;i<NOCities ; i++){ //declare cities with numbers
		Cities.push_back(new City()); //put them into the list
	}

  	int city_a;
  	int city_b;
  	int length;

  	for(int m =0 ;m<ways ; m++){
    		fin>>city_a;
    		fin>>city_b;		
		fin>>length;					//kendine gelen olari tutuyor ve distancelari
    		Cities[city_b-1]->Neighbors.push_back(city_a-1); //cities start from 1 not 0
    		Cities[city_b-1]->Distances.push_back(length);
  	}	
  

	Cities[start-1]->isMarked=true;
	Cities[start-1]->dist=0;

	int unknown;

	unknown = MaxDist(Cities[start-1],Cities[dest-1],Cities);
  
  ofstream myfile;    
  myfile.open(argv[2]);  //open out put file
  myfile << unknown <<endl;
  myfile.close();

  return 0;
}


int MaxDist(City* source, City* target, vector<City*>& Cities){
	if(target->isMarked) return target->dist;
	if(target->Neighbors.empty()){ target->isMarked=true; return -1;}
	
	int temp=0;
	int max_dist=-1;
	int sum=0;
	
	for(vector<City*>::size_type k = 0; k < target->Neighbors.size(); k++){
		temp=MaxDist(source,Cities[target->Neighbors[k]],Cities);
		if(temp==-1) continue;
		sum = temp + target->Distances[k];
		if(sum>max_dist){ max_dist = sum; }
		
	}

	target->dist= max_dist;
	target->isMarked=true;
	return max_dist;
}


















