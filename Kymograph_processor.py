import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import glob
import tkinter.filedialog as tkfd
import tkinter as tk
import gc
import time

import lumicks.pylake as lk



def exportListOfListToFile(columns, filename):
    with open(filename, "w") as csvToExport:
        csvToExport.write(time.asctime(time.localtime(time.time())) + "\n")

        for i in range(len(columns[0])):
            currLine = ""
            for j in range(len(columns)):
                currLine += (str(columns[j][i]) + ", ")
            currLine += "\n"
            csvToExport.write(currLine)

def exportDict(dictToExport, filename):
    with open(filename, "w") as csvToExport:
        csvToExport.write(time.asctime(time.localtime(time.time())) + "\n")

        for eachKey in dictToExport.keys():
            currLine = str(eachKey) + ", " + str(dictToExport[eachKey]) + "\n"
            csvToExport.write(currLine)

def exportSettingsFromDict(dictOfSettings, filename):
    with open(filename, "w") as csvToExport:
        csvToExport.write(time.asctime(time.localtime(time.time())) + "\n")

        for eachKey in dictOfSettings.keys():
            currLine = str(eachKey) + ", " + str(dictOfSettings[eachKey][1]) + "\n"
            csvToExport.write(currLine)

def importSettingsFromCSV(dictOfEntryObjects):
    csvFilename = tkfd.askopenfilename(title="choose the settings file for track_greedy",\
                                    filetypes=[("csv files", ".csv"),\
                                               ("all files", "*,*")])
    allKeys = dictOfEntryObjects.keys()
    if csvFilename != "":
        with open(csvFilename, "r") as csvFile:
            lines = csvFile.readlines()
            for line in lines:
                formattedList = line.split("\n")[0].split(", ")
                if formattedList[0] in allKeys:
                    dictOfEntryObjects[formattedList[0]][1] = formattedList[1]

    setEntryValues(dictOfEntryObjects)    

'''
def traceAndExtractSignal2(kymo,\
                          averagingPxLengths = 2,\
                          tracedChannel = "blue", \
                          extractSignalFromChannel = "red",
                          trackWidth = 0.2,\
                          pixelThreshold = 1,\
                          window = 6):

#    kymoActualHeight = kymo.pixels_per_line * kymo.pixelsize_um[0]
    red = kymo.get_image(extractSignalFromChannel)
    kymoActualDuration = red.shape[1] * kymo.line_time_seconds

    upperBead = 6
    lowerBead = 20

    traces = lk.track_greedy(kymo,\
                             tracedChannel,\
                             track_width=trackWidth,\
                             pixel_threshold=pixelThreshold,\
                             window=window,\
                             rect=[[0, upperBead],\
                                   [kymoActualDuration, lowerBead]])

    traces = lk.filter_tracks(traces, 20)

    allRedTraces = []
    
    for trace in traces:
    
        timeLengthPx = len(trace)
    
        redChannel = [0 for x in range(timeLengthPx)]

    
        for i in range(timeLengthPx):
            y = int(trace.coordinate_idx[i])
            x = trace.time_idx[i]

           # Take average
            tempAggregate = 0
            totalAveragePoints = 2 * averagingPxLengths + 1
            for j in range(totalAveragePoints):
                tempAggregate += red[y - averagingPxLengths + j, x]
            redChannel[i] = tempAggregate / totalAveragePoints
        allRedTraces.append(redChannel)

    return traces, allRedTraces
'''

def traceKymo(kymo,\
                averagingPxLengths = 2,\
                tracedChannel = "blue", \
                trackWidth = 0.2,\
                pixelThreshold = 1,\
                window = 6,\
                RectLeft = 0,\
                RectUp = 6,\
                RectRight = -1,\
                RectDown = 20,\
                FilterTrace = 10):

    tracedChannelImage = kymo.get_image(tracedChannel)
    kymoActualDuration = tracedChannelImage.shape[1] * kymo.line_time_seconds

    if -1 == RectRight:
        RectRight = kymoActualDuration

    traces = lk.track_greedy(kymo,\
                             tracedChannel,\
                             track_width=trackWidth,\
                             pixel_threshold=pixelThreshold,\
                             window=window,\
                             rect=[[RectLeft, RectUp],\
                                   [RectRight, RectDown]])

    return lk.filter_tracks(traces, FilterTrace)

