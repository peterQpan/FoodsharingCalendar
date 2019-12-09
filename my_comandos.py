import os
import queue
import threading
import time
import information
from events import Event
from googleconnect import GoogleEventCalendar
from information import JsFoodsharingSiteScraperFireFox
from randomone import SomethingDing

def deletePasswordAndEmail():
    if os.path.exists("soondong.tmp"):
        os.remove("soondong.tmp")

def runProgram(login_name, pswd, remember, main_window, first):
    import gui_toolkit  # or else circular import
    #todo loose circular import

    queue_here = queue.Queue()
    logging_window = gui_toolkit.LoggingWindow(input_queue=queue_here)
    main_window.update()
    driver = information.PlatformDriver(dev=False)
    fs_connection = JsFoodsharingSiteScraperFireFox(driver, queue_here, main_window=logging_window)
    fs_thread = threading.Thread(target=fs_connection.logingIn, args=(login_name, pswd, first))
    fs_thread.start()
    main_window.update()

    if remember:
        something = SomethingDing()
        something.save(login_name, pswd)

    fs_thread.join()
    fs_thread = threading.Thread(target=fs_connection.createEvents, args=())
    fs_thread.start()

    google_connection = GoogleEventCalendar(queue_here=queue_here)
    google_thread = threading.Thread(target=google_connection.fetchExistingEvents, args=())
    google_thread.start()

    logging_window.update()
    while fs_thread.is_alive() or google_thread.is_alive():
        time.sleep(0.4)
        logging_window.update()

    google_thread.join()
    fs_thread.join()
    fs_events = fs_connection.existingEvents()
    google_events = google_connection.existingEvents()
    checked_data, conflict_dict = Event.doubleCheck(fs_events, google_events)

    if conflict_dict:
        logging_window.result(conflict_dict)

    for event in checked_data:
        google_connection.createEvent(event)



