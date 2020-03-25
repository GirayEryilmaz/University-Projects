package strgmngr;

import java.io.IOException;
import java.io.RandomAccessFile;

public class Record implements Comparable<Record> {

	int[] fields;
	int key;
	boolean isOccupied = false;

	public Record() {

	}

	public Record(int[] fields) {
		// isOccupied =true;
		this.fields = fields;
		key = fields[0];

	}

	public Record(String line) {

		String[] arr = line.split(" ");

		if (arr[0].equals("1")) {
			isOccupied = true;

		}

		fields = new int[arr.length - 2];

		// it has to have first field
		fields[0] = Integer.parseInt(arr[1]);

		// rest are optional
		for (int i = 2; i < arr.length; i++) {
			// fields[i-2] = Integer.parseInt(arr[i]);
			fields[i - 1] = Integer.parseInt(arr[i]);
		}

	}

	/**
	 * writes this record to file
	 * offset is set before this method is called
	 * @param raFile randomAccessFile
	 * @throws IOException
	 */
	void writeYourSelf(RandomAccessFile raFile) throws IOException {
		raFile.writeBoolean(isOccupied);
		for (int f : fields) {

			raFile.writeInt(f);

		}

		for (int i = fields.length; i < 10; i++) {
			raFile.writeInt(0);

		}

	}

	/**
	 * reads this record from the file
	 * offset is set before this method is called
	 * @param raFile randomAccessFile
	 * @throws IOException
	 */
	void readYourSelf(RandomAccessFile raFile) throws IOException {
		isOccupied = raFile.readBoolean();
		//System.out.println(isOccupied);
		fields = new int[10];
		for (int i = 0; i < 10; i++) {
			fields[i] = raFile.readInt();

		}

		key = fields[0];

	}

	void delete() {
		isOccupied = false;
	}

	@Override
	public String toString() {
		int isOcc = (isOccupied) ? 1 : 0;

		StringBuffer sb = new StringBuffer();

		sb.append(isOcc);

		for (int f : fields) {

			sb.append(' ');
			String s = Integer.toString(f);

			for (int j = s.length(); j < 10; j++) {
				sb.append('0'); // 0's in the beginning
			}

			sb.append(s);

		}

		for (int i = fields.length; i < 10; i++) {
			sb.append(' ');
			sb.append("0000000000");

		}

		// \n is missing here, will put at when writing to file at Page.java

		return sb.toString();
	}

	@Override
	public int compareTo(Record r) {

		if (key > r.key) {
			return 1;
		} else if (key < r.key) {
			return -1;
		} else {
			return 0;
		}

	}

	@Override
	public int hashCode() {
		return Integer.hashCode(key);

	}

	@Override
	public boolean equals(Object obj) {
		Record rec = (Record) obj;
		return rec.key == this.key;

	}

}