def extractSignalFromTrace(kymo,\
                           trace,\
                           signalChannel="red",\
                           averagingPxLengths=1):
    signalChannelMatrix = kymo.get_image(signalChannel)
    
    timeLengthPx = len(trace)

    oneTrackOfSignal = [0 for x in range(timeLengthPx)]


    for i in range(timeLengthPx):
        y = int(trace.coordinate_idx[i])
        x = trace.time_idx[i]

       # Take average
        tempAggregate = 0
        totalAveragePoints = 2 * averagingPxLengths + 1
        for j in range(totalAveragePoints):
            tempAggregate += signalChannelMatrix[y - averagingPxLengths + j, x]
        oneTrackOfSignal[i] = tempAggregate / totalAveragePoints

    return oneTrackOfSignal




def traceAndExtractSignal(kymo,\
                           averagingPxLengths = 2,\
                           tracedChannel = "blue", \
                           extractSignalFromChannel = "red",
                           trackWidth = 0.2,\
                           pixelThreshold = 1,\
                           window = 6,\
                           RectLeft = 0,\
                           RectUp = 6,\
                           RectRight = -1,\
                           RectDown = 20,\
                           FilterTrace = 10):

#    kymoActualHeight = kymo.pixels_per_line * kymo.pixelsize_um[0]
    red = kymo.get_image(extractSignalFromChannel)
    kymoActualDuration = red.shape[1] * kymo.line_time_seconds

    if -1 == RectRight:
        RectRight = kymoActualDuration

    traces = lk.track_greedy(kymo,\
                             tracedChannel,\
                             track_width=trackWidth,\
                             pixel_threshold=pixelThreshold,\
                             window=window,\
                             rect=[[RectLeft, RectUp],\
                                   [RectRight, RectDown]])

    traces = lk.filter_tracks(traces, FilterTrace)

    allRedTraces = []
    
    for trace in traces:
    
        timeLengthPx = len(trace)
    
        redChannel = [0 for x in range(timeLengthPx)]

    
        for i in range(timeLengthPx):
            y = int(trace.coordinate_idx[i])
            x = trace.time_idx[i]

           # Take average
            tempAggregate = 0
            totalAveragePoints = 2 * averagingPxLengths + 1
            for j in range(totalAveragePoints):
                tempAggregate += red[y - averagingPxLengths + j, x]
            redChannel[i] = tempAggregate / totalAveragePoints
        allRedTraces.append(redChannel)

    return traces, allRedTraces

def saveFigure(kymo,\
               traces,\
               allRedTraces,\
               fileName,\
               extractSignalFromChannel = "red"):
    kymoActualDuration = kymo.get_image(extractSignalFromChannel).shape[1] *\
                         kymo.line_time_seconds
    
    fig, ax = plt.subplots(3, 1)
    plt.figure(figsize=(6,9))
    plt.subplots_adjust(left=0.2, 
                    bottom=0.1,  
                    right=0.9,  
                    top=0.9,  
                    wspace=0.4,  
                    hspace=0.6) 
    plt.subplot(3, 1, 1)
    kymo.plot(channel="rgb", aspect="auto", adjustment=lk.ColorAdjustment(0, 1))
    for i in range(len(traces)):
        b = plt.subplot(3, 1, 1)
# comment out the following line to not plot the tracing line(s) on the raw image
        b.plot(traces[i].seconds, traces[i].position)
        a = plt.subplot(3, 1, 2)
        a.plot(traces[i].seconds, allRedTraces[i])
        a.set_title("Condensin signal")
        a.set_ylabel("Red Fluorescence (AU)")
        a.set_xlabel("time (s)")
        a.set_xlim(left=0, right=kymoActualDuration)
        plt.subplot(3, 1, 3)
        traces[i].plot_msd(max_lag=200, marker='.')
    plt.savefig(fileName + "_plot.tiff")
    plt.close("all")
    plt.cla()
    plt.clf()

