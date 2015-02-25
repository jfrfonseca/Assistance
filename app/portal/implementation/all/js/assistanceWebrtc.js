
/*
 * Constants
 */
const verbosity = 1;
const logDiv = 'consoleDiv';
const transceiverPort = 23019;
const wsUri = "ws://localhost:"+transceiverPort+"/";

/*
 * Buffers
 */
var firebaseUrl;
var database;
var announceChannel;
var signalChannel;
var webSocket;

/*
 * Variables
 */
var id;              // Our unique ID
var sharedKey;       // Unique identifier for two clients to find each other
var remote;          // ID of the remote peer -- set once they send an offer
var peerConnection;  // This is our WebRTC connection
var dataChannel;     // This is our outgoing data channel within WebRTC
var running = false; // Keep track of our connection state

/*
 * GUI Functions
 */
function logMsg(minVerb, divLogName, message){
	//console.log(message);
	if(verbosity >= minVerb){
		$('#'+divLogName).append('<p>' + message + '</p>');
	}
}

function logMsg(minVerb, divLogName, message, color){
	//console.log(message);
	if(verbosity >= minVerb){
		$('#'+divLogName).append('<p><span style="color: '+color+';">' + message + '</span></p>');
	}
}



/* Based on the WebRTC Demo avaliable in http://fosterelli.co/getting-started-with-webrtc-data-channels.html
 * Allows two clients to connect via WebRTC with Data Channels, using Firebase as a signalling server
 */

/* == Announcement Channel Functions ==
 * The 'announcement channel' allows peers to find each other on Firebase
 * These functions are for communicating through the announcement channel
 * This is part of the signalling server mechanism
 *
 * After two peers find each other on the announcement channel, they 
 * can directly send messages to each other to negotiate a WebRTC connection
 */

//Announce our arrival to the announcement channel
var sendAnnounceChannelMessage = function() {
	announceChannel.remove(function() {
		announceChannel.push({
			sharedKey : sharedKey,
			id : id
		});
		logMsg(2, logDiv, 'Announced our sharedKey is ' + sharedKey);
		logMsg(0, logDiv, 'Announced our ID is ' + id);
	});
};

//Handle an incoming message on the announcement channel
var handleAnnounceChannelMessage = function(snapshot) {
	var message = snapshot.val();
	if (message.id != id && message.sharedKey == sharedKey) {
		logMsg(0, logDiv, 'Discovered matching announcement from ' + message.id);
		remote = message.id;
		initiateWebRTCState();
		connect();
	}
};

/* == Signal Channel Functions ==
 * The signal channels are used to delegate the WebRTC connection between 
 * two peers once they have found each other via the announcement channel.
 * 
 * This is done on Firebase as well. Once the two peers communicate the
 * necessary information to 'find' each other via WebRTC, the signalling
 * channel is no longer used and the connection becomes peer-to-peer.
 */

//Send a message to the remote client via Firebase
var sendSignalChannelMessage = function(message) {
	message.sender = id;
	database.child('messages').child(remote).push(message);
};

//Handle a WebRTC offer request from a remote client
var handleOfferSignal = function(message) {
	running = true;
	remote = message.sender;
	initiateWebRTCState();
	startSendingCandidates();
	peerConnection.setRemoteDescription(new RTCSessionDescription(message));
	peerConnection.createAnswer(function(sessionDescription) {
		logMsg(1, logDiv, 'Sending answer to ' + message.sender);
		peerConnection.setLocalDescription(sessionDescription);
		sendSignalChannelMessage(sessionDescription);
	});
};

//Handle a WebRTC answer response to our offer we gave the remote client
var handleAnswerSignal = function(message) {
	peerConnection.setRemoteDescription(new RTCSessionDescription(message));
};

//Handle an ICE candidate notification from the remote client
var handleCandidateSignal = function(message) {
	var candidate = new RTCIceCandidate(message);
	peerConnection.addIceCandidate(candidate);
};

//This is the general handler for a message from our remote client
//Determine what type of message it is, and call the appropriate handler
var handleSignalChannelMessage = function(snapshot) {
	var message = snapshot.val();
	var sender = message.sender;
	var type = message.type;
	logMsg(2, logDiv, 'Recieved a \'' + type + '\' signal from ' + sender);
	if (type == 'offer') handleOfferSignal(message);
	else if (type == 'answer') handleAnswerSignal(message);
	else if (type == 'candidate' && running) handleCandidateSignal(message);
};

