package strgmngr;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Scanner;

public class SystemCatalog {

	File sysCat;
	ArrayList<Type> types = new ArrayList<Type>();
	private final String DBname = "simpleDB";
	private int numOfTypes = 0;
	private final int maxLenofTypeName = 100;
	private final int numOfRecsPerPage = 10;
	private final int maxFieldSize = 32;

	public SystemCatalog() throws IOException {

		sysCat = new File("SystemCatalog");

		if (sysCat.exists()) {

			Scanner reader = new Scanner(sysCat);

			String s;
			String[] arr;

			reader.nextLine(); // header

			/*
			 * read types
			 * 
			 */
			while (reader.hasNextLine()) {
				s = reader.nextLine();

				arr = s.split(" ");
				// System.out.println(Arrays.toString(arr));
				addRead(new Type(arr[0], Arrays.copyOfRange(arr, 1, arr.length)));

			}

			reader.close();

		} else {

			try {

				PrintStream ps = new PrintStream(sysCat);
				ps.println("simpleDB 0 100 10 32");
				// nameOfDB #ofRecords max#ofTypes maxLenofTypeName
				// #ofRecPerPage maxFieldSize(bits)

				ps.close();

			} catch (FileNotFoundException e) {

				System.out.println("bang!");
				e.printStackTrace();

			}
		}

	}
/**
 * read type from file and add to SystemCatalog
 * @param nT new type
 */
	private void addRead(Type nT) {
		types.add(nT);
		numOfTypes++;
	}
	
	/**
	 * add type manually
	 * @param nT new type
	 */

	void add(Type nT) {
		int index = Collections.binarySearch(types, nT);

		if (index >= 0) {
			System.out.println("type \"" + nT.name + "\" allready exists!");
			return;
		}

		// System.out.println(-1 * (Collections.binarySearch(types, nT)+1));
		types.add(-1 * (index + 1), nT);
		numOfTypes++;

	}
	
/**
 * remove the Type with given name from system
 * @param name  of type to be removed
 * @throws IOException 
 */
	void remove(String name) throws IOException {
		int index = types.indexOf(new Type(name, null)); //new type is for searching

		if (index < 0) {
			System.out.println("type " + name + " already does not exits");
			return;
		}

		types.get(index).del();
		types.remove(index);
		numOfTypes--;
		

	}

	void listAll() {
		int i = 1;
		System.out.println("Listing all types:");
		for (Type t : types) {
			System.out.println(i++ + ". -->  " + t.toString(true));

		}

	}

	void close() {
		try {
			closeShop();

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	/**
	 * write changes to disk 
	 * 
	 * @throws FileNotFoundException
	 */
	private void closeShop() throws FileNotFoundException {

		PrintStream ps = new PrintStream(sysCat);

		ps.println(DBname + " " + numOfTypes + " "  + " " + maxLenofTypeName + " " + numOfRecsPerPage
				+ " " + maxFieldSize);
		int i;
		for (i = 0; i < types.size() - 1; i++) {

			ps.println(types.get(i).toString(true));

		}

		if (!types.isEmpty())
			ps.print(types.get(i).toString(true));

		ps.close();

	}

}
