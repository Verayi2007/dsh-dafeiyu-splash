# 大肥鱼开屏 · dsh-dafeiyu-splash

给 **DeepSeek Harness** 做的一段全屏开屏动效：点开之后先是一条**大肥鱼**从黑暗里被描出来，然后是形体、高光、字标落款，约 3.7 秒后自动让位给界面。

纯客户端插件，不注册服务、不加工具、不联网、不读你的会话。

<p align="center">
  <img src="docs/preview.png" width="820" alt="开屏定格：鲸鱼成形 + DeepSeek 字标">
</p>

<p align="center"><sub>上图为 <code>preview/preview.html</code> 在浏览器里定格到第 3.4 秒的截图，不是插件在 DSH 里的实拍。</sub></p>

## 四拍

| 时间 | 发生什么 |
| --- | --- |
| 0 – 0.9s | 幕布亮起，一道斜光从上方落下，四角压暗，一圈细光像声呐一样扩散 |
| 0.26 – 1.42s | **描边自绘**：蓝色高光沿鲸鱼轮廓一笔画出（`pathLength=1` + `stroke-dashoffset`） |
| 0.88 – 1.93s | **凝形**：填充从雾里收拢，边光和头顶高光一起亮起，鲸身轻轻落定 |
| 1.42 – 2.72s | **高光斜扫**：一段白光沿身体斜着掠过（被鲸身裁掉，不会溢出） |
| 1.25 – 4.0s | 气泡上浮，错峰出现 |
| 1.88 – 3.25s | **落款**：`DeepSeek` 字距从 0.64em 收到 0.42em 上浮，细线展开，`深度求索` 淡入 |
| 2.54s 起 | 三个信号点开始脉动，表示还在加载 |
| 3.1s | 收幕：整幕淡出（0.56s），3.66s 卸载，指针事件全部归还 |

## 交互

- **随时跳过**：点击 / 触摸任意位置，或按任意键、滚一下滚轮，立刻收幕。
- **自动收场**：即使脚本出错，CSS 也会把这一幕走完，不会挡着界面。
- **一次页面加载只放一次**：SPA 内的路由切换、会话切换都不会重放。
- **跟随系统「减弱动态效果」**：`prefers-reduced-motion: reduce` 时只留一次极简淡入，描边、扫光、气泡全部不出现。

## 安装

```bash
# 从 GitHub 装
dsh plugin --profile desktop add "github:Verayi2007/dsh-dafeiyu-splash"

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

在页面控制台里（或你自己的注入脚本里）可以覆盖任意一项，改完下一次加载生效：

```js
window.__DAFEIYU_SPLASH__ = {
  disabled: true,        // 这一次不放
  duration: 3100,        // 开始收幕的时间（毫秒）
  title: "DeepSeek",     // 主字标，换空串就是一个纯图形开场
  subtitle: "深度求索",  // 副标，给空串则隐藏
  hint: "点击任意位置继续"
};
```

诊断：动画阶段写在 `<html data-dafeiyu-splash>` 上——`playing` / `leaving` / `done`；浮层节点是 `[data-plugin="dsh-dafeiyu-splash"]`。

## 视觉是怎么来的

- **鲸鱼轮廓**：从 DSH 自带的图标 `resources/icon.png` 里描出来的——`tools/trace_whale.py` 用 OpenCV 取外轮廓与镂空（腹部、眼睛），再用 Catmull-Rom 转成三次贝塞尔，最终是一份约 7KB 的纯矢量路径。所以放大到任何尺寸都是清晰的，也不带任何位图依赖。
- **一份源码，两个落点**：`src/splash.css` + `src/splash.body.html` + `src/runtime.js` 由 `tools/build.py` 编译成
  - `preview/preview.html`（免安装预览页，浏览器直接打开；
  - `client.js`（插件用的自包含客户端模块）。
  
  预览页支持 `?t=1800` 定格到第 1800 毫秒，方便逐帧调。

```
src/splash.css       视觉与时间轴（全部动画都在这里）
src/splash.body.html 结构：SVG 鲸鱼 + 字标 + 气泡 + 信号点
src/runtime.js       挂载 / 跳过 / 收幕
tools/trace_whale.py 图标 -> SVG 路径
tools/build.py       生成预览页与 client.js
```

重新构建：

```bash
python tools/trace_whale.py   # 需要 icon.png 的路径（默认读本机安装目录）
python tools/build.py
```

## 说明

- 不注册服务、不加工具、不联网；除一个 `shell.overlay` 槽位条目外不改动应用。
- 颜色是画面自己的（深蓝底 + 品牌蓝鲸鱼），不跟随亮暗主题——开屏是一段「片子」，不是一块界面。
- 交互只做两件事：把节点挂上去、到点或被打断时把节点摘掉。

## License

[MIT](LICENSE) © 2026 Verayi2007