/* == ICE Candidate Functions ==
 * ICE candidates are what will connect the two peers
 * Both peers must find a list of suitable candidates and exchange their list
 * We exchange this list over the signalling channel (Firebase)
 */

//Add listener functions to ICE Candidate events
var startSendingCandidates = function() {
	peerConnection.oniceconnectionstatechange = handleICEConnectionStateChange;
	peerConnection.onicecandidate = handleICECandidate;
};

//This is how we determine when the WebRTC connection has ended
//This is most likely because the other peer left the page
var handleICEConnectionStateChange = function() {
	if (peerConnection.iceConnectionState == 'disconnected') {
		logMsg(0, logDiv, 'Client disconnected!');
		sendAnnounceChannelMessage();
	}
};

//Handle ICE Candidate events by sending them to our remote
//Send the ICE Candidates via the signal channel
var handleICECandidate = function(event) {
	var candidate = event.candidate;
	if (candidate) {
		candidate.type = 'candidate';
		logMsg(2, logDiv, 'Sending candidate to ' + remote);
		sendSignalChannelMessage(candidate);
	} else {
		logMsg(2, logDiv, 'All candidates sent');
	}
};

/* == Data Channel Functions ==
 * The WebRTC connection is established by the time these functions run
 * The hard part is over, and these are the functions we really want to use
 * 
 * The functions below relate to sending and receiving WebRTC messages over
 * the peer-to-peer data channels 
 */

//This is our receiving data channel event
//We receive this channel when our peer opens a sending channel
//We will bind to trigger a handler when an incoming message happens
var handleDataChannel = function(event) {
	event.channel.onmessage = handleDataChannelMessage;
};

//This is called on an incoming message from our peer
//You probably want to overwrite this to do something more useful!
var handleDataChannelMessage = function(event) {
	logMsg(0, logDiv, 'Recieved Message: ' + event.data);
	logMsg(2, logDiv, event.data);
};

//This is called when the WebRTC sending data channel is officially 'open'
var handleDataChannelOpen = function() {
	logMsg(1, logDiv, 'Data channel created!');
	//starts the Assistance Transceiver Server
	startAssistanceTransceiver(dataChannel);
};

//Called when the data channel has closed
var handleDataChannelClosed = function() {
	logMsg(0, logDiv, 'The data channel has been closed!');
};

//Function to offer to start a WebRTC connection with a peer
var connect = function() {
	running = true;
	startSendingCandidates();
	peerConnection.createOffer(function(sessionDescription) {
		logMsg(2, logDiv, 'Sending offer to ' + remote);
		peerConnection.setLocalDescription(sessionDescription);
		sendSignalChannelMessage(sessionDescription);
	});
};

//Function to initiate the WebRTC peerconnection and dataChannel
var initiateWebRTCState = function() {
	try { peerConnection = new webkitRTCPeerConnection(servers); }
	catch(err) { alert('Darn! Unfortunately, this system is only compatible with webkit-based browsers - Chrome and Safari. Firefox, we will get to you soon! I promise!'); }
	peerConnection.ondatachannel = handleDataChannel;
	dataChannel = peerConnection.createDataChannel('assistanceDevDataChannel');
	dataChannel.onmessage = handleDataChannelMessage;
	dataChannel.onopen = handleDataChannelOpen;
};

