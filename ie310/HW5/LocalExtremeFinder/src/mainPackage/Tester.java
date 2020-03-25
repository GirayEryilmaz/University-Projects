package mainPackage;

import java.io.File;
import java.io.PrintStream;
import java.util.Locale;
import java.util.Scanner;

public class Tester {

	private static final double GR = 1.61803398875;
	private static double[] coeffs;
	private static double[] original;

	public static void main(String[] args) throws Exception {

		double result = 0;

		File input = new File("input.txt");
		Scanner scanner = new Scanner(input);
		Scanner reader = scanner.useLocale(Locale.US);

		reader.nextLine();
		String type = reader.next();
		reader.nextLine();

		reader.nextLine();
		reader.nextLine();
		String coeffStr = reader.nextLine();

		coeffs = parse(coeffStr);
		original = coeffs.clone();

		reader.nextLine();
		reader.nextLine();
		String limitsLine = reader.nextLine();

		double[] limits = parse(limitsLine);

		reader.nextLine();
		reader.nextLine();

		double e = reader.nextDouble();
		reader.nextLine();

		reader.nextLine();
		reader.nextLine();
		reader.nextLine();

		int method = reader.nextInt();

		reader.close();
		scanner.close();

		/////////////////////////////
		double a, b, c, d;

		///////////////////////////
		
		
		PrintStream writer = new PrintStream(new File("output.txt"));

		a = limits[0];
		b = limits[1];

		if (type.equalsIgnoreCase("max")) {
			if (method == 1) { // bisection
				derivate();

				c = (a + b) / 2;

				while (Math.abs(f(c)) > e) {

					if (f(a) * f(c) < 0) {
						b = c;
					} else if (f(c) * f(b) < 0) {
						a = c;

					} else {

						System.out.println("No optimum or mutiple optima exists in the interval");
						writer.close();
						return;
					}

					c = (a + b) / 2;

				}

				result = c;

			} else { // golden section

				c = b - (b - a) / GR;
				d = a + (b - a) / GR;

				while (Math.abs(c - d) > e) {
					if (f(c) > f(d)) {
						b = d;

					} else {
						a = c;
					}

					c = b - (b - a) / GR;
					d = a + (b - a) / GR;

				}

				result = (a + b) / 2;
			}

		} else { // minimum
			if (method == 1) { // bisection
				derivate();

				c = (a + b) / 2;

				while (Math.abs(f(c)) > e) {

					if (f(a) * f(c) < 0) {
						b = c;
					} else if (f(c) * f(b) < 0) {
						a = c;

					} else {
						
//						System.out.println(f(a));
//						System.out.println(f(b));
//						System.out.println(f(c));
						System.out.println("No optimum or mutiple optima exists in the interval");
						writer.close();
						return;
					}

					c = (a + b) / 2;

				}

				result = c;
			} else { // golden section

				c = b - (b - a) / GR;
				d = a + (b - a) / GR;

				while (Math.abs(c - d) > e) {
					if (f(c) < f(d)) {
						b = d;

					} else {
						a = c;
					}

					c = b - (b - a) / GR;
					d = a + (b - a) / GR;

				}

				result = (a + b) / 2;
			}

		}

		

		writer.println(type);
		
		int numb = findDecPlaces(e) + 2;

		//System.out.println(numb);

		String format = "%." + numb + "f";

		writer.print("Xopt = ");
		writer.printf(format, result);
		writer.println();

		writer.print("Z = ");
		writer.printf(format, f(original, result));
		writer.println();

		writer.print("[");
		if (a > b) {
			writer.printf(format, b);
			writer.print(", ");
			writer.printf(format, a);
		} else {
			writer.printf(format, a);
			writer.print(", ");
			writer.printf(format, b);

		}
		writer.println("]");

		writer.close();

	}

	private static double f(double x) {
		return coeffs[0] * Math.pow(x, 3) + coeffs[1] * Math.pow(x, 2) + coeffs[2] * Math.pow(x, 1) + coeffs[3];

	}

	private static double f(double[] coeffs, double x) {
		return coeffs[0] * Math.pow(x, 3) + coeffs[1] * Math.pow(x, 2) + coeffs[2] * Math.pow(x, 1) + coeffs[3];

	}

	private static void derivate() {

		coeffs[3] = coeffs[2];
		coeffs[2] = coeffs[1] * 2;
		coeffs[1] = coeffs[0] * 3;
		coeffs[0] = 0;

	}

	/**
	 * 
	 * 
	 * @param s
	 *            contains doubles separated by comma ','
	 * 
	 * @return an integer array parsed from input s
	 */

	private static double[] parse(String s) {

		s = s.trim(); // get rid of possible spaces at the end or beginning of
						// the
						// string
		String[] arr = s.split(",");

		double[] doubleArray = new double[arr.length];

		for (int i = 0; i < arr.length; i++) {
			doubleArray[i] = Double.parseDouble(arr[i]);
		}
		return doubleArray;

	}
	
	
	private static int findDecPlaces(double x){
		int counter = 0;
		x = Math.abs(x);
		if(x>1){
			x = x - (int)x;
		}
		while(x<1){
			x = 10*x;
			counter++;
		}
		
		return counter;
		
		
	}

}





