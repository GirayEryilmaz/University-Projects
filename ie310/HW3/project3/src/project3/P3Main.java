package project3;

import java.io.File;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Locale;
import java.util.Scanner;

import Jama.Matrix;

public class  P3Main{
	static int[] artVariables;

	public static void main(String[] args) {

		int n = 0, m = 0;
		String type = "";
		String cTString1 = "";
		String cTString2 = "";

		double[][] cT1 = new double[1][1]; // phase1
		double[][] cT2 = new double[1][1]; // phase2

		try {

			File input = new File("input.txt");
			Scanner scanner = new Scanner(input);
			Scanner reader = scanner.useLocale(Locale.US);
			PrintStream out1 = new PrintStream(new File("out1ini.txt"));
			// PrintStream out2 = new PrintStream(new File("out opt.txt"));

			reader.nextLine();
			type = reader.nextLine();
			reader.nextLine();
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

			cTString1 = reader.nextLine(); // get vector c transpose as a line
											// did not get the numbers to an
											// array by one by because
											// number of elements is not known
											// in advance

			cT1[0] = parse(cTString1); // the string is parsed to an array of
										// doubles
			reader.nextLine();
			reader.nextLine();

			cTString2 = reader.nextLine(); // get vector c transpose as a line
											// did not get the numbers to an
											// array by one by because
											// number of elements is not known
											// in advance

			cT2[0] = parse(cTString2); // the string is parsed to an array of
										// doubles
			
			
			if(type.toLowerCase().contains("min")){
				for(int i =0 ; i < cT2[0].length; i++){
					cT2[0][i] = cT2[0][i] * (-1);
					
				}
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
			double[][] cTinitial = new double[1][n]; // initial

			artVariables = new int[n - 2 * m];
			int index_ = 0;
			for (int i = 0; i < n; i++) {
				if (cT1[0][i] != 0) {
					artVariables[index_] = i;
					index_++;
				}
			}

			for (int i = 0; i < n; i++)
				cTinitial[0][i] = cT1[0][i];

			double initialRHS = 0;

			for (int i = 0; i < artVariables.length; i++) {
				for (int j = 0; j < n; j++) {
					cTinitial[0][j] += matrixA[n - artVariables[i]][j];
				}
				initialRHS -= vectorB[n - artVariables[i]][0];
			}

			// for(int i=0; i<cTinitial[0].length; i++){
			// System.out.print(cTinitial[0][i] + " ");
			// }

			double[][] row0 = new double[1][cTinitial[0].length];

			for (int i = 0; i < cTinitial[0].length; i++) {
				row0[0][i] = (-1) * cTinitial[0][i];
			}
			reader.close();
			scanner.close();

			// -----------------------------------------------INPUT
			// COMPLETE------------------------------------------------

			int[] basicVarIndexes = new int[m]; // initilaze an array to hold
												// basic variables

			// find initial basic variablesINDEXES
			findBasicVarFromTable(matrixA, basicVarIndexes);

			// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			// ------------------------INITIAL
			// TABLE--------------------------------//
			out1.print("Row\tZ\t");

			for (int i = 01; i <= n; i++) {
				out1.print("x" + i + "\t");

			}

			out1.print("RHS\t");
			out1.println("Basic Variables");

			out1.println("------------------------------------------------------------");
			out1.print("0\t1\t");

			for (int i = 0; i < n; i++) {
				if (row0[0][i] != 0)
					out1.print(row0[0][i] + "\t");
				else
					out1.print(-1 * row0[0][i] + "\t");
			}
			out1.print(initialRHS + "\t");
			out1.print("z");

			out1.println();
			out1.println("------------------------------------------------------------");

			for (int i = 0; i < m; i++) {
				out1.print(i + 1 + "\t0\t");
				for (int j = 0; j < n; j++) {
					out1.print(matrixA[i][j] + "\t");
				}
				out1.print(vectorB[i][0] + "\t");
				out1.print("x" + (basicVarIndexes[i] + 1));
				out1.println();
			}

			out1.println("------------------------------------------------------------");

			out1.flush();
			out1.close();
			// -----------------------------COMPLETE---------------------------------------
			// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

			cBT = findBase(cTinitial, basicVarIndexes);

			// cBT
			cBTMatrix = Matrix.constructWithCopy(cBT);

			// cBT * -B * N
			cBTinv_BN = cBTMatrix.times(inv_BN);

			cNT = findNotBase(cTinitial, basicVarIndexes);

			// B^-1 * b
			inv_Bb = theBaseMatrixInv.times(Matrix.constructWithCopy(vectorB));

			cBTinv_BNminuscNT = cBTinv_BN.minus(Matrix.constructWithCopy(cNT));

			// System.out.println(Arrays.toString(basicVarIndexes));

			boolean first = true;

			while (!isMaximized(cBTinv_BNminuscNT.getArray()) && areArtVarIn(basicVarIndexes)) {

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

				cBT = findBase(cTinitial, basicVarIndexes);

				cBTMatrix = Matrix.constructWithCopy(cBT); // cBT

				// cBT * B^-1 * N
				cBTinv_BN = cBTMatrix.times(inv_BN);

				cNT = findNotBase(cTinitial, basicVarIndexes);

				// B^-1 * b
				inv_Bb = theBaseMatrixInv.times(Matrix.constructWithCopy(vectorB));

				// cBT * B^-1 * N - cNT
				cBTinv_BNminuscNT = cBTinv_BN.minus(Matrix.constructWithCopy(cNT));

			}

		
			//
			//System.out.println("final status of phase 1 :");

			//System.out.println(Arrays.toString(basicVarIndexes));

			//
			// System.out.println("basic vars:");
			//
			// System.out.println(Arrays.toString(basicVarIndexes));
			
//			if (areArtVarIn(basicVarIndexes)) {
//				throw new Exception("the initila problem is infeaseble");
//			}

			///////////////// ----------------PRINT
			///////////////// OUT-----------------/////////////////////////
			// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			/// -----------------------------------------------------print
			/// optimized-----------
			out1 = new PrintStream(new File("out1opt.txt"));
			Matrix cBTMatrix_times_inv_Bb = cBTMatrix.times(inv_Bb);
			if (cBTMatrix_times_inv_Bb.get(0, 0) + initialRHS != 0)
				out1.println("No feasible solution");
			else {
				double[][] matrixA2 = new double[m][n - artVariables.length];
				double[][] vectorB2 = new double[m][1];
				out1.print("Row\tZ\t");

				for (int i = 01; i <= n; i++) {
					out1.print("x" + i + "\t");

				}
				out1.print("RHS\t");
				out1.println("Basic Variables");

				out1.println("------------------------------------------------------------");
				out1.print("0\t1\t");

				int index = 0;

				for (int i = 0; i < n; i++) {
					if (arrayContaines(basicVarIndexes, i)) {
						out1.print("0\t");
					} else {
						round(cBTinv_BNminuscNT, 1);
						out1.print(cBTinv_BNminuscNT.get(0, index) + "\t");
						index++;
					}
				}

				round(cBTMatrix_times_inv_Bb, 1);
				out1.print((cBTMatrix_times_inv_Bb.get(0, 0) + initialRHS) + "\t");
				out1.println("z");
				out1.println("------------------------------------------------------------");

				Matrix currentTablo = theBaseMatrixInv.times(initialMatrix);

				matrixA2 = Matrix.constructWithCopy(currentTablo.getArray()).getArray();
				//System.out.println(Arrays.toString(artVariables));
				//for (int i = 0; i < m; i++)
					//System.out.println(Arrays.toString(matrixA2[i]));

				for (int i = 0; i < m; i++) {
					out1.print(i + 1 + "\t0\t");
					for (int j = 0; j < n; j++) {
						matrixA2[i][j] = currentTablo.get(i, j);
						round(currentTablo, 1);
						out1.print(currentTablo.get(i, j) + "\t");
					}
					vectorB2[i][0] = inv_Bb.get(i, 0);
					round(inv_Bb, 1);
					out1.print(inv_Bb.get(i, 0) + "\t");
					out1.print("x" + (basicVarIndexes[i] + 1));
					// out1.print(inv_Bb.get(i, 0) + "\t\t");
					out1.println();
				}

				out1.println("------------------------------------------------------------");
				out1.flush();
				out1.close();

				// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PHASE 2
				// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				out1 = new PrintStream(new File("out2ini.txt"));

				double phase2RHS = 0;

				double[][] cTPhase2 = new double[1][n];

				for (int i = 0; i < n; i++) {
					cTPhase2[0][i] = cT2[0][i];
				}
				int index__ = 0;
				for (int i = 0; i < basicVarIndexes.length; i++) {
					for (int j = 0; j < n; j++) {
						if (basicVarIndexes[i] == j) {
							double ratio = cT2[0][j];
							for (int k = 0; k < n; k++) {
								cTPhase2[0][k] += ((-ratio) * currentTablo.get(index__, k));
							}
							phase2RHS += (ratio) * inv_Bb.get(index__, 0);
						}
					}
					index__++;
				}
				// for(int i=0; i<cTPhase2[0].length; i++)
				// System.out.print(cTPhase2[0][i] + " ");

				out1.print("Row\tZ\t");

				for (int i = 01; i <= n; i++) {
					out1.print("x" + i + "\t");

				}
				out1.print("RHS\t");
				out1.println("Basic Variables");

				out1.println("------------------------------------------------------------");
				out1.print("0\t1\t");

				for (int i = 0; i < n; i++) {
					if (cTPhase2[0][i] != 0)
						out1.print(-cTPhase2[0][i] + "\t");
					else
						out1.print(cTPhase2[0][i] + "\t");
				}

				round(cBTMatrix_times_inv_Bb, 1);
				out1.print(phase2RHS + "\t");
				out1.println("z");
				out1.println("------------------------------------------------------------");

				for (int i = 0; i < m; i++) {
					out1.print(i + 1 + "\t0\t");
					for (int j = 0; j < n; j++) {

						// round(currentTablo, 1);
						out1.print(currentTablo.get(i, j) + "\t");
					}
					// round(inv_Bb, 1);
					out1.print(inv_Bb.get(i, 0) + "\t");
					out1.print("x" + (basicVarIndexes[i] + 1));
					// out1.print(inv_Bb.get(i, 0) + "\t\t");
					out1.println();
				}

				out1.println("------------------------------------------------------------");
				out1.flush();
				out1.close();
				// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//				for (int i = 0; i < basicVarIndexes.length; i++)
//					System.out.print(basicVarIndexes[i] + " ");

				double[][] thebase2;
				double[][] theNotbase2;
				Matrix theBaseMatrixInv2;
				Matrix inv_BN2;
				double[][] cBT2;
				Matrix cBTMatrix2;
				Matrix cBTinv_BN2;
				double[][] cNT2;
				Matrix inv_Bb2;
				Matrix cBTinv_BNminuscNT2;
				Matrix initialMatrix2 = Matrix.constructWithCopy(matrixA2);
				for (int i = 0; i < cTPhase2[0].length; i++) {
					row0[0][i] = (-1) * cTPhase2[0][i];
				}

//				for (int i = 0; i < vectorB2.length; i++) {
//					System.out.println(vectorB2[i][0]);
//				}

				// -----------------------------------------------PHASE2
				// CALCULATIONS------------------------------------

				// get rid of art. var.
				double[][] temp = new double[m][n];
				//
				// for(int i = 0, next =0 ; i < m ; i++, next = 0){
				// for(int j = 0 ; j < n ; j++){
				// if(!arrayContaines(artVariables, j)){
				// temp[i][j] = matrixA2[i][j];
				// //next++;
				// }else{
				// temp[i][j] = 0;
				// }
				// }
				//
				// }

				for (int i = 0; i < m; i++) {
					for (int j = 0; j < n; j++) {
						if (!arrayContaines(artVariables, j)) {
							temp[i][j] = matrixA2[i][j];
							// next++;
						} else {
							temp[i][j] = 0;
						}
					}

				}

				matrixA2 = temp;

				thebase2 = findBase(matrixA2, basicVarIndexes);

				theNotbase2 = findNotBase(matrixA2, basicVarIndexes);

				// B^-1
				theBaseMatrixInv2 = Matrix.constructWithCopy(thebase2).inverse();

				// B^-1 * N
				inv_BN2 = theBaseMatrixInv2.times(Matrix.constructWithCopy(theNotbase2));

				cBT2 = findBase(cTPhase2, basicVarIndexes);

				// cBT
				cBTMatrix2 = Matrix.constructWithCopy(cBT2);

				// cBT * -B * N
				cBTinv_BN2 = cBTMatrix2.times(inv_BN2);

				cNT2 = findNotBase(cTPhase2, basicVarIndexes);

				// B^-1 * b
				inv_Bb2 = theBaseMatrixInv2.times(Matrix.constructWithCopy(vectorB2));

				cBTinv_BNminuscNT2 = cBTinv_BN2.minus(Matrix.constructWithCopy(cNT2));

//				System.out.println("hey" + Arrays.toString(basicVarIndexes));
//				refreshBasicVars(basicVarIndexes, matrixA2, findNotBasicVarIndexes(matrixA2, basicVarIndexes), vectorB2,
//						cBTinv_BNminuscNT2.getArray());

//				System.out.println("heyoo" + Arrays.toString(basicVarIndexes));

				boolean second = true;

				while (!isMaximized(cBTinv_BNminuscNT2.getArray())) {
					//System.out.println("aa");
					if (second) {
						refreshBasicVars(basicVarIndexes, matrixA2, findNotBasicVarIndexes(matrixA2, basicVarIndexes),
								vectorB2, cBTinv_BNminuscNT2.getArray());
						second = false;
					}

					refreshBasicVars(basicVarIndexes, theBaseMatrixInv2.times(initialMatrix2).getArray(),
							findNotBasicVarIndexes(matrixA2, basicVarIndexes), inv_Bb2.getArray(),
							cBTinv_BNminuscNT2.getArray());

					thebase2 = findBase(matrixA2, basicVarIndexes);

					theNotbase2 = findNotBase(matrixA2, basicVarIndexes);

					// B^-1
					theBaseMatrixInv2 = Matrix.constructWithCopy(thebase2).inverse();

					// B^-1 * N
					inv_BN2 = theBaseMatrixInv2.times(Matrix.constructWithCopy(theNotbase2));

					cBT2 = findBase(cTPhase2, basicVarIndexes);

					cBTMatrix2 = Matrix.constructWithCopy(cBT2); // cBT

					// cBT * B^-1 * N
					cBTinv_BN2 = cBTMatrix2.times(inv_BN2);

					cNT2 = findNotBase(cTPhase2, basicVarIndexes);

					// B^-1 * b
					inv_Bb2 = theBaseMatrixInv2.times(Matrix.constructWithCopy(vectorB2));

					// cBT * B^-1 * N - cNT
					cBTinv_BNminuscNT2 = cBTinv_BN2.minus(Matrix.constructWithCopy(cNT2));

				}

				cBTMatrix_times_inv_Bb = cBTMatrix2.times(inv_Bb2);
				currentTablo = theBaseMatrixInv2.times(initialMatrix2);
				out1 = new PrintStream(new File("out2opt.txt"));
				out1.print("Row\tZ\t");

				for (int i = 01; i <= n; i++) {
					out1.print("x" + i + "\t");

				}
				out1.print("RHS\t");
				out1.println("Basic Variables");

				out1.println("------------------------------------------------------------");
				out1.print("0\t1\t");
				
				int indexxx=0;
				for (int i = 0; i < n; i++) {
					if (arrayContaines(basicVarIndexes, i)) {
						out1.print("0\t");
					} else {
						round(cBTinv_BNminuscNT,1);
						out1.print(cBTinv_BNminuscNT2.get(0, indexxx) + "\t");
						indexxx++;
					}
				}

//				for (int i = 0; i < n; i++) {
//					out1.print(row0[0][i] + "\t");
//
//				}

				round(cBTMatrix_times_inv_Bb, 1);
				out1.print(phase2RHS + cBTMatrix_times_inv_Bb.get(0, 0)+ "\t");
				out1.println("z");
				out1.println("------------------------------------------------------------");

				for (int i = 0; i < m; i++) {
					out1.print(i + 1 + "\t0\t");
					for (int j = 0; j < n; j++) {

						round(currentTablo, 1);
						out1.print(currentTablo.get(i, j) + "\t");
					}
					round(inv_Bb, 1);
					out1.print(inv_Bb2.get(i, 0) + "\t");
					out1.print("x" + (basicVarIndexes[i] + 1));
					// out1.print(inv_Bb.get(i, 0) + "\t\t");
					out1.println();
				}

				out1.println("------------------------------------------------------------");
				out1.flush();
				out1.close();

				int[] NBV = findNotBasicVarIndexes(matrixA2, basicVarIndexes);

				// System.out.println(Arrays.toString(NBV));
				// System.out.println(Arrays.toString(basicVarIndexes));
				//
				for (int i = 0; i < n; i++) {
					if (arrayContaines(NBV, i) && row0[0][i] == 0 && !arrayContaines(artVariables, i)) {
						System.out.println("multiple optima!");
						//System.out.println(i);
					}
				}
			}

		} catch (Exception e) {
			if (e instanceof UnsupportedOperationException && e.getMessage().equals("unbounded")) {
				System.out.println("unbounded");

			} else {
				e.printStackTrace();
				System.err.println(
						"full name of the input file must be input.txt and it has to be in the project folder");
			}

		}

	}

	private static boolean areArtVarIn(int[] basicVarIndexes) {
		for (int i = 0; i < artVariables.length; i++) {
			if (arrayContaines(basicVarIndexes, artVariables[i])) {
				return true;
			}
		}
		return false;
	}

	/**
	 * find the basic variables from given table by searching for columns that
	 * contain one '1' and zeros all the rest
	 * 
	 * @param table
	 *            initial table (matrixA)
	 * 
	 * @param basicVarIndexes
	 *            the array that will hold indexes of basic variables for
	 *            instance 0 means x1, 1 means x2 etc.
	 */
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

	/**
	 * helper function of findBasicVarFromTable
	 * 
	 * @param table
	 *            the matrix
	 * @param row
	 *            the row that holds '1' at given column
	 * @param column
	 *            the column that is possible belong to a basic variable
	 * @return true if the implied column of the given table contains all zeros
	 *         except the given row
	 */

	private static boolean doesColumnContainAllZeros(double[][] table, int row, int column) {
		for (int i = 0; i < table.length; i++) {
			if (i != row && Math.abs(table[i][column]) > 0.001) {
				return false;
			}
		}
		return true;
	}

	/**
	 * 
	 * @param notBase
	 *            the matrix that consists of the columns which hold non basic
	 *            variables'
	 * @return true if the table that owns these non basic variables is
	 *         maximized
	 */

	private static boolean isMaximized(double[][] notBase) {

		// System.out.println("row0");
		// for (int i = 0; i < notBase[0].length; i++) {
		// System.out.print(notBase[0][i] + " \t");
		// }
		// System.out.println("\n");

		for (int i = 0; i < notBase[0].length; i++) {
			if (notBase[0][i] < 0)
				return false;
		}

		return true;
	}

	/**
	 * 
	 * finds which variables goes into plan and which goes out, refreshes the
	 * indexes of basic variables array
	 * 
	 * @param basicVarsIndexes
	 *            indexes of basic variables in the table
	 * 
	 * @param matrix
	 *            the table
	 * @param notBasicVarsIndexes
	 *            indexes of non basic variables in the table
	 * @param vectorB
	 *            (rhs) right hand side coefficients
	 * @param cBTinvBNminuscNT
	 */

	private static void refreshBasicVars(int[] basicVarsIndexes, double[][] matrix, int[] notBasicVarsIndexes,
			double[][] vectorB, double[][] cBTinvBNminuscNT) {

		// double[][] x = vectorB;
		// for (int i = 0; i < x.length; i++) {
		// for (int j = 0; j < x[0].length; j++) {
		// System.out.print(x[i][j] + "\t");
		// }
		// System.out.println();
		// }

		int enters = findEnteringVarIndex(notBasicVarsIndexes, cBTinvBNminuscNT);
		int IndexOfLeavingVar = findLeavingVarIndex(matrix, vectorB, enters);

		// System.out.println("enters " + enters);
		// System.out.println("leaves " + basicVarsIndexes[IndexOfLeavingVar]);

		basicVarsIndexes[IndexOfLeavingVar] = enters;

	}

	/**
	 * 
	 * @param matrix
	 *            the matrixA
	 * @param vectorB
	 *            rhs
	 * @param column
	 *            index of the column of entering variable
	 * @return index of leaving variable in the basicVarsIndexes array
	 * 
	 *         example returns 3, if 4th element of basicVarsIndexes will no
	 *         longer be a basic variable which will be replaced by entering
	 *         variable
	 */

	private static int findLeavingVarIndex(double[][] matrix, double[][] vectorB, int column) {

		int row = 0;
		double min = 9999999; // vectorB[0][0] / matrix[0][column];
		// System.out.println("ratio " + vectorB[0][0] / matrix[0][column]);
		for (int i = 0; i < matrix.length; i++) {
			if (vectorB[i][0] / matrix[i][column] < min && vectorB[i][0] / matrix[i][column] > 0
					&& matrix[i][column] != 0) {
				min = vectorB[i][0] / matrix[i][column];
				row = i;
			}
		}

		if (min == 9999999) {
			throw new UnsupportedOperationException("unbounded");
		}

		return row;
	}

	/**
	 * 
	 * @param notBasicVarsIndexes
	 * @param notBasicVariables
	 * @return returns the name of entering variable (name means index of
	 *         variable at main table example: 0 means x1 etc.)
	 */
	private static int findEnteringVarIndex(int[] notBasicVarsIndexes, double[][] notBasicVariables) {

		int index = 0;
		double min = notBasicVariables[0][0];
		for (int i = 1; i < notBasicVariables[0].length; i++) {

			if (notBasicVariables[0][i] < min) {
				min = notBasicVariables[0][i];
				index = i;
			}

		}

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

	/**
	 * 
	 * @param array
	 *            the array to search
	 * @param key
	 *            the element to search in the array
	 * @return true if array contains the element (key)
	 * 
	 */

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

	/**
	 * 
	 * @param A
	 *            the matrixA
	 * @param basicVariablesIndexes
	 *            array holds indexes (names) of basic variables
	 * @return array hold the names of variables that are not basic
	 */

	private static int[] findNotBasicVarIndexes(double[][] A, int[] basicVariablesIndexes) {

		ArrayList<Integer> arr = new ArrayList<Integer>();

		for (int j = 0; j < A[0].length; j++) {
			if (!arrayContaines(basicVariablesIndexes, j)) {
				arr.add(j);
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
	 *            the tablo
	 * @param basicVariablesIndexes
	 *            indexes of basic variables
	 * 
	 * @return returns N (not base columns of the tablo)
	 */

	private static double[][] findNotBase(double[][] A, int[] basicVariablesIndexes) {

		int[] notBaseVariablesIndexes = findNotBasicVarIndexes(A, basicVariablesIndexes);

		return findBase(A, notBaseVariablesIndexes);

	}

	/**
	 * rounds all numbers of given matrix to given number of places after
	 * decimal, actually manipulating original matrix
	 * 
	 * @param _matrix
	 * @param places
	 */

	public static void round(Matrix _matrix, int places) {
		double[][] matrix = _matrix.getArray();
		places++;
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