//Use Google's public servers for STUN
//STUN is a component of the actual WebRTC connection
var servers = {
		iceServers: [ 
		             { url : 'stun:stun.l.google.com:19302' },
		             { url : 'stun:stun.l.google.com:19302' },
		             { url : 'stun:stun1.l.google.com:19302' },
		             { url : 'stun:stun2.l.google.com:19302' },
		             { url : 'stun:stun3.l.google.com:19302' },
		             { url : 'stun:stun4.l.google.com:19302' },
		             { url : 'stun:stun01.sipphone.com:19302' },
		             { url : 'stun:stun.ekiga.net:19302' },
		             { url : 'stun:stun.fwdnet.net:19302' },
		             { url : 'stun:stun.ideasip.com:19302' },
		             { url : 'stun:stun.iptel.org:19302' },
		             { url : 'stun:stun.rixtelecom.se:19302' },
		             { url : 'stun:stun.schlund.de:19302' },
		             { url : 'stun:stunserver.org:19302' },
		             { url : 'stun:stun.softjoys.com:19302' },
		             { url : 'stun:stun.voiparound.com:19302' },
		             { url : 'stun:stun.voipbuster.com:19302' },
		             { url : 'stun:stun.voipstunt.com:19302' },
		             { url : 'stun:stun.voxgratia.org:19302' },
		             { url : 'stun:stun.xten.com:19302' },
		             ]
};


/*
 * 
 */
function setupWebSocket(){
	websocket = new WebSocket(wsUri);
	websocket.onopen = function(evt) { onOpen(evt) };
	websocket.onclose = function(evt) { onClose(evt) };
	websocket.onmessage = function(evt) { onMessage(evt) };
	websocket.onerror = function(evt) { onError(evt) };
}

function onOpen(evt)
{
	logMsg(1, logDiv,"CONNECTED", 'gray');
	performAssistanceTransceiverHandshake();
}

function onClose(evt)
{
	logMsg(1, logDiv,"DISCONNECTED", 'gray');
}

function onMessage(evt)
{
	logMsg(1, logDiv,'RESPONSE: ' + evt.data, 'blue');
	websocket.close();
}

function onError(evt)
{
	logMsg(1, logDiv,'ERROR: ' + evt.data + '. Ignore this message if Assistance Courier has not been initialized.', 'red');
}

function doSend(message)
{
	logMsg(1, logDiv,"SENT: " + message, 'green'); 
	websocket.send(message);
}


/*
 * Assistance Functions
 */
function performAssistancePeerHandshake(dataChan){
	dataChan.send('ID-' + id +'; '+'TM-'+(new Date()).getTime()+'');
	logMsg(0, logDiv, 'Handshake Successfull');
}

function performAssistanceTransceiverHandshake(){
	doSend("WebSocket REALLY rocks. So does WebRTC! Assistance manda seus cumprimentos para os artistas.");
}

function startAssistanceTransceiver(dataChan){
	performAssistancePeerHandshake(dataChan);
	setupWebSocket();
}


/*
 * tests
 */
function assistanceTransceiverTest(){
	/*
	 * Setup of the Basic Tests
	 */
	// Generate this AssistancePeer a unique ID
	// AssistancePeers use this unique ID to address messages to each other after they have found each other in the announcement channel
	id = Math.random().toString().replace('.', '');

	// Configure Firebase Channel Servers
	// Assistance - DEV VERSION - Firebase URL
	firebaseUrl = 'https://assistance-dev.firebaseio.com/';
	database = new Firebase(firebaseUrl);
	announceChannel = database.child('announce');
	signalChannel = database.child('messages').child(id);

	// Unique identifier for two peers find each other on the Firebase server
	// They MUST share this to find each other
	// Each peer waits in the announcement channel to find a match to its identifier
	// When it finds its matching identifier, it initiates a WebRTC offer with the sender Peer. This unique identifier can be pretty much anything in practice.
	sharedKey = "QXNzaXN0YW5jZSBEZXZlbGxvcG1lbnQgVmVyc2lvbiBEZWZhdWx0IFNoYXJlZCBLZXk=";

	
	// Set up the Signal Channel service - a way to offers to get received
	signalChannel.on('child_added', handleSignalChannelMessage);

	// Set up the Announce Channel service - a way to offers to be sent
	announceChannel.on('child_added', handleAnnounceChannelMessage);

	/*
	 * Performing the test
	 */
	// Send a message to the announcement channel
	// If our partner is already waiting, they will send us a WebRTC offer
	// over our Firebase signalling channel and we can begin delegating WebRTC
	sendAnnounceChannelMessage();
}


function assistanceTransceiverTestCloseup(){
	var logtext = document.getElementById(logDiv).innerHTML;
	database.child('logs').child(id).set(logtext);
	logMsg(0, logDiv,"The test has properly ended", 'green'); 
	database.goOffline();
}






