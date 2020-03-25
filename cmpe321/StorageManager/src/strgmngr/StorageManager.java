package strgmngr;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class StorageManager {

	public static void main(String[] args) throws IOException {

		SystemCatalog sysCat = new SystemCatalog();

		Scanner terminal = new Scanner(System.in);

		System.out.println("at start db has these --> " + sysCat.types.toString());

		String command;

		while (true) {
			command = terminal.next();

			if (command.equals("quit")) { //enter quit to terminate
				break;
			}

			// DDL opeartions

			if (command.startsWith("addType")) {
				String name = terminal.next();
				String temp;
				ArrayList<String> strL = new ArrayList<>();
				while (terminal.hasNext()) {

					temp = terminal.next();

					if (temp.equals("end")) { // signal end by enterinf end to
												// console
						addType(name, strL.toArray(new String[strL.size()]), sysCat);
						break;
					} else {
						strL.add(temp);
					}

				}

			}

			if (command.startsWith("deleteType")) {
				String name = terminal.next();
				deleteType(name, sysCat);
				System.out.println("delete this : ----------------" + name);

			}

			if (command.startsWith("listTypes")) {
				System.out.println("Listing all types!");
				listAllTypes(sysCat);
			}

			// DML operations

			if (command.startsWith("addRecord")) {
				String name = terminal.next();
				int temp;
				ArrayList<Integer> ints = new ArrayList<>();
				while (terminal.hasNext()) {

					try {
						temp = terminal.nextInt();
					} catch (Exception e) {
						int[] intAr = new int[ints.size()]; // copy arraylist to
															// array
						int index = 0;
						for (Integer i : ints) {
							intAr[index++] = i;
						}
						addRecord(name, intAr, sysCat);
						break;
					}
					ints.add(temp);

				}
			}

			if (command.startsWith("deleteRecord")) {
				String name = terminal.next();
				int key = terminal.nextInt();
				deleteRecord(name, key, sysCat);
			}

			if (command.startsWith("updateRecord")) {
				String name = terminal.next();
				int temp;
				ArrayList<Integer> ints = new ArrayList<>();
				while (terminal.hasNext()) {

					try {
						temp = terminal.nextInt(); // if non-int get read,
													// breaks
					} catch (Exception e) {
						int[] intAr = new int[ints.size()];
						int index = 0;
						for (Integer i : ints) {
							intAr[index++] = i;
						}
						updateRecord(name, intAr[0], intAr, sysCat);
						break;
					}
					ints.add(temp);

				}
			}

			if (command.startsWith("searchRecord")) {
				String name = terminal.next();
				int key = terminal.nextInt();
				search(name, key, sysCat);

			}

			if (command.startsWith("listRecordsOfType")) {
				String name = terminal.next();
				listRecordsOfType(name, sysCat);
			}

		}

		int testNo = 0;

		test(testNo, sysCat);
		terminal.close();

		System.out.println("at the end  SystemCat ------> = " + sysCat.types.toString());

		sysCat.close();
	}

	static void addType(String name, String[] fieldNames, SystemCatalog sysCat) throws IOException {
		Type nT = new Type(name, fieldNames);
		sysCat.add(nT);
	}

	static void deleteType(String name, SystemCatalog sysCat) throws IOException {
		sysCat.remove(name);
	}

	static void listAllTypes(SystemCatalog sysCat) {
		sysCat.listAll();
	}

	static void addRecord(String typeName, int[] fields, SystemCatalog sysCat) {
		try {

			Type t = findType(typeName, sysCat);
			t.addRecord(fields);

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	static void deleteRecord(String typeName, int key, SystemCatalog sysCat) {
		Type t = findType(typeName, sysCat);
		t.deleteRecord(key);

	}

	static void updateRecord(String typeName, int key, int[] fields, SystemCatalog sysCat) {
		Type t = findType(typeName, sysCat);
		t.updateRecord(key, fields);
	}

	static void search(String typeName, int key, SystemCatalog sysCat) {
		Type t = findType(typeName, sysCat);
		System.out.println(t.findRecord(key).toString());
	}

	static void listRecordsOfType(String typeName, SystemCatalog sysCat) {
		Type t = findType(typeName, sysCat);
		t.listAllRecords(false);
	}

	private static Type findType(String typeName, SystemCatalog sysCat) {
		Type t = null;
		try {

			int index = Collections.binarySearch(sysCat.types, new Type(typeName, null));
			t = sysCat.types.get(index);

		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("will return null, cause null pointer");
		}

		return t;

	}

	/**
	 * this method is for some test purposes
	 * 
	 * @param test
	 *            id of test
	 * @param sysCat
	 *            SystemCatalog
	 * @throws IOException
	 */
	static void test(int test, SystemCatalog sysCat) throws IOException {

		switch (test) {
		case 1:

			System.out.println("1 - addType , deleteType");

			addType("cb", null, sysCat);

			addType("a", null, sysCat);

			addType("b", null, sysCat);

			addType("g", null, sysCat);

			System.out.println("added a , b , cb --->" + sysCat.types.toString());

			deleteType("b", sysCat);

			System.out.println("removed b --->" + sysCat.types.toString());

			break;
		case 2:
			System.out.println("2 - listall");

			addType("cb", null, sysCat);

			addType("a", null, sysCat);

			addType("b", null, sysCat);

			System.out.println("added a , b , cb --->" + sysCat.types.toString());

			listAllTypes(sysCat);

			deleteType("b", sysCat);

			System.out.println("removed b --->" + sysCat.types.toString());

			listAllTypes(sysCat);

			break;
		case 3:
			System.out.println("3 --- delete a, b, c");
			deleteType("a", sysCat);
			deleteType("b", sysCat);
			deleteType("c", sysCat);
			break;
		case 4:
			addType("a", new String[] { "id", "password" }, sysCat);
			addRecord("a", new int[] { 5, 6, 7 }, sysCat);
			System.out.println("hey");
			break;
		case 5:
			addType("a", new String[] { "id", "password" }, sysCat);
			addType("b", new String[] { "id", "password" }, sysCat);
			addRecord("a", new int[] { 5, 6, 7 }, sysCat);
			addRecord("a", new int[] { 5, 6, 7 }, sysCat);
			addRecord("b", new int[] { 5, 6, 7 }, sysCat);
			System.out.println("how");
			break;
		case 6:
			addType("a", new String[] { "id", "password" }, sysCat);

			for (int i = 0; i < 20; i++) {
				addRecord("a", new int[] { 5, 6, 7 }, sysCat);
			}

			break;
		case 7:
			addType("g", new String[] { "cool", "fileds" }, sysCat);
			addRecord("g", new int[] { 3, 1, 2, 3, 4, 5, 6 }, sysCat);
			search("a", 5, sysCat);
			search("g", 3, sysCat);
			break;

		case 8:
			deleteRecord("g", 3, sysCat);
			break;
		case 9:

			listRecordsOfType("a", sysCat);
			addRecord("g", new int[] { 3, 1, 2, 3, 4, 5, 6 }, sysCat);

			listRecordsOfType("g", sysCat);
			break;
		default:
			System.out.println("no extra test done");
		}

	}

}
