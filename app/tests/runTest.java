import java.io.IOException;
import java.net.ConnectException;
import java.lang.ArrayIndexOutOfBoundsException;


public class runTest {

	public static void main(String[] args) {
		AssistanceSocketClient dummySocket;
		String assistanceServer = "127.0.0.1";
		try {
			assistanceServer = args[0];
			System.out.println("Looking for a instance of the Assistance System in IP:"+assistanceServer);	
		}catch (ArrayIndexOutOfBoundsException arg){
			System.out.println("Assistance SHA256_TEST -JAVA will be run in localhost, since you did not provided another host as argument!");
		}
		try {
		    dummySocket = new AssistanceSocketClient(assistanceServer, 29112, "0123456789ABCDEF");
		    dummySocket.sendData("ASSISTANCE_SHA256_TEST\n"+"NONE"+"\n"+"NONE"+"\n"+"NONE"+"\n");
		    System.out.println("requesting a SHA256 that SHOUD take a second to run!");
		    String ticket = dummySocket.receiveData();
		    dummySocket.close();
		    System.out.println("Received Assistance ServiceTicket "+ticket);
		}catch (ConnectException c){
			System.out.println("No instance of the Assistance System was found in host IP:"+assistanceServer);
		}catch (IOException e) {
			e.printStackTrace();
		}
	}

}
