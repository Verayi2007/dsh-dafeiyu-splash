# 大肥鱼开屏 · dsh-dafeiyu-splash

给 **DeepSeek Harness** 做的一段开屏动画：**大肥鱼娘先从屏幕底边探出个头，看清是你，一下冲到面前占满整屏，再萌萌地退回舞台、缩回原大小，冲你挥手说「嗨～」。**

纯客户端插件：不注册服务、不加工具、不联网、不读会话。

<p align="center">
  <img src="docs/preview.png" width="820" alt="冲到面前：她占满整屏的那一拍">
</p>

<p align="center"><sub>她冲到面前的那一拍（<code>preview/preview.html?t=2000</code>）。</sub></p>

<p align="center">
  <img src="docs/preview-end.png" width="620" alt="落定：挥手、打招呼、字标">
</p>

<p align="center"><sub>落定的样子（<code>?t=4300</code>）：挥手 + 「嗨～」+ 字标。</sub></p>

## 五拍

| 时间 | 发生什么 |
| --- | --- |
| 0 – 0.5s | 幕布亮起，斜光落下，四角压暗 |
| 0.5 – 1.2s | **探头**：她从屏幕底边升上来，只露一颗头，光晕跟着她的头一起沉到底部 |
| 1.2 – 1.6s | 停一下、微微歪头，然后**往下一缩**（蓄力） |
| 1.6 – 2.4s | **冲满屏**：一下顶到面前，脸占满整幅画面，白光闪一下（这一拍是整段的重点） |
| 2.4 – 2.9s | **退回来**：缩回原大小、落回舞台，带一点过冲和回弹 |
| 2.9 – 4.3s | **打招呼**：左右晃两下（挥手），旁边弹出「嗨～」气泡；2.9s 字标落款、3.05s 一道高光扫过 |
| 3.8s 起 | 三个信号点脉动，表示还在加载 |
| 4.6s | 收幕淡出（0.56s），5.16s 卸载，指针事件全部归还 |

整段镜头是一条 5000ms 的关键帧（`.dfy-camera`）驱动的：探头、蓄力、满屏、退回都在这一条上；光晕、气泡、字标、信号点挂在同一根时间轴上按拍子错开。

## 交互

- **随时跳过**：点击 / 触摸任意位置，或按任意键、滚一下滚轮，立刻收幕。
- **自动收场**：即使脚本出错，CSS 也会把这一幕走完，不会挡着界面。
- **一次页面加载只放一次**：SPA 内的路由切换、会话切换都不会重放。
- **跟随系统「减弱动态效果」**：`prefers-reduced-motion: reduce` 时不做镜头运动，只留一张定格的她 + 字标。

## 安装

```bash
# 从 GitHub 装（tarball，不依赖 git 协议）
dsh plugin --profile desktop add "https://codeload.github.com/Verayi2007/dsh-dafeiyu-splash/tar.gz/refs/heads/main"

# 或者先克隆，再按本地目录装
git clone https://github.com/Verayi2007/dsh-dafeiyu-splash
dsh plugin --profile desktop add "link:/绝对/路径/dsh-dafeiyu-splash"
```

装完**重启一次 DSH**（客户端 bundle 在启动时装配）。

卸载：

```bash
dsh plugin --profile desktop remove dsh-dafeiyu-splash
```

> Tarball 装法不会自动把包写进 profile 的 `dsh.profile.bundles`。装完没反应的话，看一眼
> `~/.dsh/profiles/desktop/package.json` 的 `bundles` 里有没有 `dsh-dafeiyu-splash`，没有就手动补一行。

## 改一改

```js
window.__DAFEIYU_SPLASH__ = {
  disabled: true,        // 这一次不放
  duration: 4600,        // 开始收幕的时间（毫秒）
  title: "DeepSeek",     // 主字标
  subtitle: "深度求索",  // 副标，给空串则隐藏
  hint: "点击任意位置继续"
};
```

气泡那句「嗨～」在 `src/splash.body.html` 的 `.dfy-talk` 里，改字就行。

诊断：阶段写在 `<html data-dafeiyu-splash>` 上 —— `playing` / `leaving` / `done`；浮层节点是 `[data-plugin="dsh-dafeiyu-splash"]`。

## 换角色 / 改节奏

- **换角色**：把 `assets/feiyu.webp` 换成你自己的透明底立绘（方形，长边 1000–1200px 最好 —— 要放大到 3 倍占满屏），重新 `python tools/build.py`。
- **改节奏**：所有拍子都在 `src/splash.css` 的 `@keyframes dfy-camera` 里（百分比 × 5000ms 就是毫秒），改那组数字就是改镜头。
- **一份源码，两个落点**：
  - `preview/preview.html` —— 免安装预览页，浏览器直接打开；`?t=2000` 定格到第 2000 毫秒（同步定格，截图不会抓空）；
  - `client.js` —— 插件用的自包含客户端模块（图以 base64 内嵌，单文件、零外部请求）。

```
src/splash.css       视觉与时间轴（镜头、挥手、气泡、字标全在这）
src/splash.body.html 结构：立绘 + 光晕 + 高光 + 气泡 + 字标
src/runtime.js       挂载 / 跳过 / 收幕 / 定格
assets/feiyu.webp    角色立绘（CC BY-NC-SA 4.0，见 assets/README.md）
tools/build.py       生成预览页与 client.js
```

## 许可

- **代码**：[MIT](LICENSE) © 2026 Verayi2007
- **角色立绘**（`assets/feiyu.webp`）：社区二创的 DeepSeek 鲸鱼娘，[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)，**不可商用**。详见 [assets/README.md](assets/README.md)。
