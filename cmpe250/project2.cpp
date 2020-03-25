
/*
Student Name:Giray Eryilmaz
*/
#include <iostream>
#include <fstream>
#include <algorithm>
#include <cstdlib>
#include <vector>
#include <queue>

using namespace std;

struct kargo_packet
{

  int lists[4];

  int no;
  double time;

  double arriveTime;

  double timeInProcess; //dont forgetto deal with arrival time

  kargo_packet(double nTime, int nNo)
  {

    lists[0] = 1;  //0 kargo Que
    lists[1] = -1; //1 first line servers
    lists[2] = -1; //2second Que
    lists[3] = -1; //3 second line servers

    time = nTime;

    no = nNo;

    arriveTime = nTime;
  }
};

int f_l;
int s_l;
int numb_cargos;

double *first_level;
double *second_level;
double *cargos;

double to_Print[12];

int readData(char *infileName);
int layOut1(char *outfileName);
int layOut2(char *outfileName);
void InsertIn(double newNum, vector<kargo_packet *> &the_heap, int no);
kargo_packet *PopTheMin(vector<kargo_packet *> &the_heap);
void InsertIn(kargo_packet *newNum, vector<kargo_packet *> &the_heap);
void adjust_times_inHeap(double time_Passed, vector<kargo_packet *> &the_heap);

int main(int argc, char *argv[])
{

  readData(argv[1]);

  layOut1(argv[2]);

  layOut2(argv[2]);

  //writes the out put...

  ofstream myfile;
  myfile.open(argv[2]);
  for (int i = 0; i < 6; i++)
  {
    myfile << to_Print[i] << endl;
  }

  myfile << endl;

  for (int i = 6; i < 12; i++)
  {
    myfile << to_Print[i] << endl;
  }

  myfile.close();

  delete[] first_level;
  delete[] second_level;
  delete[] cargos;

  return 0;
}

int readData(char *infileName)
{

  std::ifstream fin(infileName);

  fin >> f_l;
  first_level = new double[f_l];

  for (int i = 0; i < f_l; i++)
  {
    fin >> first_level[i];
  }

  fin >> s_l;

  second_level = new double[s_l];

  for (int i = 0; i < s_l; i++)
  {
    fin >> second_level[i];
  }

  fin >> numb_cargos;

  cargos = new double[numb_cargos];

  for (int i = 0; i < numb_cargos; i++)
  {
    fin >> cargos[i];
  }

  return 0;
}

int layOut1(char *outfileName)
{

  unsigned int f_longest = 0;

  unsigned int s_longest = 0;

  double currentTime = 0; //includes waiting for the first packet
  double totalRunningTimeOfTheOffice = 0;
  bool fst_servers[f_l]; //false mean empty true means busy (for both)
  bool snd_servers[s_l];
  double totalTurnAroundTime = 0;
  double longestWaitTime = 0;
  double totalWaitTime = 0;
  kargo_packet *temp;

  for (int i = 0; i < f_l; i++)
  {
    fst_servers[i] = false;
  }

  for (int i = 0; i < s_l; i++)
  {
    snd_servers[i] = false;
  }

  vector<kargo_packet *> the_heap;

  the_heap.push_back(new kargo_packet(0, -1)); //fill 0th element. i wont use that

  queue<kargo_packet *> FLQ;
  queue<kargo_packet *> SLQ;

  for (int i = 0; i < numb_cargos; i++)
  {
    InsertIn(cargos[i], the_heap, i);
  }

  bool is_blocked = true;

  while (true)
  {

    if (s_longest < SLQ.size())
    {
      s_longest = SLQ.size();
    }

    if (f_longest < FLQ.size())
    {
      f_longest = FLQ.size();
    }

    if (!SLQ.empty())
    {
      temp = SLQ.front();
      for (int j = 0; j < s_l; j++)
      {
        if (!snd_servers[j])
        {
          temp->timeInProcess += second_level[j];

          temp->lists[2] = -1; //luzumsuz galiba
          temp->lists[3] = j;
          snd_servers[j] = true;
          temp->time = second_level[j];

          InsertIn(temp, the_heap);

          SLQ.pop(); //since we found a place for this guy, we pop it.

          break;
        }
      }
    }

    if (!FLQ.empty())
    {
      temp = FLQ.front();
      for (int i = 0; i < f_l; i++)
      {
        if (!fst_servers[i])
        {
          temp->lists[0] = -1;
          temp->lists[1] = i;
          fst_servers[i] = true;
          temp->time = first_level[i];
          temp->timeInProcess += first_level[i];
          InsertIn(temp, the_heap);
          FLQ.pop();

          break;
        }
      }
    }

    is_blocked = true;

    temp = PopTheMin(the_heap);

    if (temp->lists[0] != -1)
    { //if waiting to arrive

      for (int i = 0; i < f_l; i++)
      {
        if (!fst_servers[i])
        {

          currentTime += temp->time; //pass the arrival time
          adjust_times_inHeap(temp->time, the_heap);
          temp->lists[0] = -1;
          temp->lists[1] = i;
          fst_servers[i] = true;
          temp->time = first_level[i];
          temp->timeInProcess += first_level[i];
          is_blocked = false;
          InsertIn(temp, the_heap);

          break;
        }
      }
      if (is_blocked)
      {
        currentTime += temp->time;                 //process made (the arrival)
        adjust_times_inHeap(temp->time, the_heap); //time passed for everyone in heap
        temp->time = 0;                            //just idle waiting
        temp->lists[0] = -1;                       //list[0] means "waiting to arrive" now
        FLQ.push(temp);
      }
    }
    else if (temp->lists[1] != -1)
    {                                      //if in first servers
      fst_servers[temp->lists[1]] = false; //clean the place in bool array fst_servers
      currentTime += temp->time;           //lists[1] is the number indicates its place in flservers
      adjust_times_inHeap(temp->time, the_heap);
      temp->lists[1] = -1;
      temp->lists[2] = 1;
      temp->time = 0;
      SLQ.push(temp);
    }
    else if (temp->lists[3] != -1)
    { //if in second servers
      currentTime += temp->time;
      adjust_times_inHeap(temp->time, the_heap);
      snd_servers[temp->lists[3]] = false;
      temp->lists[3] = -1; //not necessary i think because i dont push it to heap again
                           //consider deleting it somewhere

      totalWaitTime += currentTime - temp->timeInProcess - temp->arriveTime;

      totalTurnAroundTime += currentTime - temp->arriveTime;
      if (longestWaitTime < currentTime - temp->timeInProcess - temp->arriveTime)
      {
        longestWaitTime = currentTime - temp->timeInProcess - temp->arriveTime;
      }
    }

    if (the_heap.size() == 1 && FLQ.empty() && SLQ.empty())
    {
      totalRunningTimeOfTheOffice = currentTime - cargos[0];

      break;
    }
  }

  to_Print[0] = totalTurnAroundTime / numb_cargos;
  to_Print[1] = f_longest;
  to_Print[2] = s_longest;
  to_Print[3] = totalWaitTime / numb_cargos;
  to_Print[4] = longestWaitTime;
  to_Print[5] = totalRunningTimeOfTheOffice;

  return 0;
}

