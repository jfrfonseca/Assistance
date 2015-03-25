from pkgMissionControl.implementation import Launcher


def shutdown():
    Launcher.shutdown()
        

def setup():
    Launcher.setup()


if __name__ == '__main__':
    setup()