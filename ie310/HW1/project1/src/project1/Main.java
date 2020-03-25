package project1;

import java.io.File;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Locale;
import java.util.Scanner;

import Jama.Matrix;

public class Main {

	public static void main(String[] args) {
		
		int n = 0, m = 0;
		String cTString = "";
		double[][] cT = new double[1][1];

		try {

			// Matrix M = new Matrix(cT);

			File input = new File("input.txt");
			Scanner reader = new Scanner(input).useLocale(Locale.US);
			PrintStream pt = new PrintStream(new File("output.txt"));

			reader.nextLine();

			n = reader.nextInt(); // get n

			reader.nextLine(); // reader.nextLine(); --> just to get rid of
								// empty lines and stuff
			reader.nextLine();
			reader.nextLine();

			m = reader.nextInt(); // get m

			double[][] matrixA = new double[m][n]; // initilaze the matrix A
			double[][] vectorB = new double[m][1]; // initilaze vector b (right
													// hand
													// side coeffs)
			int[] basicVar = new int[m]; // initilaze an array to hold basic
											// variables

			reader.nextLine();
			reader.nextLine();
			reader.nextLine();

			cTString = reader.nextLine(); // get vector c transpose as a line
											// did not get the numbers to an
											// array by one by because
											// number of elements is not known
											// in advance

			cT[0] = parse(cTString); // the string is parsed to an array of
										// doubles

			reader.nextLine();
			reader.nextLine();

			for (int i = 0; i < m; i++) { // read the matrix to a 2D array
				for (int j = 0; j < n; j++) {
					matrixA[i][j] = reader.nextDouble();
				}
			}

			reader.nextLine();
			reader.nextLine();
			reader.nextLine();

			for (int i = 0; i < m; i++) { // read vector b to an array
				vectorB[i][0] = reader.nextDouble();
			}

			reader.nextLine();
			reader.nextLine();
			reader.nextLine();

			for (int i = 0; i < m; i++) { // read basic variables to an array
				basicVar[i] = reader.nextInt();
			}

			Arrays.sort(basicVar); // sort the array not crucial though

			// test begin
			double[][] thebase = findBase(matrixA, basicVar);
			
			double[][] theNotbase = findNotBase(matrixA, basicVar);
			
			Matrix resultMatrix = Matrix.constructWithCopy(thebase);
			resultMatrix = resultMatrix.inverse();

			double[][] result = resultMatrix.getArray();
		

			

			Matrix resultMatrix2 = resultMatrix.times(Matrix.constructWithCopy(theNotbase));

			// double [][] result2 = matrixMult(result, theNotbase);

			double[][] result2 = resultMatrix2.getArray();
			

			Matrix resultMatrix3 = resultMatrix.times(Matrix.constructWithCopy(vectorB));

			// double [][] result2 = matrixMult(result, theNotbase);

			double[][] result3 = resultMatrix3.getArray();

			// double [][] result3 = matrixMult(result, vectorB);

			
			double[][] cBT = findBase(cT, basicVar);

			Matrix cBTMatrix = Matrix.constructWithCopy(cBT);

			Matrix resultMatrix4 = cBTMatrix.times(resultMatrix3);

			double[][] result4 = resultMatrix4.getArray();

			// double [][] result4 = matrixMult(cBT, result3);

			
			double[][] cNT = findNotBase(cT, basicVar);

			double[][] result6 = cBTMatrix.times(resultMatrix).times(Matrix.constructWithCopy(theNotbase)).getArray();

			// double [][] result5 = matrixMult(cBT, result);
			// double [][] result6 = matrixMult(result5, theNotbase);

			double[][] result7 = sub(result6, cNT);
			
	//-------------------------------------------------------
			
		System.out.println("1. B=\n");
		pt.println("1. B=");
		pt.println();
		for (int i = 0; i < thebase.length; i++) {
			for (int a = 0; a < thebase[0].length; a++) {
				System.out.print(thebase[i][a] + " ");
				pt.print(thebase[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}

		System.out.println("\n2. N=\n");
		pt.println("\r\n2. N=\r\n");
		for (int i = 0; i < theNotbase.length; i++) {
			for (int a = 0; a < theNotbase[0].length; a++) {
				System.out.print(theNotbase[i][a] + " ");
				pt.print(theNotbase[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}

		System.out.println("\n3. B_inverse=\n");
		pt.println("\r\n3. B_inverse=\r\n");
		round(result,1);

		for (int i = 0; i < thebase.length; i++) {
			for (int a = 0; a < thebase[0].length; a++) {
				System.out.print(result[i][a] + "\t");
				pt.print(result[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}

		System.out.println("\n4. B_inverse.N=\n");
		pt.println("\r\n4. B_inverse.N=\r\n");
		round(result2,1);
		for (int i = 0; i < thebase[0].length; i++) {
			for (int a = 0; a < theNotbase.length; a++) {
				System.out.print(result2[i][a] + " ");
				pt.print(result2[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}

		System.out.println("\n5. B_inverse.b=\n");
		pt.println("\r\n5. B_inverse.b=\r\n");
		round(result3,1);
		for (int i = 0; i < result3.length; i++) {
			for (int a = 0; a < result3[0].length; a++) {
				System.out.print(result3[i][a] + " ");
				pt.print(result3[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}
		
		System.out.println("\n6. CBtranspose.B_inverse.b=\n");
		pt.println("\r\n6. CBtranspose.B_inverse.b=\r\n");
		
		round(result4,1);
		for (int i = 0; i < result4.length; i++) {
			for (int a = 0; a < result4[0].length; a++) {
				System.out.print(result4[i][a] + " ");
				pt.print(result4[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}

		System.out.println("\n7. CBtranspose.B_inverse.N-CNtranpose=\n");
		pt.println("\r\n7. CBtranspose.B_inverse.N-CNtranpose=\r\n");

		round(result7,1);
		for (int i = 0; i < result7.length; i++) {
			for (int a = 0; a < result7[0].length; a++) {
				System.out.print(result7[i][a] + " ");
				pt.print(result7[i][a] + "\t");
			}
			System.out.println();
			pt.println();
		}
			// test end

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
			System.err.println("full name of the input file must be input.txt and it has to be in the project folder");

		}
	}



	/**
	 * 
	 * 
	 * @param s
	 *            contains integers seperated by one space
	 * 
	 * @return an integer array parsed from input s
	 */

	private static double[] parse(String s) {

		s = s.trim(); // get rid of possible spaces at the end or beginin of the
						// string
		String[] arr = s.split(" ");

		double[] doubleArray = new double[arr.length];

		for (int i = 0; i < arr.length; i++) {
			doubleArray[i] = Double.parseDouble(arr[i]);
		}
		return doubleArray;

	}

	/**
	 * 
	 * @param A
	 *            main matrix
	 * @param basicVariables
	 *            list of basic variables
	 * @return the basic matrix
	 */
	private static double[][] findBase(double[][] A, int[] basicVariables) {

		int a = A.length;
		int b = basicVariables.length;

		double[][] base = new double[a][b];

		for (int i = 0; i < a; i++) {
			for (int j = 0; j < b; j++) {
				base[i][j] = A[i][basicVariables[j] - 1];

			}

		}

		return base;

	}

	private static double[][] findNotBase(double[][] A, int[] basicVariables) {

		ArrayList<Integer> arr = new ArrayList<Integer>();

		for (int j = 1; j <= A[0].length; j++) {
			if (Arrays.binarySearch(basicVariables, j) < 0) {
				arr.add(j);
			}
		}

		int[] notBaseVariables = new int[arr.size()];
		for (int j = 0; j < arr.size(); j++) {
			notBaseVariables[j] = arr.get(j);
		}

		return findBase(A, notBaseVariables);

	}


	private static double[][] sub(double[][] first, double[][] second) {

		int x1 = first.length, y1 = first[0].length;
		int x2 = second.length, y2 = second[0].length;

		if (x1 != x2 || y1 != y2) {
			System.err.println("subtraction cant be done!");
		}

		double[][] result = new double[x1][y1];

		for (int i = 0; i < x1; i++) {
			for (int j = 0; j < y1; j++) {
				// System.out.println("first[i][j]: " + first[i][j] + "
				// second[i][j]" + second[i][j]);
				result[i][j] = first[i][j] - second[i][j];
			}
		}

		return result;
	}
	
	
	public static void round(double[][] matrix, int places) {
	    if (places < 0)
	    	throw new IllegalArgumentException();
	    int rLength = matrix.length;
		int cLength = matrix[0].length;
		
		for(int i=0; i<rLength; i++){
			for(int j=0; j<cLength; j++){
				 BigDecimal bd = new BigDecimal(matrix[i][j]);
				   bd = bd.setScale(places, RoundingMode.HALF_UP);
				   matrix[i][j] = bd.doubleValue();
			}
		}
		
	   
	}

	
}