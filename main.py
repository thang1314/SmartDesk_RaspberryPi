import multiprocessing
import subprocess

if __name__ == '__main__':
    # Create a multiprocessing Process for each file
    p1 = multiprocessing.Process(target=subprocess.call, args=(['python', '/home/pi/Desktop/ce410/index.py'],))
    p2 = multiprocessing.Process(target=subprocess.call, args=(['python', '/home/pi/Desktop/ce410/camera.py'],))

    # Start both processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()

