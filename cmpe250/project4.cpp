/*
Student Name: Giray Eryilmaz
*/

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>

using namespace std;

int NOCities; //number of cities
int ways; //number of ways
int alpha; //number of cities got sick first night
int spreadingDays; //number of days until quarantine came down

struct City{

  bool isMarked;

  vector<int> Neighbors;

  City(){
     
    isMarked=false;    
       
  }

};

void mark(int city);

vector<City*> Cities;
queue<City*> IllQue;

int main(int argc, char *argv[]){

  ifstream fin(argv[1]);

  fin >> NOCities;
  fin >> ways;
  fin >> alpha;
  fin >> spreadingDays; 

  for(int i =0 ;i<NOCities ; i++){ //declare cities with numbers
    Cities.push_back(new City()); //put them into the list
  }

  int city_a;
  int city_b;

  for(int m =0 ;m<ways ; m++){
    fin>>city_a;
    fin>>city_b;
    Cities[city_a-1]->Neighbors.push_back(city_b-1); //cities start from 1 not 0
    Cities[city_b-1]->Neighbors.push_back(city_a-1);
  }
  
  int Ill;

  for(int i=0;i<alpha;i++){
    fin>>Ill;                           //again cities start from 1
    Cities[Ill-1]->isMarked=true;
    IllQue.push(Cities[Ill-1]);  
  }

  int size=0;
  City* temp;

  for(int i=spreadingDays; i>0 && !IllQue.empty();i--){
    size=IllQue.size();
    for(int j=0; j<size ; j++){
      temp=IllQue.front();
      IllQue.pop();
      for(vector<City*>::size_type k = 0; k < temp->Neighbors.size(); k++){
	if(!Cities[temp->Neighbors[k]]->isMarked){
	  Cities[temp->Neighbors[k]]->isMarked=true;
	  IllQue.push(Cities[temp->Neighbors[k]]);
	}
      }
    }
  }

  int counter=0;
  for(unsigned int i = 0; i<Cities.size(); i++){
    if(!Cities[i]->isMarked){
      mark(i);
      counter++;
    }
  }
  
  ofstream myfile;    
  myfile.open(argv[2]);  //open out put file
  myfile << counter <<endl;
  myfile.close();

  return 0;
}

void mark(int city){
  if(Cities[city]->isMarked)  return;
  Cities[city]->isMarked=true; 
  for(unsigned int i = 0; i<Cities[city]->Neighbors.size(); i++){
    mark(Cities[city]->Neighbors[i]);
  }
}
