import threading
import time
import logging
import random
import queue
import cv2
import os



# globals
outputDir    = 'frames'
clipFileName = 'clip.mp4'
# initialize frame count    
#count = 0
vidcap = cv2.VideoCapture(clipFileName)
success,image = vidcap.read()

logging.basicConfig(level=logging.DEBUG,
format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 10
q = queue.Queue(BUF_SIZE)

def convertToGrayscale(inputFrame,outputDir,count):
    if (inputFrame is not None):
        print("Converting frame {}".format(count))
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)


        outFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

        # write output file
        cv2.imwrite(outFileName, grayscaleFrame)
        #delete inputfile
        if os.path.exists(inFileName):
            os.remove(inFileName    )

        count += 1
        inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)
        
class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        count = 0
        while True:
            if not q.full():
                print("1")
#              item = random.randint(1,10)

                if not os.path.exists(outputDir):
                    print("Output directory {} didn't exist, creating".format(outputDir))
                    os.makedirs(outputDir)

                success,image = vidcap.read()
                if(success):
                    q.put(image)
                    cv2.imwrite("{}/frame_{:04d}.jpg".format(outputDir, count), image)
                    print('Reading frame {}'.format(count))
                    count += 1
#                    time.sleep(1000)
        
                
#                logging.debug('Putting ' + str(item)  
#                              + ' : ' + str(q.qsize()) + ' items in queue')
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        count = 0
        while True:
            if not q.empty():
                print("2")
                image = q.get()
                inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)
                inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

                if (inputFrame is not None):
                    print("Converting frame {}".format(count))
                    # convert the image to grayscale
                    grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)


                    outFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

                    # write output file
                    cv2.imwrite(outFileName, grayscaleFrame)
                    #delete inputfile
                    if os.path.exists(inFileName):
                        os.remove(inFileName)

                    count += 1

                    inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)

                    # load the next frame
                    inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

    #                time.sleep(random.random())
        return

if __name__ == '__main__':

    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

p.start()
time.sleep(1)
c.start()
time.sleep(1)   