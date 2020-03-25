package project2;



import java.io.File;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Locale;
import java.util.Scanner;

import Jama.Matrix;

public class TheMain{

	public static void main(String[] args) {

		int n = 0, m = 0;
		String cTString = "";
		double[][] cT = new double[1][1];

		try {

			File input = new File("input.txt");
			Scanner reader = new Scanner(input).useLocale(Locale.US);
			PrintStream out1 = new PrintStream(new File("out ini.txt"));
			//PrintStream out2 = new PrintStream(new File("out opt.txt"));

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

			double[][] row0 = new double[1][cT[0].length];

			for (int i = 0; i < cT[0].length; i++) {

				row0[0][i] = (-1) * cT[0][i];

			}

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

			reader.close();

			// -----------------------------------------------INPUT
			// COMPLETE------------------------------------------------

			int[] basicVarIndexes = new int[m]; // initilaze an array to hold
												// basic variables

			// find initial basic variablesINDEXES
			findBasicVarFromTable(matrixA, basicVarIndexes);

			double[][] thebase;
			double[][] theNotbase;
			Matrix theBaseMatrixInv;
			Matrix inv_BN;
			double[][] cBT;
			Matrix cBTMatrix;
			Matrix cBTinv_BN;
			double[][] cNT;
			Matrix inv_Bb;
			Matrix cBTinv_BNminuscNT;
			Matrix initialMatrix = Matrix.constructWithCopy(matrixA);

			// -----------------------------------------------CALCULATIONS------------------------------------

			thebase = findBase(matrixA, basicVarIndexes);

			theNotbase = findNotBase(matrixA, basicVarIndexes);

			// B^-1
			theBaseMatrixInv = Matrix.constructWithCopy(thebase).inverse();

			// B^-1 * N
			inv_BN = theBaseMatrixInv.times(Matrix.constructWithCopy(theNotbase));

			cBT = findBase(cT, basicVarIndexes);

			// cBT
			cBTMatrix = Matrix.constructWithCopy(cBT);

			// cBT * -B * N
			cBTinv_BN = cBTMatrix.times(inv_BN);

			cNT = findNotBase(cT, basicVarIndexes);

			// B^-1 * b
			inv_Bb = theBaseMatrixInv.times(Matrix.constructWithCopy(vectorB));

			cBTinv_BNminuscNT = cBTinv_BN.minus(Matrix.constructWithCopy(cNT));

			System.out.println(Arrays.toString(basicVarIndexes));

			System.out.println(Arrays.toString(basicVarIndexes));

			boolean first = true;

			while (!isMaximized(cBTinv_BNminuscNT.getArray())) {

				if (first) {
					refreshBasicVars(basicVarIndexes, matrixA, findNotBasicVarIndexes(matrixA, basicVarIndexes),
							vectorB, cBTinv_BNminuscNT.getArray());
					first = false;
				}

				refreshBasicVars(basicVarIndexes, theBaseMatrixInv.times(initialMatrix).getArray(),
						findNotBasicVarIndexes(matrixA, basicVarIndexes), inv_Bb.getArray(),
						cBTinv_BNminuscNT.getArray());

				thebase = findBase(matrixA, basicVarIndexes);

				theNotbase = findNotBase(matrixA, basicVarIndexes);

				// B^-1
				theBaseMatrixInv = Matrix.constructWithCopy(thebase).inverse();

				// B^-1 * N
				inv_BN = theBaseMatrixInv.times(Matrix.constructWithCopy(theNotbase));

				cBT = findBase(cT, basicVarIndexes);

				cBTMatrix = Matrix.constructWithCopy(cBT); // cBT

				// cBT * B^-1 * N
				cBTinv_BN = cBTMatrix.times(inv_BN);

				cNT = findNotBase(cT, basicVarIndexes);

				// B^-1 * b
				inv_Bb = theBaseMatrixInv.times(Matrix.constructWithCopy(vectorB));

				// cBT * B^-1 * N - cNT
				cBTinv_BNminuscNT = cBTinv_BN.minus(Matrix.constructWithCopy(cNT));

				System.out.println(Arrays.toString(basicVarIndexes));

			}

			System.out.println("final status:");

			System.out.println("basic vars:");

			System.out.println(Arrays.toString(basicVarIndexes));

			double[][] notBase = cBTinv_BNminuscNT.getArray();
			for (int i = 0; i < notBase[0].length; i++) {
				System.out.print(notBase[0][i] + " \t");
			}
			System.out.println("\n");

			System.out.println("rhs");

			for (int i = 0; i < inv_Bb.getArray().length; i++) {
				System.out.println(inv_Bb.getArray()[i][0]);
			}

			///////////////// ----------------PRINT
			///////////////// OUT-----------------/////////////////////////
			
			
			///------------print initial-----------

			out1.print("Row\tZ\t");
			
			for (int i = 01; i <= n; i++) {
				out1.print("x" + i + "\t");
			
			}
			out1.println("RHS");
			
			out1.println("------------------------------------------------------------");
			out1.print("0\t1\t");
			
			for (int i = 0; i < n; i++) {
				if(row0[0][i]!=0)
					out1.print(row0[0][i] + "\t");
				else
					out1.print(-1*row0[0][i] + "\t");
			}
			
			out1.print(0);
			
			out1.println();
			out1.println("------------------------------------------------------------");
			
			for (int i = 0; i < m; i++) {
				out1.print(i+1 + "\t0\t");
				for (int j = 0; j < n; j++) {
		
					out1.print(matrixA[i][j] + "\t");
				}
				out1.print(vectorB[i][0] + "\t");
				//out1.print(inv_Bb.get(i, 0) + "\t\t");
				out1.println();
			}
			
			out1.println("------------------------------------------------------------");
			
			out1.flush();
			out1.close();
			
			out1 = new PrintStream(new File("out opt.txt"));
			
			
			///-----------------------------------------------------print optimized-----------
			
			
			out1.print("Row\tZ\t");
			
			for (int i = 01; i <= n; i++) {
				out1.print("x" + i + "\t");
			
			}
			out1.println("RHS");
			
			out1.println("------------------------------------------------------------");
			out1.print("0\t1\t");
			
			int index = 0;
			
			for (int i = 0; i < n; i++) {
				if (arrayContaines(basicVarIndexes, i)) {
					out1.print("0\t");
				} else {
					round(cBTinv_BNminuscNT,1);
					out1.print(cBTinv_BNminuscNT.get(0, index) + "\t");
					index++;
				}
			}
			Matrix cBTMatrix_times_inv_Bb = cBTMatrix.times(inv_Bb);
			round(cBTMatrix_times_inv_Bb, 1);
			out1.println(cBTMatrix_times_inv_Bb.get(0, 0));
			out1.println("------------------------------------------------------------");
			
			Matrix currentTablo = theBaseMatrixInv.times(initialMatrix);
			
			for (int i = 0; i < m; i++) {
				out1.print(i+1 + "\t0\t");
				for (int j = 0; j < n; j++) {
					round(currentTablo, 1);
					out1.print(currentTablo.get(i,j) + "\t");
				}
				round(inv_Bb, 1);
				out1.print(inv_Bb.get(i, 0) + "\t");
				//out1.print(inv_Bb.get(i, 0) + "\t\t");
				out1.println();
			}
			
			out1.println("------------------------------------------------------------");
			

		reader.close();

		} catch (Exception e) {
			e.printStackTrace();
			System.err.println("full name of the input file must be input.txt and it has to be in the project folder");

		}

	}

