# SafeNote——一种基于Note.ms的安全存储库
## 介绍
SafeNote是由CleanNote组织研发的开源Note.ms安全存储库，支持多命名空间，通过sha256算法生成地址并且AES加密内容来保护你的页面，任何没有密钥的人都无法访问。
## 使用方法
SafeNote使用python3编写而成，你只需要安装python3即可使用。
需要的库：
- 标准库
- 第三方库：pycryptodome
- tools.py
### 调用方法
#### 创建对象
使用SafeNote之前需要创建SafeNote对象。
`SafeNote(namespace='',key=b'')`
其中，`namespace`参数代表你需要的命名空间，可以使用unicode字符，`key`代表命名空间的密钥，bytes类型。
不一样的`key`将会导致你访问到不同的命名空间。
例如：
`obj=SafeNote('test',b'114514')`
#### 设置内容
设置内容需要提供页面名称和内容。
`obj.post(name,st,namespace,key)`
其中，name为页面名称，st为设置的内容，namespace为命名空间，key为密钥。
后两个参数可以不提供，默认为你创建对象时设置的。
返回值：实际的页面地址
#### 获取内容
获取内容需要提供页面名称。
`obj.get(name,namespace,key)`
其中，name为页面名称，namespace为命名空间，key为密钥。
后两个参数可以不提供，默认为你创建对象时设置的。
返回值：页面内容或者None
如果获成功，返回页面内容(bytes类型)，否则返回None。
