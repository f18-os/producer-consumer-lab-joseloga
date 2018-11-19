import threading
import time
import logging
import random
import queue
import cv2
import os
import time

# globals
outputDir    = 'frames'
clipFileName = 'clip.mp4'
vidcap = cv2.VideoCapture(clipFileName)
BUF_SIZE = 10

q = queue.Queue(BUF_SIZE)
q2 = queue.Queue(BUF_SIZE)

def extractFrames(success,count, image):
    if(success):
        q.put(image)
        cv2.imwrite("{}/frame_{:04d}.jpg".format(outputDir, count), image)
        print('Reading frame {}'.format(count))
        return True
        
    else:
        print ("Done exporting ---------------------------------------------------")
        return False



def convertToGray(inFileName,inputFrame,count):
    
    if (inputFrame is not None):
        print("Converting frame {}".format(count))
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        outFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

        # write output file
        q2.put(cv2.imwrite(outFileName, grayscaleFrame))
        #delete inputfile
        if os.path.exists(inFileName):
            os.remove(inFileName)
        
    
        
        
def playVideo(count,frameDelay):    
    q2.get()
    startTime = time.time()

    # Generate the filename for the first frame 
    frameFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

    # load the frame
    frame = cv2.imread(frameFileName)
    if(frame is not None):  

        print("Displaying frame {}".format(count))
        # Display the frame in a window called "Video"
        cv2.imshow("Video", frame)

        # compute the amount of time that has elapsed
        # while the frame was processed
        elapsedTime = int((time.time() - startTime) * 1000)
        print("Time to process frame {} ms".format(elapsedTime))

        # determine the amount of time to wait, also
        # make sure we don't go into negative time
        timeToWait = max(1, frameDelay - elapsedTime)
        count+=1
        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(timeToWait) and 0xFF == ord("q"):
            #                            break    

            # get the start time for processing the next frame
            startTime = time.time()

            # get the next frame filename
            count += 1
            frameFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

            # Read the next frame file
            frame = cv2.imread(frameFileName)

            # make sure we cleanup the windows, otherwise we might end up with a mess
            cv2.destroyAllWindows()

                
class ExtractFrames(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ExtractFrames,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        count = 0
        flag =True
        if not os.path.exists(outputDir):
            print("Output directory {} didn't exist, creating".format(outputDir))
            os.makedirs(outputDir)
        while flag:
            if not q.full():
                
                success,image = vidcap.read()
                flag=extractFrames(success,count,image)
                count += 1
                    

        return

    
class convertThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(convertThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        count = 0
        aux=""
        flag= True
        while flag:
            if not q.empty():
                image = q.get()
                inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)
                aux=inFileName
                inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)
                convertToGray(inFileName,inputFrame,count)
                count += 1
                inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)
                success, jpgImage = cv2.imencode('.jpg', image)
                if(count in (0,738) ):
                    print("Done converting ---------------------------")
                    flag=False    
                
        return
    
    
    
class PlayvideoThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(PlayvideoThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
            counts = 0
            outputDir    = 'frames'
            frameDelay   = 42
            flag=True
            while flag:
                if not q2.full():
                    playVideo(counts,frameDelay)
                    counts+=1
                    print (counts," z")
                    if(counts in (0,738) ):
                        print("Done displaying ---------------------------")
                        flag=False
                    
                    
if __name__ == '__main__':
    
    f = ExtractFrames(name='extract')
    c = convertThread(name='convert')
    v = PlayvideoThread(name='video')

f.start()
c.start()
v.start()
   
