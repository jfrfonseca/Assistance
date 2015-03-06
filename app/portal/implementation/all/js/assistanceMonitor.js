/* ==================================================
 * ~~~~~~~~~~~~~~~~~~ Constants on Defaults ~~~~~~~~~~~~~~~~~~
 * ==================================================
 */
const interval = 1;														// Level of importance of the messages logged by the Portal
const plotDiv = 'plotDiv';										// DIV to print the messages logged by the Portal
const intendentPort = 23019;										// Port for the WebSocket to communicate thorough
const wsUri = "ws://localhost:"+intendentPort+"/";		// URL to communicate with the WebSocket


function setupWebSocket(){
	websocket = new WebSocket(wsUri);
	websocket.onopen = function(evt) { onOpen(evt) };
	websocket.onclose = function(evt) { onClose(evt) };
	websocket.onmessage = function(evt) { onMessage(evt) };
	websocket.onerror = function(evt) { onError(evt) };
}

function onOpen(evt)
{
	console.log("CONNECTED");
}

function onClose(evt)
{
	console.log("DISCONNECTED");
}

function onMessage(evt)
{
	
}

function onError(evt)
{
	console.log('ERROR: ' + evt.data);
}

function doSend(message)
{
	console.log("SENT: " + message); 
	websocket.send(message);
}


function assistanceMonitorTest(){
	
}