def saveFigureForTrace(kymo,\
                       trace,\
                       RedTrace,\
                       fileName,\
                       extractSignalFromChannel = "red",
                       maximumLagFrames = 200):
    
    kymoActualDuration = kymo.get_image(extractSignalFromChannel).shape[1] *\
                         kymo.line_time_seconds
    
     

    
    fig, ax = plt.subplots(3, 1)
    plt.figure(figsize=(6,9))
    plt.subplots_adjust(left=0.2, 
                        bottom=0.1,  
                        right=0.9,  
                        top=0.9,  
                        wspace=0.4,  
                        hspace=0.6)
    b = plt.subplot(3, 1, 1)
    kymo.plot(channel="rgb",\
              aspect="auto",\
              adjustment=lk.ColorAdjustment(0, 1))
# comment out the following line to not plot the tracing line(s) on the raw image
    b.plot(trace.seconds, trace.position)
    a = plt.subplot(3, 1, 2)
    a.plot(trace.seconds, RedTrace)
    a.set_title("Condensin signal")
    a.set_ylabel("Red Fluorescence (AU)")
    a.set_xlabel("time (s)")
    a.set_xlim(left=0, right=kymoActualDuration)
    plt.subplot(3, 1, 3)
    trace.plot_msd(max_lag=maximumLagFrames, marker='.')
    plt.savefig(str(fileName))
    plt.close("all")
    plt.cla()
    plt.clf()
    
'''
def saveIndividualFigure(kymo,\
                         traces,\
                         allRedTraces,\
                         fileName,\
                         extractSignalFromChannel = "red"):
    
    kymoActualDuration = kymo.get_image(extractSignalFromChannel).shape[1] *\
                         kymo.line_time_seconds
    
     

    for i in range(len(traces)):
        fig, ax = plt.subplots(3, 1)
        plt.figure(figsize=(6,9))
        plt.subplots_adjust(left=0.2, 
                            bottom=0.1,  
                            right=0.9,  
                            top=0.9,  
                            wspace=0.4,  
                            hspace=0.6)
        b = plt.subplot(3, 1, 1)
        kymo.plot(channel="rgb",\
                  aspect="auto",\
                  adjustment=lk.ColorAdjustment(0, 1))
# comment out the following line to not plot the tracing line(s) on the raw image
        b.plot(traces[i].seconds, traces[i].position)
        a = plt.subplot(3, 1, 2)
        a.plot(traces[i].seconds, allRedTraces[i])
        a.set_title("Condensin signal")
        a.set_ylabel("Red Fluorescence (AU)")
        a.set_xlabel("time (s)")
        a.set_xlim(left=0, right=kymoActualDuration)
        plt.subplot(3, 1, 3)
        traces[i].plot_msd(max_lag=200, marker='.')
        plt.savefig(str(fileName) + "_" + str(i) + "_plot.tiff")
        plt.close("all")
        plt.cla()
        plt.clf()
'''

def h5FileFinder(path):
    collection = []
    for x in glob.iglob(path + '**/**', recursive=True):
        if x.endswith(".h5"):
            collection.append(x)
    return collection


def headlessBatchProcessing():

    files = tkfd.askopenfilenames(title="choose source h5 file(s)",\
                                filetypes=[("h5 files", ".h5"),\
                                           ("all files", "*,*")])

    if files != None:
        for eachFile in files:
            file = lk.File(eachFile)

            for name, kymo in file.kymos.items():

                traces, allRedTraces = traceAndExtractSignal(kymo)

                for i in range(len(traces)):
                    exportListOfListToFile([traces[i].seconds,\
                                       traces[i].position,\
                                       allRedTraces[i]],\
                                      str(eachFile) + "_" + str(i) + ".csv")
                    saveFigureForTrace(kymo,\
                                       traces[i],\
                                       allRedTraces[i],\
                                       str(eachFile) + "_" + str(i) + "_plot.tiff",\
                                       extractSignalFromChannel = "red")



def createLinesOfEntries(entryList, root, startRow):
    dictOfEntryObjects = {}
    
    for i in range(len(entryList)):
        tk.Label(root, text=entryList[i][0]).grid(column=0, row=i+startRow)

        currEntry = tk.Entry(root)
        currEntry.insert(0, str(entryList[i][1]))
        currEntry.grid(column=1, row=i+startRow)

        dictOfEntryObjects[entryList[i][0]] = [currEntry, str(entryList[i][1])]

    return dictOfEntryObjects