	private static void findBasicVarFromTable(double[][] table, int[] basicVarIndexes) {
		int index = 0;
		for (int i = 0; i < table.length; i++) {
			for (int j = 0; j < table[0].length; j++) {
				if (Math.abs(1.0 - table[i][j]) < 0.01) {
					if (doesColumnContainAllZeros(table, i, j)) {
						basicVarIndexes[index] = j;
						index++;
					}
				}
				// System.out.print(table[i][j] + "\t");
			}
			// System.out.println();
		}

	}

	private static boolean doesColumnContainAllZeros(double[][] table, int row, int column) {
		for (int i = 0; i < table.length; i++) {
			if (i != row && Math.abs(table[i][column]) > 0.001) {
				return false;
			}
		}
		return true;
	}

	private static boolean isMaximized(double[][] notBase) {

		System.out.println("row0");
		for (int i = 0; i < notBase[0].length; i++) {
			System.out.print(notBase[0][i] + " \t");
		}
		System.out.println("\n");
		for (int i = 0; i < notBase[0].length; i++) {
			if (notBase[0][i] < 0) {
				return false;
			}
		}

		return true;
	}

	private static void refreshBasicVars(int[] basicVarsIndexes, double[][] matrix, int[] notBasicVarsIndexes,
			double[][] vectorB, double[][] cBTinvBNminuscNT) {
		double[][] x = vectorB;
		for (int i = 0; i < x.length; i++) {
			for (int j = 0; j < x[0].length; j++) {
				System.out.print(x[i][j] + "\t");
			}
			System.out.println();
		}

		int enters = findEnteringVarIndex(notBasicVarsIndexes, cBTinvBNminuscNT);
		int leaves = findLeavingVarIndex(matrix, notBasicVarsIndexes, vectorB, enters);
		System.out.println("enters " + enters);
		System.out.println("leaves " + basicVarsIndexes[leaves]);

		basicVarsIndexes[leaves] = enters;

	}

