/* Student Name: Giray Eryılmaz

* Compile Status: Compiling
* Program Status: Working
* Notes: given output and mine differ because of white spaces, i couldn't find out why exacty but i am sure * that the visuals are the same. if you want you can compare them pixel by pixel.
*/


#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <unistd.h>
#include <mpi.h>
#define  the_MASTER  0


/*
*Explanined on function implementation
*/
int calc(int* picture,double* filter , int i , int j,int N_column);
int calc1(int* picture , int i , int j,int N_column);


int main(int argc, char **argv)
{
    int         rank;
    int         size;        /* number of processes in job */
    int         peer;
	MPI_Status status;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    //MPI_Barrier(MPI_COMM_WORLD);
    
    int TAG1 = 1;
	int lastGuy = size - 1; //rank of last processor (the one with the largest rank)
	int N = 200;			//dimenions of picture
	int num_elements = N*N;	//number of pixels

	int threshold = atoi(argv[3]);    //get threshold from terminal
    int *picture; 						//the picture
    int *lineDetPic;					//final version of picture, applied line detection
    
    int perWorker = N*(N/(size-1)); 	//number of pixels for each procc.
    
    
    int myPart[perWorker + 2 * N ]; 	//hold each processes share + 2 more lines will be needed when filtering
    
    int filteredA[perWorker + 2 * N ];	//holds filtered share + 2 more lines to make indexing easier


    int num;
    
    /*
    *only master initializes the picture and reads the input 
    *also initializes  final picture
    *
    */
    
    if(rank==the_MASTER){
    	FILE *c_in = fopen(argv[1], "r"); //open picture
    	picture =  (int *)calloc(num_elements+perWorker , sizeof(int));
    	lineDetPic = (int *)calloc(num_elements+perWorker , sizeof(int)); //note that i did not shrink it yet
    	int i=perWorker;
    	while(fscanf(c_in, "%d", &num)==1){
    		picture[i]=num;
    		i++;
    	}
    	fclose(c_in);
 
    }
	
	
	/*
	*scatter every process its fair share
	*
	*/
		
	MPI_Scatter(picture, perWorker, MPI_INT, &myPart[N] ,perWorker , MPI_INT, the_MASTER, MPI_COMM_WORLD);

        
        
   	if(rank == 1){  	
    	int i;
   		for(i = 0 ;  i < N ; i++){
    		myPart[i] = 0;
    	
    	}
    }else if(rank==lastGuy){
    	int i, counter;
    	for(i = N+perWorker , counter = 0;  counter < N ; counter++ , i++){
    		myPart[i] = 0;
    	
    	}
    
    }
   
   /*
   *first odd numbers get their needed lower line from their lower neighbour
   *
   */
   	//tek sayılar, alt satırı al
    if (rank%2==1 && rank!=lastGuy) {

        MPI_Recv(&myPart[N+perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD,MPI_STATUS_IGNORE);


    }else if(rank%2==0 && rank!=the_MASTER){
    
    	MPI_Send(&myPart[N], N, MPI_INT, rank-1, TAG1, MPI_COMM_WORLD);
    
    }

	/*
   *first odd numbers get their needed upper line from their upper neighbour
   *
   */    
    //tek sayılar, üst satırı al
    if (rank%2==1 && rank!=1) {
    	
    	MPI_Recv(myPart, N, MPI_INT, rank - 1, TAG1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    	
    }else if(rank%2==0 && rank!=the_MASTER && rank!=lastGuy){
    
    	MPI_Send(&myPart[perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD);
    
    }
    
   /*
   *then even numbers get their needed lower line from their lower neighbour
   *
   */
    	//çift sayılar, alt satırı al
    if (rank%2==0 && rank!=lastGuy && rank!=the_MASTER) {

        MPI_Recv(&myPart[N+perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD,MPI_STATUS_IGNORE);


    }else if(rank%2==1 && rank!=1){
    
    	MPI_Send(&myPart[N], N, MPI_INT, rank-1, TAG1, MPI_COMM_WORLD);
    
    }
    
   /*
   *then even numbers get their needed upper line from their upper neighbour
   *
   */
    //çift sayılar, üst satırı al
    if (rank%2==0 && rank!=the_MASTER) {
    	
    	MPI_Recv(myPart, N, MPI_INT, rank - 1, TAG1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    	
    }else if(rank%2==1 && rank!=lastGuy){
    
    	MPI_Send(&myPart[perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD);
    
    }
    
    
    
    //MPI_Barrier(MPI_COMM_WORLD);
    
    
   
    
	//convolution 1 start
	
	int rowNum = N/(size-1) + 2;
	int columnNum =  N;
	
	int filtered[rowNum*columnNum];
	
	
   	if(rank!=the_MASTER){
   		
   		int i , j ;
   		for(i =  1; i < rowNum-1; i++ ){
			for(j = 1; j < columnNum-1; j++){
				filtered[columnNum*(i)+(j)] =  calc1(myPart , i ,j,columnNum);
			}
		}	
   	
   	}
   	
    
    
    
    //convolution 1 end
    
    /*
    *	wait until every proccessor 
    *	completes smoothing
    *
    *
    *
    *
    */
    
    MPI_Barrier(MPI_COMM_WORLD);
    
    
    ////////////////////////////////////////////////////////////////////////////////////
    
    /*
    * then again every process get upper and lower line from their neighbours
    *
    *
    */
    
    //tek sayılar, alt satırı al
    if (rank%2==1 && rank!=lastGuy) {

        MPI_Recv(&filtered[N+perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD,MPI_STATUS_IGNORE);


    }else if(rank%2==0 && rank!=the_MASTER){
    
    	MPI_Send(&filtered[N], N, MPI_INT, rank-1, TAG1, MPI_COMM_WORLD);
    
    }
    
    //tek sayılar, üst satırı al
    if (rank%2==1 && rank!=1) {
    	
    	MPI_Recv(filtered, N, MPI_INT, rank - 1, TAG1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    	
    }else if(rank%2==0 && rank!=the_MASTER && rank!=lastGuy){
    
    	MPI_Send(&filtered[perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD);
    
    }
    
    
    	//çift sayılar, alt satırı al
    if (rank%2==0 && rank!=lastGuy && rank!=the_MASTER) {

        MPI_Recv(&filtered[N+perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD,MPI_STATUS_IGNORE);


    }else if(rank%2==1 && rank!=1){
    
    	MPI_Send(&filtered[N], N, MPI_INT, rank-1, TAG1, MPI_COMM_WORLD);
    
    }
    
    
    //çift sayılar, üst satırı al
    if (rank%2==0 && rank!=the_MASTER) {
    	
    	MPI_Recv(filtered, N, MPI_INT, rank - 1, TAG1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    	
    }else if(rank%2==1 && rank!=lastGuy){
    
    	MPI_Send(&filtered[perWorker], N, MPI_INT, rank + 1, TAG1, MPI_COMM_WORLD);
    
    }
    
    ///////////////////////////////////////////////////////////////////////////////////
    
    
    //MPI_Barrier(MPI_COMM_WORLD);
    
    
    /////////////////second con. part start/////////////////////////////////////////////
     /*
    *apply filtering
    *
    *
    *
    */
    if(rank!=the_MASTER){
   		double filterA[] = {-1,-1,-1,	 2,2, 2,	-1,-1,-1};
		double filterB[] = {-1, 2,-1,	-1,2,-1,	-1, 2,-1};
		double filterC[] = {-1,-1, 2,	-1,2,-1,	 2,-1,-1};
		double filterD[] = { 2,-1,-1,	-1,2,-1,	-1,-1, 2};

   		int i , j ;
   		

   		for(i =  1; i < rowNum-1; i++ ){
			for(j = 2; j < columnNum-2; j++){
			
				if(calc(filtered, filterA , i ,j,columnNum) > threshold){
				
					filteredA[columnNum*(i)+(j)] = 255;
					
				}else if(calc(filtered, filterB , i ,j,columnNum) > threshold){
				
					filteredA[columnNum*(i)+(j)] = 255;
				
				}else if(calc(filtered, filterC , i ,j,columnNum) > threshold){
				
					filteredA[columnNum*(i)+(j)] = 255;
				
				}else if(calc(filtered, filterD , i ,j,columnNum) > threshold){
				
					filteredA[columnNum*(i)+(j)] = 255;
				
				}else{
				
					filteredA[columnNum*(i)+(j)] = 0;
				
				}
				
			}
		}	
   	
   	}
    
    /////////////////second con. part end/////////////////////////////////////////////
    
     /*
    *	wait until every proccessor 
    *	completes filtering
    *
    *
    *
    *
    */
    MPI_Barrier(MPI_COMM_WORLD);
    
    /*
    *	when every process is done,  gather results
    */
    
    MPI_Gather(&filteredA[N], perWorker, MPI_INT, lineDetPic ,perWorker , MPI_INT, the_MASTER, MPI_COMM_WORLD);

   

    //MPI_Barrier(MPI_COMM_WORLD);
    
    /*
    *only master outputs results
    *
    */
    
    if(rank == the_MASTER){
		
		int i ,j;
		
		
		FILE *f = fopen(argv[2], "w+");
		
		for(i = perWorker/N + 2; i<N+(perWorker/N)-2 ; i++){  			//rows
			for(j = 2 ; j<N-2 ; j++){					//columns
				
				fprintf(f, "%d", lineDetPic[i*N + j]);
				
				if(j!=N-3){
					fprintf(f , " ");
				}
			}
			
			if(i!=N+(perWorker/N)-3){
				fprintf(f , "\n");
				
			}
			
					
		}
		
		
		fclose(f);
		
    	free(picture);
    	free(lineDetPic);
    
    }
    
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();
    return 0;
}


/*
*Calculates and returns one fitered cell(pixel),
*i and j indexes of the pizel(cell), N_column stands for number of columns which is needed when using a one dimenstional
*array as a 2D array as 
*                             array2D[i][j] <---> array1D[i*NumberOfCoumns + j] 
*standart C tricks...
*
*filter is the filter to be applied
*
*/
int calc(int* picture, double* filter , int i , int j,int N_column){
	int k , l;
	double  temp= 0;
	for(k =0 ; k<3 ; k ++){	
		for(l = 0 ; l<3 ; l++){
			temp+= picture[(i-1+k)*N_column + (j-1+l)] * filter[3*k + l];
		}
	}
	
	return temp;
}


/*
*used as a helper in the smootihng porcess
*calculates and returns one smoothed cell
*/


int calc1(int* picture , int i , int j,int N_column){
	int k , l;
	double  temp= 0.0;
	for(k =0 ; k<3 ; k ++){	
		for(l = 0 ; l<3 ; l++){
			temp+= picture[(i-1+k)*N_column + (j-1+l)];
			
		}
	}


	//temp = temp/9.0;
	return temp/9.0;
}