int layOut2(char *outfileName)
{

  unsigned int f_longest = 0;

  unsigned int s_longest = 0;

  double currentTime = 0; //includes waiting for the first packet
  double totalRunningTimeOfTheOffice = 0;
  bool fst_servers[f_l]; //false mean empty true means busy (for both)
  bool snd_servers[s_l];

  double totalTurnAroundTime = 0;
  double longestWaitTime = 0;
  double totalWaitTime = 0;
  kargo_packet *temp;

  for (int i = 0; i < f_l; i++)
  {
    fst_servers[i] = false;
  }

  for (int i = 0; i < s_l; i++)
  {
    snd_servers[i] = false;
  }

  vector<kargo_packet *> the_heap;

  the_heap.push_back(new kargo_packet(0, -1)); //fill 0th element. i wont use that

  queue<kargo_packet *> *SLQs[s_l];

  for (int i = 0; i < s_l; i++)
  {
    SLQs[i] = new queue<kargo_packet *>;
  }

  queue<kargo_packet *> FLQ;

  for (int i = 0; i < numb_cargos; i++)
  {

    InsertIn(cargos[i], the_heap, i);
  }

  bool is_blocked = true;

  while (true)
  {

    for (int i = 0; i < s_l; i++)
    {
      if (SLQs[i]->size() > s_longest)
      {
        s_longest = SLQs[i]->size();
      }
    }

    if (f_longest < FLQ.size())
    {
      f_longest = FLQ.size();
    }

    for (int i = 0; i < s_l; i++)
    {
      if (!SLQs[i]->empty())
      { //in second level queues
        temp = SLQs[i]->front();
        if (!snd_servers[temp->lists[2]])
        {
          temp->lists[3] = temp->lists[2];
          temp->timeInProcess += second_level[temp->lists[3]];
          temp->lists[2] = -1;
          snd_servers[temp->lists[3]] = true;
          temp->time = second_level[temp->lists[3]];
          InsertIn(temp, the_heap);
          SLQs[i]->pop();
          break; // sure to break?
        }
      }
    }

    if (!FLQ.empty())
    {
      temp = FLQ.front();
      for (int i = 0; i < f_l; i++)
      {
        if (!fst_servers[i])
        {
          temp->lists[0] = -1;
          temp->lists[1] = i;
          fst_servers[i] = true;
          temp->time = first_level[i];
          temp->timeInProcess += first_level[i];
          InsertIn(temp, the_heap);
          FLQ.pop();

          break;
        }
      }
    }

    is_blocked = true;

    temp = PopTheMin(the_heap);

    if (temp->lists[0] != -1)
    { //if waiting to arrive

      for (int i = 0; i < f_l; i++)
      {
        if (!fst_servers[i])
        {

          currentTime += temp->time; //pass the arrival time

          adjust_times_inHeap(temp->time, the_heap);
          temp->lists[0] = -1;
          temp->lists[1] = i;
          fst_servers[i] = true;
          temp->time = first_level[i];
          temp->timeInProcess += first_level[i];
          is_blocked = false;

          InsertIn(temp, the_heap);

          break;
        }
      }
      if (is_blocked)
      {
        currentTime += temp->time;                 //process made (the arrival)
        adjust_times_inHeap(temp->time, the_heap); //time passed for everyone in heap
        temp->time = 0;                            //just idle waiting
        temp->lists[0] = -1;                       //list[0] means "waiting to arrive" now
        FLQ.push(temp);
      }
    }
    else if (temp->lists[1] != -1)
    {                                      //if in first servers
      fst_servers[temp->lists[1]] = false; //clean the place in bool array fst_servers
      currentTime += temp->time;           //lists[1] is the number indicates its place in flservers
      adjust_times_inHeap(temp->time, the_heap);

      SLQs[temp->lists[1] / 2]->push(temp);
      temp->lists[2] = temp->lists[1] / 2;
      temp->lists[1] = -1;
      temp->time = 0;
    }
    else if (temp->lists[3] != -1)
    { //if in second servers
      currentTime += temp->time;
      adjust_times_inHeap(temp->time, the_heap);
      snd_servers[temp->lists[3]] = false;
      temp->lists[3] = -1; //not necessary i think because i dont push it to heap again
                           //consider deleting it somewhere

      totalWaitTime += currentTime - temp->timeInProcess - temp->arriveTime;
      totalTurnAroundTime += currentTime - temp->arriveTime;
      if (longestWaitTime < currentTime - temp->timeInProcess - temp->arriveTime)
      {
        longestWaitTime = currentTime - temp->timeInProcess - temp->arriveTime;
      }
    }

    bool isSLQsEmpty = true;

    for (int i = 0; i < s_l; i++)
    {
      if (!SLQs[i]->empty())
      { //looking for non empty
        isSLQsEmpty = false;
        break;
      }
    }

    if (the_heap.size() == 1 && FLQ.empty() && isSLQsEmpty)
    {
      totalRunningTimeOfTheOffice = currentTime - cargos[0];

      break;
    }
  }

  to_Print[6] = totalTurnAroundTime / numb_cargos;
  to_Print[7] = f_longest;
  to_Print[8] = s_longest;
  to_Print[9] = totalWaitTime / numb_cargos;
  to_Print[10] = longestWaitTime;
  to_Print[11] = totalRunningTimeOfTheOffice;

  return 0;
}

