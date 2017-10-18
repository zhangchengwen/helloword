创建内部接口
ovs-vsctl add-br br0   
ovs-vsctl add-port br0 p0 -- set Interface p0 type=internal
#查看网桥br0   
ovs-vsctl show br0
    Bridge "br0"
        fail_mode: secure
        Port "p0"
            Interface "p0"
                type: internal
        Port "br0"
            Interface "br0"
                type: internal
在OVS中，只有”internal”类型的设备才支持配置IP地址信息

#配置端口Ip
ip addr add 192.168.10.11/24 dev br0  等价于  ifconfig eth0 192.168.1.102 netmask 255.255.255.0  //添加IP地址

ip link set br0 up

#添加默认路由
ip route add default via 192.168.10.1 dev br0

//添加网关
route add default gw 192.168.1.1
 
设置tag值需要使用set port
ovs-vsctl set port p0 tag=110

Patch类型的接口
当主机中有多个ovs网桥时，可以使用Patch Port把两个网桥连起来。Patch Port总是成对出现，分别连接在两个网桥上，从一个Patch Port收到的数据包会被转发到另一个Patch Port，类似于Linux系统中的veth。使用Patch连接的两个网桥跟一个网桥没什么区别，OpenStack Neutron中使用到了Patch Port。上面网桥br-ext中的Port phy-br-ext与br-int中的Port int-br-ext是一对Patch Port
可以使用ovs-vsctl创建patch设备，如下创建两个网桥br0,br1，然后使用一对Patch Port连接它们

ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl \
-- add-port br0 patch0 -- set interface patch0 type=patch options:peer=patch1 \
-- add-port br1 patch1 -- set interface patch1 type=patch options:peer=patch0
#结果如下
#ovs-vsctl show
    Bridge "br0"
        Port "br0"
            Interface "br0"
                type: internal
        Port "patch0"
            Interface "patch0"
                type: patch
                options: {peer="patch1"}
    Bridge "br1"
        Port "br1"
            Interface "br1"
                type: internal
        Port "patch1"
            Interface "patch1"
                type: patch
                options: {peer="patch0"}

连接两个网桥不止上面一种方法，linux中支持创建Veth设备对，我们可以首先创建一对Veth设备对，然后把这两个Veth分别添加到两个网桥上，其效果跟OVS中创建Patch Port一样，只是性能会有差别

#创建veth设备对veth-a,veth-b
ip link add veth-a type veth peer name veth-b
#使用Veth连接两个网桥
ovs-vsctl add-port br0 veth-a
ovs-vsctl add-port br1 veth-b








