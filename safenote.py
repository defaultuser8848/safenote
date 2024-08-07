import base64
from hashlib import sha256
import struct
from Crypto.Cipher import AES
import tools
import asyncio
class SafeNote(object):
    def __init__(self,namespace='',key=b''):
        self.namespace=namespace
        self.key=key
    @staticmethod
    def convert(namespace,name,key=b''):
        namespace=namespace.encode()
        st=name.encode()
        f=sha256(b'%s::%s#%s'%(namespace,st,key)).digest()
        return ''.join(filter(lambda x:x not in "+=/",base64.b64encode(f).decode()))
    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += b'\0'
        return value
    @staticmethod
    def encrypt(st,key):
        key=sha256(key).digest()
        st=sha256(st).digest()+st
        st=struct.pack('!I',len(st))+st
        st=SafeNote.add_to_16(st)
        return base64.b85encode(AES.new(key,AES.MODE_ECB).encrypt(st)).decode()
    @staticmethod
    def decrypt(st,key):
        try:
            key=sha256(key).digest()
            f=base64.b85decode(st)
            
            x=AES.new(key,AES.MODE_ECB).decrypt(f)
            l=struct.unpack("!I",x[:4])[0]
            f=x[4:4+l]
            
            h=f[:32]
            v=f[32:]
        except:
            return None
        if sha256(v).digest()!=h:
            return None
        return v
        
    async def post(self,name,st,namespace=None,key=None):
        if namespace is None:
            namespace=self.namespace
        if key is None:
            key=self.key
        page=self.convert(namespace,name,key)
        await tools.setContent(page,self.encrypt(st,key))
        return page
    async def get(self,name,namespace=None,key=None):
        if namespace is None:
            namespace=self.namespace
        if key is None:
            key=self.key
        page=self.convert(namespace,name,key)
        f=await tools.getContent(page)
        return self.decrypt(f,key)
    async def clean(self,name,namespace=None,key=None):
        if namespace is None:
            namespace=self.namespace
        if key is None:
            key=self.key
        page=self.convert(namespace,name,key)
        await tools.setContent(page,'')
        return page
    @staticmethod
    def to_sync(x):
        return asyncio.get_event_loop().run_until_complete(x)