	private static int findLeavingVarIndex(double[][] matrix, int[] notBasicVarsIndexes, double[][] vectorB,
			int column) {

		int row = 0;
		double min = 9999999; // vectorB[0][0] / matrix[0][column];
		System.out.println("ratio " + vectorB[0][0] / matrix[0][column]);
		for (int i = 0; i < matrix.length; i++) {
			if (vectorB[i][0] / matrix[i][column] < min && vectorB[i][0] / matrix[i][column] > 0) {
				min = vectorB[i][0] / matrix[i][column];
				row = i;
			}
		}
		System.out.println("row" + row);
		return row;
	}

	private static int findEnteringVarIndex(int[] notBasicVarsIndexes, double[][] notBasicVariables) {

		int index = 0;
		double min = notBasicVariables[0][0];
		for (int i = 1; i < notBasicVariables[0].length; i++) {

			if (notBasicVariables[0][i] < min) {
				min = notBasicVariables[0][i];
				index = i;
			}

		}
		// System.out.println("notBasicVarsIndexes[index]" +
		// notBasicVarsIndexes[index]);
		return notBasicVarsIndexes[index];
	}

	/**
	 * 
	 * 
	 * @param s
	 *            contains integers separated by one space
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

	private static boolean arrayContaines(int[] array, int key) {
		for (int n : array) {
			if (n == key)
				return true;
		}
		return false;
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
				base[i][j] = A[i][basicVariables[j]];

			}

		}

		return base;

	}

	private static int[] findNotBasicVarIndexes(double[][] A, int[] basicVariablesIndexes) {

		ArrayList<Integer> arr = new ArrayList<Integer>();

		for (int j = 0; j < A[0].length; j++) { // Caution limits
			if (!arrayContaines(basicVariablesIndexes, j)) {
				arr.add(j);
				// System.out.println(j);
			}
		}

		int[] notBaseVariables = new int[arr.size()];
		for (int j = 0; j < arr.size(); j++) {
			notBaseVariables[j] = arr.get(j);
		}

		return notBaseVariables;

	}
	
	
	/**
	 * 
	 * @param A 
	 * 		the tablo
	 * @param basicVariablesIndexes
	 * 		indexes of basic variables
	 * 
	 * @return	returns N (not base columns of the tablo)
	 */

	private static double[][] findNotBase(double[][] A, int[] basicVariablesIndexes) {

		int[] notBaseVariablesIndexes = findNotBasicVarIndexes(A, basicVariablesIndexes);

		return findBase(A, notBaseVariablesIndexes);

	}

	public static void round(Matrix _matrix, int places) {
		double[][] matrix = _matrix.getArray();
		if (places < 0)
			throw new IllegalArgumentException();
		int rLength = matrix.length;
		int cLength = matrix[0].length;

		for (int i = 0; i < rLength; i++) {
			for (int j = 0; j < cLength; j++) {
				BigDecimal bd = new BigDecimal(matrix[i][j]);
				bd = bd.setScale(places, RoundingMode.HALF_UP);
				matrix[i][j] = bd.doubleValue();
			}
		}
		_matrix = Matrix.constructWithCopy(matrix);

	}

}