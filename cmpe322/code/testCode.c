#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
 
int main () {

   int a;

	printf("this should print numbers from 10 to 19\n");
   for( a = 10; a < 20; a = a + 1 ){
      printinteger(a);
      
   }
 
   return 0;
}
