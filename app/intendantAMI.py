from AssistanceInstance.txt import py
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch the Assistance service.')
    parser.add_argument("--test_tor_transceiver_echo", action="store_true", 
                        help="run the pkgTransceiver service package as a echo server to the tor component on its tor port")
    
    args = parser.parse_args()
    
    thisInstance = AssistanceInstance.py.AssistanceInstance()
    
    if (args.test_tor_transceiver_echo):
        thisInstance.testTorTransceiverEcho()
