import sys
import gui


def main():
    application = gui.Application(sys.argv)

    main_window = gui.MainWindow()
    main_window.show()

    return application.exec()


if __name__ == '__main__':
    result = main()
    sys.exit(result)
