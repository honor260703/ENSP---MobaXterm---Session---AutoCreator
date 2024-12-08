# 使用说明

```
#作者：黄荣彬
#邮箱：2607037721@qq.com
#哔哩哔哩：啥也不会黄某人（https://space.bilibili.com/96001203）
#编写日期：2024-12-06
#编写地点：家
#总算有一份我觉得算是拿得出手的Github项目啦（丢人）
```

## 解答

### 这个脚本能干什么？有什么意义？

通过运行此脚本，能够生成一个名为“MobaXterm Sessions.mxtsessions”的MobaXterm会话文件，进而实现批量创建连接至ENSP模拟器的Telnet会话，无需手动创建。此外，该脚本还可生成名为“设备信息表”的xlsx表格，表格内容包含设备名、设备端口号、设备MAC地址、SN码以及设备ID。 从第三方远程连接工具连接到网络设备的CLI（命令行界面）之后，能够更直观地查看设备输出信息，如下所示：

![5e9bce01242470800628e067aff45469](./5e9bce01242470800628e067aff45469.jpg)

### Mobaxterm连接后回车显示M如何解决？ 

在MobaXterm程序所在的路径下找到MobaXterm.ini文件并新增代码即可解决问题

```
[MottyOptions]
LocalEcho=1
LocalEdit=1
```

![image-20241206115457756](./image-20241206115457756.png)

### 我该怎么使用这个项目？

很简单，你只需要把topo_messages.py脚本下载下来并放到保存的拓扑文件夹内，再执行一下脚本就行了。

## 使用示范

**注：需要Python环境**

将topo_messages.py脚本（原名topo_fanyi.py，我不想重新截图了）移动至保存的拓扑文件夹内，并在地址栏内输入cmd（或者你也可以通过VS Studio code、Pycharm等方式直接运行脚本）并回车打开命令提示符

![image-20241206113309723](./image-20241206113309723.png)

执行命令python topo_messages.py后，会在当前拓扑文件夹内生成表格文件和MobaXterm会话文件。

![image-20241206113638626](./image-20241206113638626.png)

打开MobaXterm程序，如下图所示，右键User session选择Import session from file选项

![{BD63A6ED-8288-4795-96EB-07950C212D90}](./{BD63A6ED-8288-4795-96EB-07950C212D90}.png)

选择生成的MobaXterm会话文件

![image-20241206114021564](./image-20241206114021564.png)

Yes

![image-20241206114038133](./image-20241206114038133.png)

![image-20241206114225200](./image-20241206114225200.png)

![image-20241206114416992](./image-20241206114416992.png)