kargo_packet *PopTheMin(vector<kargo_packet *> &the_heap)
{

  kargo_packet *first_El = the_heap[1];

  the_heap[1] = the_heap.back();
  the_heap.pop_back();

  unsigned int i = 1;

  while (true)
  {
    if (2 * i > the_heap.size())
    {
      break;
    }
    else
    {

      if (2 * i + 1 > the_heap.size())
      {

        if (the_heap[2 * i]->time < the_heap[i]->time)
        {
          swap(the_heap[i], the_heap[2 * i]);
          i = 2 * i;
        }
        else
        {
          break;
        }
      }
      else
      {

        if (the_heap[2 * i]->time <= the_heap[2 * i + 1]->time && the_heap[2 * i]->time < the_heap[i]->time)
        {
          swap(the_heap[i], the_heap[2 * i]);
          i = 2 * i;
        }
        else if (the_heap[2 * i + 1]->time < the_heap[2 * i]->time && the_heap[2 * i + 1]->time < the_heap[i]->time)
        {
          swap(the_heap[i], the_heap[2 * i + 1]);
          i = 2 * i + 1;
        }
        else
        {
          break;
        }
      }
    }
  }

  return first_El;
}

void InsertIn(double newNum, vector<kargo_packet *> &the_heap, int no)
{

  kargo_packet *kpp = new kargo_packet(newNum, no);

  the_heap.push_back(kpp);

  int x = the_heap.size() - 1;

  for (int i = x; i > 1; i /= 2)
  {
    if (the_heap[i]->time < the_heap[i / 2]->time)
    {
      swap(the_heap[i], the_heap[i / 2]);
    }
    else
    {
      break;
    }
  }
}

void InsertIn(kargo_packet *newNum, vector<kargo_packet *> &the_heap)
{

  the_heap.push_back(newNum);

  int x = the_heap.size() - 1;

  for (int i = x; i > 1; i /= 2)
  {
    if (the_heap[i]->time < the_heap[i / 2]->time)
    {
      swap(the_heap[i], the_heap[i / 2]);
    }
    else
    {
      break;
    }
  }
}

void adjust_times_inHeap(double time_Passed, vector<kargo_packet *> &the_heap)
{

  if (time_Passed == 0)
  {

    return;
  }
  else if (time_Passed < 0)
  {
    cout << "man! time passsed cant be negative:  " << time_Passed << endl;
    cout << "size of heap:   " << the_heap.size() << endl;
  }

  for (vector<kargo_packet *>::size_type i = 1; i < the_heap.size(); i++)
  {
    the_heap[i]->time = the_heap[i]->time - time_Passed;
  }
}
