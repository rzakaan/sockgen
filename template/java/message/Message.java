package message;

public abstract class Message extends MessageIO {
    private ByteBufferOutputStream buffer = new ByteBufferOutputStream();
    private Queue<Boolean> bitBuffer = new LinkedList<>();
    
    public abstract byte[] encode();
    public abstract boolean decode();
    
    public void clearBuffer() {
        buffer.reset();
        bitBuffer.clear();
    }
    
    private void write(byte[] bArray) {
        try {
            this.buffer.write(bArray);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    protected byte[] toByteArray() {
        return buffer.toByteArray();
    }
    
    protected void putByte(byte value) {
        byte[] array = ByteBuffer.allocate(Byte.BYTES).order(this.order).put(value).array();
        this.write(array);
    }
    
    protected void putByte(byte[] value) {
        byte[] array = ByteBuffer.allocate(value.length).order(this.order).put(value).array();
        this.write(array);
    }
    
    protected void putShort(short value) {
        byte[] array = ByteBuffer.allocate(Short.BYTES).order(this.order).put(value).array();
        this.write(array);
    }
    
    protected void putShort(float value, float resolution) {
        byte[] tArray = ByteBuffer.allocate(Integer.BYTES).putInt((int) (value / resolution)).array();
        byte[] bArray = new byte[Short.BYTES];
        for (int i = 0; i < Short.BYTES; i++) {
            bArray[i] = tArray[i + 2];
        }
        
        write(ByteBuffer.wrap(bArray).array());
    }
    
    protected void putInt(int value) {
        byte[] array = ByteBuffer.allocate(Integer.BYTES).order(this.order).putInt(value).array();
        this.write(array);
    }
    
    protected void putInt(float value, float resolution) {
        byte[] tArray = ByteBuffer.allocate(Long.BYTES).putInt((int) (value / resolution)).array();
        byte[] bArray = new byte[Integer.BYTES];
        for (int i = 0; i < Integer.BYTES; i++) {
            bArray[i] = tArray[i + 4];
        }
        
        write(ByteBuffer.wrap(bArray).array());
    }
    
    protected void putLong(long value) {
        byte[] array = ByteBuffer.allocate(Long.BYTES).order(this.order).putLong(value).array();
        this.write(array);
    }
    
    protected void putFloat(float value) {
        byte[] array = ByteBuffer.allocate(Float.BYTES).order(this.order).putFloat(value).array();
        this.write(array);
    }
    
    protected void putDouble(double value) {
        byte[] array = ByteBuffer.allocate(Double.BYTES).order(this.order).putDouble(value).array();
        this.write(array);
    }
    
    protected void putASCII(String value) {
        byte[] array = ByteBuffer.allocate(value.length()).order(this.order).put(value.getBytes(StandartCharsets.US_ASCII)).array();
        this.write(array);
    }
    
    protected void putBit(boolean value) {
        bitBuffer.add(value);
        while (bitBuffer.size() >= 8) {
            byte bArray = new byte[1];
            for (int i = 0; i < Byte.BYTES; i++) {
                if (bitBuffer.poll()) {
                    bArray[0] |= 1 << (7 - i);
                }
            }
            
            write(bArray);
        }
    }
}
