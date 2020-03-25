package strgmngr;

import java.io.IOException;
import java.io.RandomAccessFile;

public class Page {

	//private static int PGNo = 0;

	Record[] records = new Record[25];
	String pageHeader;
	int pageID;
	boolean isFull = false;
	boolean isLast = true;
	
	/**
	 * fixed size pages 990bytes
	 */
	static final int SIZE =  4 + 1 + 1 + 24 * 1 + 24 * 10 * 4;
	// header = 4 (int) + 2 (2 booleans)
	// 24 line also conatins 1 bool, 1 byte each
	// 24 'lines' each line has 10 int's each int 4 bytes

	public Page(Type tp) {
//		PGNo++;
//		pageID = PGNo;
		pageID  = tp.numberOfPages;

		for (int i = 0; i < 24; i++) {
			records[i] = new Record(new int[] { 0, 0, 0 });
		}

	}
	
	/**
	 * reads exactly one page
	 * 
	 * @param raFile raDomAccessFile
	 * @param pos  	offset to start read from file start (0)
	 * @param typeName		the name of the type this page belongs
	 * @throws IOException
	 */
	public void readPage(RandomAccessFile raFile, int pos, String typeName) throws IOException {
		System.out.println("Reading page #" + pageID +" of type "+ typeName);
		raFile.seek(pos);

		pageID = raFile.readInt();

		isFull = raFile.readBoolean();
		isLast = raFile.readBoolean();

		for (int i = 0; i < 24; i++) {
			//System.out.println("record i = " + i);
			Record r = new Record();
			r.readYourSelf(raFile);
			records[i] = r;

		}
	}

	/**
	 * 
	 * 
	 * writes the page currently at hand, last read page or empty page if non
	 * read before empty page refers to a page full of 10X0's
	 * 
	 * @param raFile
	 *            randomAccessFile to wtite
	 * @param pos
	 *            pointer relative to page start (0), points where to start
	 *            writing.
	 * @throws IOException
	 */

	public void writePage(RandomAccessFile raFile, int pos) throws IOException {

		raFile.seek(pos);

		raFile.writeInt(pageID);
		raFile.writeBoolean(isFull);
		raFile.writeBoolean(isLast);



		for (int i = 0; i < 24; i++) {
			records[i].writeYourSelf(raFile);

		}

	}
	
	/**
	 * find un occupied record in this page
	 * @return index of the record in this page 0 to 23 if exists;
	 * -1 otherwise
	 */

	int findUn_OccupiedRecord() {
		for (int i = 0; i < 24; i++) {
			if (!records[i].isOccupied) {
				return i;
			}
		}
		return -1;
	}

	/**
	 * prints page to console
	 */
	void printPage() {
		System.out.println(pageID + " " + isFull + " " + isLast);
		for (int i = 0; i < 24; i++) {
			System.out.println("record " + (i + 1) + "\t " + records[i].toString());

		}

	}
	
	/**
	 * 
	 * @return true if the all the 24 records of this page are occupied
	 */
	boolean isFulll() {

		try {

			for (Record f : records) {
				if (!f.isOccupied) {
					return false;
				}

			}

		} catch (NullPointerException e) {
			//e.printStackTrace();
			System.out.println("null record in page");
		}

		return true;
	}

}
