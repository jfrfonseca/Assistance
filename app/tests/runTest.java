import java.io.IOException;


public class runTest {

	public static void main(String[] args) {
		AssistanceSocketClient dummySocket;
		try {
			dummySocket = new AssistanceSocketClient("127.0.0.1", 29112, "0123456789ABCDEF");
		    dummySocket.sendData("ASSISTANCE_SHA256_TEST\n"+"NONE"+"\n"+"NONE"+"\n"+"NONE"+"\n"+"NONE"+"\n");
		    System.out.println("requesting a SHA256 that SHOUD take a second to run!");
		    String ticket = dummySocket.receiveData();
		    dummySocket.close();
		    System.out.println("Received Assistance ServiceTicket "+ticket);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
