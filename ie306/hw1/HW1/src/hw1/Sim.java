package hw1;
//import java.util.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

class Sim {

	// Class Sim variables
	public static double Clock, MeanInterArrivalTime, MeanServiceTime, SIGMA, LastEventTime, TotalBusy, SumResponseTime;
	
	public static long NumberOfCustomers, QueueLength, NumberInService, TotalCustomers, NumberOfDepartures;

	public final static int arrival = 1;
	public final static int departure = 2;

	public static EventList FutureEventList;
	public static Queue Customers;
	public static Random stream;

	public static List<Double> RenegeQueue;
	public static int minPatience = 10;
	public static int maxPatience = 30;

	public static int renegedCounter = 0;
	public static double totalServiceTime = 0.0;
	public static double totalWaitingTime = 0.0;

	public static void main(String argv[]) {
		
		MeanInterArrivalTime = 4.5;
		MeanServiceTime = 3.2;
		SIGMA = 0.6;
		TotalCustomers = 1000;

		long seed = Long.parseLong("12345");
		seed = Long.parseLong(argv[0]);
		TotalCustomers = Integer.parseInt(argv[1]); 
		System.out.println("seed <- " + seed + " and TotalCustomers <- " + TotalCustomers);

		stream = new Random(seed); // initialize rng stream
		FutureEventList = new EventList();
		Customers = new Queue();
		RenegeQueue = new ArrayList<>();

		Initialization();

		// Loop until first "TotalCustomers" have departed
		while (NumberOfDepartures < TotalCustomers) {
			Event evt = (Event) FutureEventList.getMin(); // get imminent event
			FutureEventList.dequeue(); // be rid of it
			Clock = evt.get_time(); // advance simulation time
			if (evt.get_type() == arrival) {
				ProcessArrival(evt);
				//System.out.println("hello");
			} else {
				ProcessDeparture(evt);
			}
			// System.out.println(FutureEventList.size);
		}
		ReportGeneration();
	}

	public static void ProcessArrival(Event evt) {
		Customers.enqueue(evt);
		QueueLength++;

		RenegeQueue.add(Clock + uniform(stream, minPatience, maxPatience));

		// if the server is idle, fetch the event, do statistics
		// and put into service
		if (NumberInService == 0)
			ScheduleDeparture();
		else
			TotalBusy += (Clock - LastEventTime); // server is busy



		// schedule the next arrival
		Event next_arrival = new Event(arrival, Clock + exponential(stream, MeanInterArrivalTime));
		FutureEventList.enqueue(next_arrival);
		LastEventTime = Clock;
	}

	public static void ScheduleDeparture() {
		double ServiceTime;
		// get the job at the head of the queue
		while ((ServiceTime = normal(stream, MeanServiceTime, SIGMA)) < 0)
			;

		Event depart = new Event(departure, Clock + ServiceTime);
		depart.serviceTime = ServiceTime;
		FutureEventList.enqueue(depart);
		NumberInService = 1;
		QueueLength--;

		RenegeQueue.remove(0);
	}

	public static void ProcessDeparture(Event e) {
		// get the customer description
		Event finished = (Event) Customers.dequeue();
		// System.out.println("Clock: " + Clock + ", arrival: " +
		// finished.get_time());
		double renegeTime = 0;
		// if there are customers in the queue then schedule
		// the departure of the next one
		//System.out.println("NumberOfDepartures = " + NumberOfDepartures);
		 //System.out.println("resp - serv " + String.valueOf( e.serviceTime));

		if (QueueLength > 0) {
			//double renegeTime = 0;
			renegeTime = RenegeQueue.get(0);
			// System.out.println("Clock: " + Clock + ", renege: " +
			// renegeTime);
			while (Clock > renegeTime && NumberOfDepartures < TotalCustomers - 1) {
				RenegeQueue.remove(0);
				NumberOfDepartures++;
				Customers.dequeue();
				QueueLength--;
				renegedCounter++;
				//System.out.println("------------ RENEGE ------------------");
				 //System.out.println(QueueLength);
				if (QueueLength <= 0)
					break;

				renegeTime = RenegeQueue.get(0);
			}

			if (QueueLength > 0){
				ScheduleDeparture();
				
			}else{
				NumberInService = 0; //bu else eksikti sanirim
			}
		} else {
			NumberInService = 0;

		}
		// measure the response time and add to the sum
		// System.out.println("Clock: " + Clock + " Finish get time: " +
		// finished.get_time());
		// System.out.println("service time " + e.serviceTime);
		
		if(Clock > renegeTime && NumberOfDepartures == TotalCustomers - 1){
			LastEventTime = renegeTime;
			Clock = renegeTime;
		}else{
			totalServiceTime += e.serviceTime;
			totalWaitingTime += Clock - finished.get_time() - e.serviceTime;
			double response = (Clock - finished.get_time());
			SumResponseTime += response;
			TotalBusy += (Clock - LastEventTime);
			LastEventTime = Clock;
		}
		
		
		
		
		NumberOfDepartures++;
		
		
		
	}

	public static void ReportGeneration() {



		System.out.println("Service utilization: " + Double.toString(totalServiceTime / LastEventTime));
		System.out.println("Average Waiting Time: " + totalWaitingTime / (TotalCustomers - renegedCounter));
		System.out.println("Number of Reneged Customers: " + renegedCounter);
	}

	// seed the event list with TotalCustomers arrivals
	public static void Initialization() {
		Clock = 0.0;
		QueueLength = 0;
		NumberInService = 0;
		LastEventTime = 0.0;

		SumResponseTime = 0;
		NumberOfDepartures = 0;


		// create first arrival event
		Event evt = new Event(arrival, exponential(stream, MeanInterArrivalTime));
		FutureEventList.enqueue(evt);

		// RenegeQueue.add(evt.get_time() + uniform(new Random(), minPatience,
		// maxPatience));
	}

	private static double exponential(Random rng, double mean) {
		return -mean * Math.log(rng.nextDouble());
	}

	private static double uniform(Random rng, int MinPatience, int MaxPatience) {
		return ((MaxPatience - MinPatience) * rng.nextDouble() + MinPatience);
	}

	public static double SaveNormal;
	public static int NumNormals = 0;
	public static final double PI = 3.1415927;

	public static double normal(Random rng, double mean, double sigma) {
		double ReturnNormal;
		// should we generate two normals?
		if (NumNormals == 0) {
			double r1 = rng.nextDouble();
			double r2 = rng.nextDouble();
			ReturnNormal = Math.sqrt(-2 * Math.log(r1)) * Math.cos(2 * PI * r2);
			SaveNormal = Math.sqrt(-2 * Math.log(r1)) * Math.sin(2 * PI * r2);
			NumNormals = 1;
		} else {
			NumNormals = 0;
			ReturnNormal = SaveNormal;
		}
		return ReturnNormal * sigma + mean;
	}
}