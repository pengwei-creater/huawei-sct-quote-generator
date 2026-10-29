# 各产品线配置模板

写 `rows[].config` 时按对应模板逐行填写，单位、数量、格式见 [rules.md](rules.md)。

## 全闪存 OceanStor Dorado 3000/5000/8000

```
机箱：OceanStor Dorado XXX(2U,双控,NVME,交流240V高压直流,25*Palm,SPE62C0225,V7)
缓存：XXXGB
接口：8*1Gb ETH、8*10Gb ETH(含多模SFP+)、2*4端口 DPU-Based SmartIO I/O模块(SFP28,32Gb FC)
硬盘：X*3.84TB SSD NVMe Palm硬盘单元(7")
软件：SAN功能包使用许可(含Thin,Snap,Replication,...)、UltraPath SAN主机多路径使用许可
维保：五年原厂质保
```

- 缓存单独成行，不在机箱行重复。
- FC 模块注明端口数与速率：`(SFP28,32Gb FC)` 或 `(SFP+,16Gb FC)`。

## 混合存储 OceanStor 5210/5310/5510

```
机箱：XXX(2U,双控,SAS,交流240V高压直流,4*SAS3.0端口,25*2.5英寸SAS,SPE26C0225)
缓存：XXXGB
接口：8*1Gb ETH、4*10Gb ETH(含多模SFP+)、2*4端口 SmartIO I/O模块(SFP+,16Gb FC)
硬盘：X*16TB NL SAS、X*3.84TB SSD SAS
扩展柜：1*SAS硬盘框(4U,24盘位)
软件：SAN&NAS高级包
维保：五年原厂质保、介质保留服务
```

## 分布式存储 OceanStor Pacific 9520/9920/9928

```
本次共X节点，以下为单节点配置：
机箱：OceanStor Pacific 9520(2U,12*3.5",K22R-02)
CPU：2*kunpeng920(32C 2.6GHz)
电源：2*900W 交流电源
内存：8*32GB DDR4
硬盘：2*480GB SSD SATA(2.5")、2*3.2TB SSD NVMe(2.5")、12*8TB 7.2K SATA(3.5")
网口：4*GE、4*10GE
软件：块存储标准版软件
维保：三年标准+原厂质保
```

- 机箱括号只保留形态要素（盘位、BBU、机型码）；CPU 与网口剥离成行。
- CPU 型号**必须核实**（并非都是鲲鹏 920）。
- 网口速率依光模块判定，按速率分别列出。

## AI 服务器 Atlas 800 (Model 3000)

```
机箱：Atlas 800 (Model 3000),8*2.5英寸硬盘机箱,K22R-02
CPU：2*鲲鹏920 64Core@2.6GHz
电源：2*2000W 交流电源
内存：16*32GB DDR4
硬盘：2*1920GB SATA SSD、6*3840GB SATA SSD
RAID卡：RAID标卡-PCIE 3.0 X8-2GB cache
网口：4*GE
IO扩展：IO扩展模组
维保：五年原厂金牌质保、介质保留服务
```

## 超融合 FusionCube 1000H-T2 / 1000H-X4

```
本次共X节点(主站点X节点+备站点X节点)，以下为单节点配置：
机箱：超融合节点-DP2220(12*3.5英寸硬盘EXP机箱)
CPU：2*C6530(2.1GHz/32-Core/160MB/270W)
电源：2*2000W 交流电源
内存：8*64GB DDR5 5600MHz
硬盘：2*480GB SSD SATA(2.5")、2*1.92TB SSD SAS(3.5")、4*16TB 7.2K SATA(3.5")
RAID卡：9560-8i RAID标卡(PCIe 4.0 x8,4GB Cache,支持超级电容)
网卡：2*GE、6*10GE(含多模光模块)
软件：虚拟化套件高级版许可-6CPU、基础架构软件Capacity高级版许可-6CPU
服务：含规划实施服务、硬件安装服务、三年标准+质保
```

- 硬盘合并一行（系统盘→缓存盘→数据盘，容量升序）。
- 软件只写许可名称与 CPU 数，3 年订阅不单列。
- 服务与维保合并成一行。
- 名称默认不写「含 DCS 虚拟化」，DCS 许可并入软件行。
- 备注写 RAID 后可用容量，如「做Raid6，一块热备，可用容量：65TiB」。

## 备份一体机 OceanProtect X 系列

```
本次共X节点，以下为单节点配置：
机箱：OceanProtect X3000(2U,双控,SAS,交流240V高压直流,12*3.5英寸SAS,SPE26C0212)
缓存：256GB
硬盘：4*3.84TB SSD SAS(3.5")、8*16TB 7.2K NL SAS(3.5")
接口：8*1Gb ETH、4*10Gb ETH(含多模SFP+)
软件：备份存储基础容量许可增强版(含40TB)、备份存储容量许可增强版(88TB)、软件3年升级支持服务
服务：OceanProtect X系列安装服务
维保：三年标准质保
```

## 数通产品（交换机/路由器/AP/安全网关）

这类产品的 BOM 只有基础信息，需要从官网「技术规格」页取参数，填进备注或单独一列：

- 交换机：交换容量、包转发率、接口规格、国产化芯片、路由/管理协议、实配信息、3 年质保
- AP：Wi-Fi 标准、频段、空间流速率、安装方式、芯片、天线、蓝牙、PoE、3 年质保
- 路由器：交换容量、包转发率、WAN/LAN 接口、实配授权、3 年质保