def readEntryValues(dictOfEntryObjects):
    for eachKey in dictOfEntryObjects.keys():
        dictOfEntryObjects[eachKey][1] = dictOfEntryObjects[eachKey][0].get()


def changeState(btn1):
    if (btn1['state'] == NORMAL):
        btn1['state'] = DISABLED
    else:
        btn1['state'] = NORMAL   

def setEntryValues(dictOfEntryObjects):
    for eachKey in dictOfEntryObjects.keys():
        dictOfEntryObjects[eachKey][0].delete(0, 'end')
        dictOfEntryObjects[eachKey][0].insert(0, str(dictOfEntryObjects[eachKey][1]))

def interactiveGUI():

    root = tk.Tk()

    root.title("Kymograph Live Tracker")
    root.geometry("500x450")

    returnedValues = {}
    

    listOfEntries = [["Channel Traced", "blue"],\
                     ["Channel Signal To Extract", "red"],\
                     ["Track Width", 1],\
                     ["Pixel Threshold", 1],\
                     ["Window", 12],\
                     ["Average Pixel Length", 2],\
                     ["Track Rect Left", 0],\
                     ["Track Rect Up", 6],\
                     ["Track Rect Right", 20],\
                     ["Track Rect Down", 20],\
                     ["Filter Traces", 10]]

    dictOfEntryObjects = createLinesOfEntries(listOfEntries,\
                                              root,\
                                              4)

    def openFile():
        returnedValues["openFile"] = tkfd.askopenfilename(title="choose the source h5 file",\
                                                       filetypes=[("h5 files", ".h5"),\
                                                                  ("all files", "*,*")])
        h5File = returnedValues["openFile"]
    
        if h5File != "":
            h5Parsed = lk.File(h5File)

            name, kymo = h5Parsed.kymos.popitem()
            kymo.plot(channel="rgb",\
                      aspect="auto",\
                      adjustment=lk.ColorAdjustment(0, 1))

            returnedValues["kymo"] = kymo
            
            red = kymo.get_image(dictOfEntryObjects["Channel Signal To Extract"][1])
            kymoActualDuration = red.shape[1] * kymo.line_time_seconds

            dictOfEntryObjects["Track Rect Right"][1] = kymoActualDuration
            setEntryValues(dictOfEntryObjects)

            trackButton["state"] = tk.NORMAL
            upLeftButton["state"] = tk.NORMAL
            downRightButton["state"] = tk.NORMAL
            plt.show()

            
            

               

    tk.Button(root,\
              text = "Open",\
              command = openFile).grid(column=0, row=0)

    tk.Label(root,\
             text = "Number of traces = ").grid(column=0, row=1)

    numOfTracesLabel = tk.Label(root,\
                                text = "0")
    numOfTracesLabel.grid(column=1, row=1)
    
    
    def trackKymograph():
        readEntryValues(dictOfEntryObjects)

        kymo = returnedValues["kymo"]

        plt.cla()
        plt.clf()

        kymo.plot(channel="rgb",\
                  aspect="auto",\
                  adjustment=lk.ColorAdjustment(0, 1))
        

        traces = traceKymo(kymo,\
                          averagingPxLengths = int(dictOfEntryObjects["Average Pixel Length"][1]),\
                          tracedChannel = dictOfEntryObjects["Channel Traced"][1], \
                          trackWidth = float(dictOfEntryObjects["Track Width"][1]),\
                          pixelThreshold =float(dictOfEntryObjects["Pixel Threshold"][1]),\
                          window = int(dictOfEntryObjects["Window"][1]),\
                          RectLeft = float(dictOfEntryObjects["Track Rect Left"][1]),\
                          RectUp = float(dictOfEntryObjects["Track Rect Up"][1]),\
                          RectRight = float(dictOfEntryObjects["Track Rect Right"][1]),\
                          RectDown = float(dictOfEntryObjects["Track Rect Down"][1]),\
                          FilterTrace = int(dictOfEntryObjects["Filter Traces"][1]))

        for trace in traces:
            plt.plot(trace.seconds, trace.position)

        numOfTracesLabel.configure(text = str(len(traces)))
        returnedValues["traces"] = traces

        exportButton["state"] = tk.NORMAL
        plt.show()
        
        
    
    trackButton = tk.Button(root,\
                            text = "Track",\
                            command = trackKymograph,\
                            state = tk.DISABLED)
    trackButton.grid(column=1, row=0)
    
    def importSettings():
        importSettingsFromCSV(dictOfEntryObjects)
        
    tk.Button(root,\
              text = "Import Settings",\
              command = importSettings).grid(column=0, row=2)

    
    def exportTracks():
        readEntryValues(dictOfEntryObjects)
        
        kymo = returnedValues["kymo"]
        traces = returnedValues["traces"]

        for i in range(len(traces)):
            extractedSignalFromTrace = extractSignalFromTrace(kymo,\
                                                              traces[i],\
                                                              signalChannel = dictOfEntryObjects["Channel Signal To Extract"][1],
                                                              averagingPxLengths = int(dictOfEntryObjects["Average Pixel Length"][1]))
        
        

            maximumLagFrames = 200

            exportListOfListToFile([traces[i].seconds, traces[i].position, extractedSignalFromTrace],\
                          filename = str(returnedValues["openFile"]) + "_Trace_" + str(i) + ".csv")
            MSDofTrace = traces[i].msd(max_lag=maximumLagFrames)
            exportListOfListToFile([list(MSDofTrace[0]), list(MSDofTrace[1])],
                        filename = str(returnedValues["openFile"]) + "_Trace_" + str(i) + "_MSD.csv")
            saveFigureForTrace(kymo,\
                                       traces[i],\
                                       extractedSignalFromTrace,\
                                       str(returnedValues["openFile"]) + "_Trace_" + str(i) + "_plot.tiff",\
                                       extractSignalFromChannel = dictOfEntryObjects["Channel Signal To Extract"][1],\
                                       maximumLagFrames=maximumLagFrames)
            
        filename = str(returnedValues["openFile"]) + "_settings.csv"
        exportSettingsFromDict(dictOfEntryObjects, filename)
        trackButton["state"] = tk.DISABLED
        upLeftButton["state"] = tk.DISABLED
        downRightButton["state"] = tk.DISABLED
        exportButton["state"] = tk.DISABLED
        
        # forced garbage collection to free memory from pyplot
        plt.clf()
        plt.close("all")
        gc.collect
    
        
    exportButton = tk.Button(root,\
                              text = "Export Tracks",\
                              command = exportTracks,\
                              state = tk.DISABLED)
    exportButton.grid(column=1, row=2)

    def defineUpLeftTrackingRect():
        def on_click(event):
            if event.button is MouseButton.LEFT and event.inaxes:
                dictOfEntryObjects["Track Rect Left"][1] = event.xdata
                dictOfEntryObjects["Track Rect Up"][1] = event.ydata
                setEntryValues(dictOfEntryObjects)
                plt.disconnect(bindingID)
        bindingID = plt.connect("button_release_event", on_click)
        
        
    upLeftButton = tk.Button(root,\
                             text = "Up Left Point of the Tracking Rect",\
                             command = defineUpLeftTrackingRect,\
                             state = tk.DISABLED)
    upLeftButton.grid(column=0, row=3)

    def defineDownRightTrackingRect():
        def on_click(event):
            if event.button is MouseButton.LEFT and event.inaxes:
                dictOfEntryObjects["Track Rect Right"][1] = event.xdata
                dictOfEntryObjects["Track Rect Down"][1] = event.ydata
                setEntryValues(dictOfEntryObjects)
                plt.disconnect(bindingID)
        bindingID = plt.connect("button_release_event", on_click)
        
        
    downRightButton = tk.Button(root,\
                                text = "Down Right Point of the Tracking Rect",\
                                command = defineDownRightTrackingRect,\
                                state = tk.DISABLED)
    downRightButton.grid(column=1, row=3)
    
    root.mainloop()
    
if __name__ == "__main__":
    interactiveGUI()

    # headlessBatchProcessing()

