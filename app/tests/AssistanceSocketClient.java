import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class AssistanceSocketClient {
	protected BufferedReader input;
	protected PrintWriter output;
	protected Socket sock;
	protected String authToken;

	public AssistanceSocketClient(String host, int port, String authToken) throws UnknownHostException, IOException{
		this.authToken = authToken;
		this.sock = new Socket(host, port);
		this.input = new BufferedReader(new InputStreamReader(sock.getInputStream()));
		this.output = new PrintWriter(sock.getOutputStream( ), true);
	}

	public void sendData(String data2send){
		output.println(authToken+"\n"+data2send);
	}

	public String receiveData() throws IOException{
		return input.readLine();
	}

	public void close() throws IOException{
		sock.close();
	}
}
