
/*
Student Name:Giray Eryilmaz
*/

#include <iostream>
#include <fstream>
#include <vector>

 using namespace std;

bool backTrack(int country, int newColor, int* colors, int N, vector<vector< bool>>& matrix);


int main(int argc, char *argv[]){
	cout<<"hi"<<endl;

    ifstream fin(argv[1]);

    int N;

    fin>>N;
    
    int colors[N];

    for(int x = 0 ; x<N ; x++){
      colors[x]= -1;
    }
   
    vector<vector<bool>> matrix(N, vector<bool>(N, false)); // NxN 2D boolean vector
    
    // fill the matrix

    int next;
    for(int i =0; i<N;i++){
      for(int j=0;j<N; j++){
	fin>>next;
	if(next==1)
	  matrix[i][j]=true;
	else
	  matrix[i][j]=false;
      }
    } 

	ofstream myfile;    
	myfile.open(argv[2]);  //open out put file

	if(backTrack(0,0,colors,N,matrix)){ //run the algorith - returns false if the map if not 4-colorable
	  for(int i =0; i<N;i++){           //fill the out put file
	    if(colors[i]==0)
	      myfile << "red" <<endl;
	    else if(colors[i]==1)
	      myfile << "blue" <<endl;
	    else if(colors[i]==2)
	      myfile << "green" <<endl;
	    else
	      myfile << "orange" <<endl;
	  }

	}else{
	  myfile << "ups"  << endl;
	}
	
	myfile.close();

    return 0;
}


bool backTrack(int country, int newColor, int* colors, int N, vector<vector< bool>>& matrix){  

  if(country>=N)
    return true; //colored all the countries

  for(int i=0;i<N;i++){
    if(matrix[country][i]==true){
      if(newColor == colors[i]){
	return false; //a neighbor namely i has this color so return false;
      }
    }
  }
  
  colors[country]=newColor; //no neighbors have this color so paint this counrty with it
  
  //call for next country
  if(backTrack(country+1,0,colors,N,matrix) || backTrack(country+1,1,colors,N,matrix)
     || backTrack(country+1,2,colors,N,matrix) || backTrack(country+1,3,colors,N,matrix)){
    return true;
  }

  return false; // dead end color of this country must change 
               //because there are no avaible colors for next guy
}
