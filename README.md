# 无忧签（WuyouSign）

在自己的 iPhone 上完成应用的签名、安装与续签，不需要电脑一直连着。

- 免费 Apple ID 签出的应用 **7 天到期**，无忧签会在到期前自动用当初签名的那账号续上。
- 安装通道走设备本机，电脑只用来导出一次配对文件。

## 下载

最新版本在 [Releases](../../releases/latest) 里，文件名形如 `无忧签_x.y.z.ipa`。

安装前请确认：

| 项 | 要求 |
|---|---|
| iOS | 15.0 及以上 |
| 配对文件 | iOS 17+ 可用「免电脑配对」；**iOS 16 及更早必须用电脑导出配对文件**，再在「配对」页导入 |
| 隧道 | 需要外部隧道 App（如 StosVPN / LocalDevVPN），免费个人证书拿不到 Network Extensions，App 不会内置隧道 |

> 覆盖安装请**不要先卸载**：记录、配对文件、Apple ID 登录态都在应用内，卸载会一起清掉。

## 遇到问题

请到 [Issues](../../issues/new/choose) 提交，选对应模板。

**Bug 模板里那几项一定要填**，否则很难定位：

1. App 版本（「设置 → 关于」里能直接看到，形如 `8.2.1 (8210)`）
2. iOS 版本与机型（设置 → 通用 → 关于本机）
3. 出问题的那一步（配对 / 装应用 / 续签 / 连接通道）
4. 「设置 → 诊断日志」里的相关几行（把里面出现的 Apple ID 打码再贴）
5. 截图（报错弹窗、界面异常）

## 源

无忧签只认 AltStore / SideStore 标准源格式（一份 JSON）。

两种用法，效果一样：

1. **地址**：在「源 → 添加源」里填源地址。
   - 主地址（国内可达）：`https://fastly.jsdelivr.net/gh/CISSIOS/WuyouSign@main/source/apps.json`
   - 备用地址：`https://gcore.jsdelivr.net/gh/CISSIOS/WuyouSign@main/source/apps.json`
   - GitHub 原始地址：`https://raw.githubusercontent.com/CISSIOS/WuyouSign/main/source/apps.json`
   - 官方站点的地址：`https://wuyouqian.top/apps.json`
2. **手动导入**：把本仓库的 [`source/apps.json`](source/apps.json) 下载到「文件」App，在「源 → 添加源 → 从文件导入 apps.json」里选它。
   地址打不开、服务器换域名、只拿到一份 JSON 的时候用这个。导入后和网络源一样可以刷新、可以删；同名文件重复导入等于更新。

手动导入的源里，每个应用的 `downloadURL` 必须是**完整的 http(s) 地址**——源包本身不带 ipa，相对路径装不上，导入时就会直接提示。

### 只有一个 IPA，没有源？

源里没有的应用照样能装：**「我的应用」右上角 `+` → 选 `.ipa` 文件**。

App 会读出包里的 Bundle ID、名称、版本，把它存进 App 内（`LocalIPAs/`），用你的 Apple ID 重新签名后直接装到设备。
存下来的包也会进目录，所以 7 天到期可以照常续签，不用每次重新找文件。

（本地导入的包不会上传到任何地方，只在这台设备上。）


## 目录

```
source/apps.json          # 官方源包，可直接手动导入
.github/ISSUE_TEMPLATE/   # 问题反馈模板
```
