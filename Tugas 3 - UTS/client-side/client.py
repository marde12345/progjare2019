import socket
import os

class SendingClass() :
    def __init__(self, sock, filetosend, addr):
        self.sock = sock
        self.file = filetosend
        self.target = addr
    
    def sendFile(self, filename):
        print "[.] sending "+ filename +" to " + str(self.target)
        self.sock.send("#start".ljust(1024))
        self.sock.send(filename.ljust(1024))
        fp = open(filename, 'rb')
        while (True):
            payload = fp.read(1024)
            self.sock.send(payload.ljust(1024))
            if not payload:
                break
        self.sock.send("##EOF".ljust(1024))
    
    def directoryCrawler(self, directory):
        self.sock.send("#directoryName".ljust(1024))
        self.sock.send(directory.ljust(1024))
        os.chdir(directory)
        filelist = glob.glob("*")
        for files in filelist:
            
            if os.path.isdir(files):
                self.directoryCrawler( files)
                continue
            self.sendFile(files)
            
        os.chdir("..")
        self.sock.send("#directoryDone".ljust(1024))
            
    
    def run (self):
        print "[.] sending "+ self.file +" to " + str(self.target)
        isdir = os.path.isdir(self.file)
        if (isdir):
            self.sock.send("#directoryStart".ljust(1024))
            self.directoryCrawler(self.file)
            self.sock.send("#directoryEnd".ljust(1024))
        else :
            self.sock.send("#sendingFile".ljust(1024))
            self.sendFile(self.file)
        
        print "[-] finish "+ self.file +" to " + str(self.target)

class Client:
    def __init__(self):
        socketbind = 18000
        ip = "127.0.0.1"
        self.server = (ip, socketbind)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server)
    
    def close(self):
        self.sock.send("#close")
    
    def clientEngineView(self):
        print "\nWelcome!!!"
        print "Menu :"
        print "see"
        print "ls"
        print "download"
        print "upload"
        return raw_input("do -> ")

    def seeEngine(self):
        os.system('cls')
        self.sock.send("#askFiles")
        datas = (self.sock.recv(1024))
        datas = datas.strip()
        datas = datas.replace(' ','')
        datas = datas.replace('[','')
        datas = datas.replace(']','')
        datas = datas.replace('\'','')
        datas = datas.split(',')
                
        ranged = []
        print "./server-side"
        for a in range(len(datas)):
            print ("%s. %s"%(a, datas[a]))
            ranged.append(datas[a])
        print "---------------------------"
        return ranged

    def lsEngine(self):
        os.system('cls')

        print "./client-side"
        arr = os.listdir(".")
        for a in range(len(arr)):
            print "%s. %s"%(a,arr[a])
        print "---------------------------"
        return arr

    def uploadEngine(self):
        datas = self.lsEngine()

        target = raw_input("Ketik angka/indek yang mewakili file : ")
        target = int(target)
        target = datas[target]

        if not target in datas:
            return

        flag = True
        target = str(target)
        self.sock.sendall("#upload")
        send = SendingClass(self.sock, target ,self.server)
        send.run()

    def downloadEngine(self):
        datas = self.seeEngine();  

        target = raw_input("Ketik angka/indek yang mewakili file : ")
        target = int(target)
        target = datas[target]

        if not target in datas:
            return
        
        flag = True
        target = str(target)
        self.sock.sendall("#ask")
        self.sock.send(target)
        data = self.sock.recv(1024)

        
        if ("#sendingFile" in data):
            data = self.sock.recv(1024)
            if ("#start" in data):
                data= self.sock.recv(1024)
                filename = data.strip()
                data = filename.split('/')
                data = data[len(data)-1]
                filename = data
                print ("[+] receiving " + str(filename))
                print filename
                fp = open(filename, "wb+")
                while True:
                    data = self.sock.recv(1024)        
                    
                    if "##EOF" in data:
                        print ("[-] received " + filename )
                        fp.close()
                        break
                    fp.write(data)
        else:
            
            while True:
                
                data = self.sock.recv(1024)
                
                if ("#directoryEnd" in data):
                    print "[-] done"
                    break
                
                elif ("#directoryName" in data):
                    
                    data = self.sock.recv(1024)
                    data = data.strip()
                    if(flag):
                        data = data.split('/')
                        data = data[len(data)-1]
                    print "[+] receiving" +data
                    if (not os.path.exists(data)):
                        os.mkdir(data)
                    os.chdir(data)
                    
                elif ("#directoryDone" in data):
                    print "[-] done"
                    os.chdir('..')
                    
                elif("#start" in data):
                    data= self.sock.recv(1024)
                    filename = data.strip()
                    print ("[+] receiving " + str(filename))
                    print filename
                    fp = open(filename, "wb+")
                    while True:
                        data = self.sock.recv(1024)        
                        
                        if "##EOF" in data:
                            fp.close()
                            break
                        fp.write(data)


    def clientRoute(self):
        while (True):
            
            menu = self.clientEngineView()

            if menu == "lst":
                self.lstEngine()

            if menu == "ls":
                self.seeEngine()
                
            if menu == "download":
                self.downloadEngine()

            if menu == "upload":
                self.uploadEngine()

if __name__ == "__main__":
    try:
        main = Client()
        main.clientRoute()
    except KeyboardInterrupt:
        main.close()
        print("done")