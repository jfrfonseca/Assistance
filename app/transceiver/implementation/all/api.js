



// Configure Firebase Channel Servers
// Assistance - DEV VERSION - Firebase URL
var firebaseUrl = 'https://assistance-dev.firebaseio.com/';
var database = new Firebase(firebaseUrl);
var announceChannel = database.child('announce');
var signalChannel = database.child('messages').child(id);



//function aTransceiverSetup(){
	// Generate this AssistancePeer a unique ID
	// AssistancePeers use this unique ID to address messages to each other after they have found each other in the announcement channel
	id = Math.random().toString().replace('.', '');

	// Unique identifier for two peers find each other on the Firebase server
	// They MUST share this to find each other
	// Each peer waits in the announcement channel to find a match to its identifier
	// When it finds its matching identifier, it initiates a WebRTC offer with the sender Peer. This unique identifier can be pretty much anything in practice.
	sharedKey = "QXNzaXN0YW5jZSBEZXZlbGxvcG1lbnQgVmVyc2lvbiBEZWZhdWx0IFNoYXJlZCBLZXk=";
	
	// Set up the Signal Channel service - a way to offers to get received
	signalChannel.on('child_added', handleSignalChannelMessage);

	// Set up the Announce Channel service - a way to offers to be sent
	announceChannel.on('child_added', handleAnnounceChannelMessage);


	// Send a message to the announcement channel
	// If our partner is already waiting, they will send us a WebRTC offer
	// over our Firebase signalling channel and we can begin delegating WebRTC
	sendAnnounceChannelMessage();
//}
