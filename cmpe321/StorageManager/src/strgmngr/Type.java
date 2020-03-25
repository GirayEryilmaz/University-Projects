package strgmngr;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;

public class Type implements Comparable<Type> {

	File typeFile_Standart;
	RandomAccessFile typeFile;

	String name = "";
	String[] fieldNames;
	boolean isFull = false;
	int numberOfPages = 1; // 1 comes as default
	int headerPos = 5;

	/**
	 * 
	 * @param typeName  name of type (unique)
	 * @param fieldNames	names of fields
	 * @throws IOException
	 */
	public Type(String typeName, String[] fieldNames) throws IOException {

		this.name = typeName; // "this." here is redundant
		this.fieldNames = fieldNames;

		typeFile_Standart = new File(name);
		typeFile = new RandomAccessFile(typeFile_Standart, "rw");

		if (typeFile.length() == 0) { // if Type file is empty

			// type header: isFull, numberOfPages
			typeFile.writeBoolean(false);

			typeFile.writeInt(1);

			Page p1 = new Page(this);
			p1.writePage(typeFile, 1 + 4); // one bool one int (type header)

		} else {

			typeFile.seek(0); //go to top of page

			isFull = typeFile.readBoolean();

			numberOfPages = typeFile.readInt(); // numberOfPages

		}

	}
	
	/**
	 * 
	 * @param fields adds a record with give fields
	 * @throws IOException
	 */

	void addRecord(int[] fields) throws IOException {

		if (this.isFull) {
			System.out.println("this Type is full!");
			return;

		}

		Record nR = new Record(fields);
		nR.isOccupied = true;
		int pos = headerPos; // pointer to first page

		Page p;

		do {

			// System.out.println("pos: " + pos);
			p = new Page(this);

			p.readPage(typeFile, pos,name);

			if (p.isFull) {
				if (p.isLast) {
					p.isLast = false;
					p.writePage(typeFile, pos); // overwrite last page which is
												// not last page anymore

					// TO-DO add new Page
					numberOfPages++;

					int temp = (int) typeFile.getFilePointer(); // push

					typeFile.seek(1); // skip isFull
					typeFile.writeInt(numberOfPages);

					typeFile.seek(temp); // pull

					p = new Page(this);
					p.isLast = true;

					p.records[0] = nR; // since page is already empty


					//write fresh page to next place (to the end)
					p.writePage(typeFile, (int) typeFile.length());

					break;

				} else {
					pos += Page.SIZE; // go to next page

				}

			} else {

				int index = p.findUn_OccupiedRecord();
				p.records[index] = nR;

				p.isFull = p.isFulll();
				p.writePage(typeFile, pos);

				break;

			}

		} while (true);

		p.printPage();

	}
	
/**
 * finds the record with the key and sets new fields to it
 * @param key the key
 * @param fields new fields
 */
	void updateRecord(int key, int[] fields){
		try {

			int pos = headerPos;

			Page p = new Page(this); // 'this' is unused as parameter,
										// unncessary

			do {

				p.readPage(typeFile, pos,name);
				p.printPage();

				for (Record r : p.records) {
					if (r == null) {
						System.out.println("r is null");
					} else {
						if (r.key == key && r.isOccupied) {
							
							r.fields = fields;
							
							p.writePage(typeFile, pos);
							p.printPage();
							return;
							
						}
					}
				}

				pos += Page.SIZE;

			} while (pos < typeFile.length());

		} catch (

		IOException e) {
			e.printStackTrace();
			System.out.println("could not find the record int this type for some reason");
		}
		
	}
	
	/**
	 * 
	 * finds the record with this key and sets isOccupied to false
	 * @param key the key
	 */

	void deleteRecord(int key) {
		try {

			int pos = headerPos;

			Page p = new Page(this); // 'this' is unused as parameter,
										// unncessary

			do {

				p.readPage(typeFile, pos,name);
				p.printPage();

				for (Record r : p.records) {
					if (r == null) {
						System.out.println("r is null");
					} else {
						if (r.key == key && r.isOccupied) {
							r.delete();
							p.isFull = false;
							p.writePage(typeFile, pos);
							p.printPage();
							return;
							
						}
					}
				}

				pos += Page.SIZE;

			} while (pos < typeFile.length());

		} catch (

		IOException e) {
			e.printStackTrace();
			System.out.println("could not find the record int this type for some reason");
			System.out.println("will return null");
		}
	}

	/**
	 * will find the record with the key is it exists in this type
	 * 
	 * @param key
	 * @return the record if exists else null
	 * @throws IOException
	 */

	Record findRecord(int key) {
		try {

			int pos = headerPos;

			Page p = new Page(this); // 'this' is unused as parameter,
										// unncessary

			do {

				p.readPage(typeFile, pos,name);

				for (Record r : p.records) {
					if (r.key == key && r.isOccupied) {
						return r;
					}
				}

				pos += Page.SIZE;

			} while (pos < typeFile.length());

		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("could not find the record int this type for some reason");
			System.out.println("will return null");
		}
		return null;
	}
	
	
	void listAllRecords(boolean reallyAll){
		try {

			int pos = headerPos;

			Page p = new Page(this); // 'this' is unused as parameter,
										// unncessary

			do {

				p.readPage(typeFile, pos,name);

				for (Record r : p.records) {
					if(r!=null){
						if(reallyAll || r.isOccupied){
							System.out.println(r.toString());
						}
					}
					
					
				}

				pos += Page.SIZE;

			} while (pos < typeFile.length());

		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("could not find the record int this type for some reason");
			System.out.println("will return null");
		}
		
		
	}

	@Override
	public int hashCode() {
		return name.hashCode();
	}

	@Override
	public boolean equals(Object obj) {
		Type tp = (Type) obj;
		return tp.name.equals(name);

	}

	@Override
	public int compareTo(Type o) {

		return this.name.compareTo(o.name);

	}

	@Override
	public String toString() {
		return name;
	}

	public String toString(Boolean b) {
		StringBuffer sb = new StringBuffer(name);
		if (fieldNames == null) {
			return name;
		}
		for (String s : fieldNames) {
			sb.append(' ');
			sb.append(s);
		}
		return sb.toString();
	}

	/**
	 * close the file and delete it from disk too
	 * @throws IOException
	 */
	void del() throws IOException {

		typeFile.close();
		typeFile_Standart.delete();

	}

}
