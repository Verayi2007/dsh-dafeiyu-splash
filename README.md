# 大肥鱼开屏 · dsh-dafeiyu-splash

给 **DeepSeek Harness** 做的一段全屏开屏动效：点开之后，**大肥鱼娘**从水下浮上来 —— 先是雾里的人影，然后落定、泛光、一道高光从她身上掠过，最后 `DeepSeek` 字标落款。约 3.7 秒，随时可以跳过。

纯客户端插件：不注册服务、不加工具、不联网、不读会话。

<p align="center">
  <img src="docs/preview.png" width="820" alt="开屏定格：鲸鱼娘 + DeepSeek 字标">
</p>

<p align="center"><sub>上图为 <code>preview/preview.html</code> 在浏览器里定格到第 3.4 秒的截图，不是插件在 DSH 里的实拍。</sub></p>

## 时间轴

| 时间 | 发生什么 |
| --- | --- |
| 0 – 0.9s | 幕布亮起，一道斜光从水面透下来，四角压暗 |
| 0.2 – 1.7s | 她身后的冷光亮起，一圈细环像水里的回响一样扩散 |
| 0.3 – 1.9s | **上浮**：从模糊的景深里升起来（14px 模糊 → 0），脚下的水面光同时铺开 |
| 1.35 – 4.0s | 气泡错峰上浮 |
| 1.5 – 2.9s | **高光斜扫**：一道白光沿她身体掠过 —— 用她的 alpha 当遮罩，光只落在人身上，不会糊到背景 |
| 1.9 – 3.25s | **落款**：`DeepSeek` 字距从 0.64em 收到 0.42em 上浮，细线展开，`深度求索` 淡入 |
| 2.52s 起 | 三个信号点开始脉动，表示还在加载 |
| 3.1s | 收幕：整幕淡出（0.56s），3.66s 卸载，指针事件全部归还 |

## 交互

- **随时跳过**：点击 / 触摸任意位置，或按任意键、滚一下滚轮，立刻收幕。
- **自动收场**：即使脚本出错，CSS 也会把这一幕走完，不会挡着界面。
- **一次页面加载只放一次**：SPA 内的路由切换、会话切换都不会重放。
- **跟随系统「减弱动态效果」**：`prefers-reduced-motion: reduce` 时只留一次极简淡入，扫光和气泡全部不出现。

## 安装

```bash
# 从 GitHub 装（tarball，不依赖 git 协议）
dsh plugin --profile desktop add "https://codeload.github.com/Verayi2007/dsh-dafeiyu-splash/tar.gz/refs/heads/main"

# 或者先克隆，再按本地目录装
git clone https://github.com/Verayi2007/dsh-dafeiyu-splash
dsh plugin --profile desktop add "link:/绝对/路径/dsh-dafeiyu-splash"
```

装完 **刷新一次界面**（客户端 bundle 在页面加载时注入）；桌面版建议直接重启一次 DSH。

卸载：

```bash
dsh plugin --profile desktop remove dsh-dafeiyu-splash
```

## 改一改

在页面控制台里（或你自己的注入脚本里）覆盖任意一项，下一次加载生效：

```js
window.__DAFEIYU_SPLASH__ = {
  disabled: true,        // 这一次不放
  duration: 3100,        // 开始收幕的时间（毫秒）
  title: "DeepSeek",     // 主字标
  subtitle: "深度求索",  // 副标，给空串则隐藏
  hint: "点击任意位置继续"
};
```

诊断：阶段写在 `<html data-dafeiyu-splash>` 上 —— `playing` / `leaving` / `done`；浮层节点是 `[data-plugin="dsh-dafeiyu-splash"]`。

## 换角色 / 改画面

- **换角色**：把 `assets/feiyu.webp` 换成你自己的透明底立绘（方形、长边 700–800px 最好），重新 `python tools/build.py`。
- **改节奏**：`src/splash.css` 顶部的注释写了每一拍的毫秒数，改 `animation-delay` 就是改时间轴。
- **一份源码，两个落点**：`src/` 由 `tools/build.py` 编译成
  - `preview/preview.html` —— 免安装预览页，浏览器直接打开，`?t=1800` 定格到第 1800 毫秒；
  - `client.js` —— 插件用的自包含客户端模块（图以 base64 内嵌，单文件、零外部请求）。

```
src/splash.css       视觉与时间轴（全部动画都在这里）
src/splash.body.html 结构：立绘 + 光晕 + 高光 + 气泡 + 字标
src/runtime.js       挂载 / 跳过 / 收幕
assets/feiyu.webp    角色立绘（CC BY-NC-SA 4.0，见 assets/README.md）
tools/build.py       生成预览页与 client.js
tools/prep_art.py    立绘裁边、缩放、转 WebP
```

## 许可

- **代码**：[MIT](LICENSE) © 2026 Verayi2007
- **角色立绘**（`assets/feiyu.webp`）：社区二创的 DeepSeek 鲸鱼娘，[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)，**不可商用**。详见 [assets/README.md](assets/README.md)。
