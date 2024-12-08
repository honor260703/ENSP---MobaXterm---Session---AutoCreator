# ENSP---MobaXterm---Session---AutoCreator
本仓库存储的项目旨在通过Python脚本实现自动创建连接到ENSP模拟器的MobaXterm会话文件。这一功能极大地提高了在网络环境模拟和测试场景下，建立连接的效率，避免了手动创建会话的繁琐过程。
## 解答
### 这个脚本能干什么？有什么意义？
通过运行此脚本，能够生成一个名为“MobaXterm Sessions.mxtsessions”的MobaXterm会话文件，进而实现批量创建连接至ENSP模拟器的Telnet会话，无需手动创建。此外，该脚本还可生成名为“设备信息表”的xlsx表格，表格内容包含设备名、设备端口号、设备MAC地址、SN码以及设备ID。 从第三方远程连接工具连接到网络设备的CLI（命令行界面）之后，能够更直观地查看设备输出信息，如下所示：
