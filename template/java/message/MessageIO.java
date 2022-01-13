package message;

import java.io.IOException;
import java.net.*;
import java.nio.*;

class MessageIO {
    private static final INVALID_PORT = -1;
    private Socket socket;
    protected ByteOrder order = ByteOrder.BIG_ENDIAN;
    public Queue<Byte> headerQueue = new LinkedList<>();
    public Queue<Byte> contentQueue = new LinkedList<>();
    public Queue<Byte> bitQueue = new LinkedList<>();
    
    public void setSocket(Socket socket) {
        this.socket = socket;
    }
    
    public Socket getSocket() {
        return this.socket;
    }
    
    public Socket getPort() {
        return (null != socket) ? socket.getPort : INVALID_PORT;
    }
    
    public Socket getLocalPort() {
        return (null != socket) ? socket.getLocalPort : INVALID_PORT;
    }
    
    public byte getByte(Socket socket) {
        byte[] bArray = new byte[Byte.BYTES];
        if (!headerQueue.isEmpty()) {
            return headerQueue.poll();
        }
        
        if (!contentQueue.isEmpty()) {
            return contentQueue.poll();
        }
        
        try {
            int result = socket.getInputStream().read(bArray, 0, Byte.BYTES);
            if (result == -1) {
                // disconnet
            } else {
                return ByteBuffer.wrap(bArray).get();
            }
        } catch (SocketException e) {
            e.printStackTree();
        } catch (SocketTimeoutException e) {
            e.printStackTree();
        } catch (IOException e) {
            e.printStackTree();
        }
        
        return Byte.MIN_VALUE;
    }
}