# Message.xml

## Keywords
- interface
- datafield
- enumeration
- complex
- message

## Interfaces
The message indicates that the conversation will be conducted via the channel and keeps the information about it

### Interface Attributes
```xml
<interface bitOrder='Intel' 
           inByteOrder='BigEndian' 
           outByteOrder='LittleEndian' 
           interfaceSettings='127.0.0.0:8080' 
           interfaceType='TCP_SERVER' 
           name='MessageInputOutput' description="description for">
```

#### Bit Order
Intel or Motorola

#### Byte Order
There are two byte order in theese **inByteOrder** and **outByteOrder**

The values it can take are **LittleEndian** and **BigEndian**

#### Interface Settings
The feature that has ip and port information

Keyword is **interfaceSettings**

#### Interface Type
- TCP_SERVER
- TCP_CLIENT
- UDP_RECEIVER
- UDP_SENDER
- UDP_MULTICAST

### Interface Nodes
```xml
<packet name='MsgName' rx='true' />
```

## Datafield
```xml
<datafields name='datafield'>
  <data>
  ...
</datafields>
```

### Datafield Nodes Attiributes
```xml
<data dataFormatType='bnr' 
      dataType='uint' 
      name='sInt8Type'  
      minValue='-128' 
      maxValue='127' 
      size='8' 
      resolution='' 
      description='' />
```
