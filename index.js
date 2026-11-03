/**
 * 大肥鱼开屏 · 宿主半边。
 *
 * 这个插件不在 Host 里做任何事：不注册服务、不加工具、不联网。
 * 渲染全在客户端半边（./client.js），由 `dsh.client` 声明加载。
 * 这里保留一个空 apply，是为了让 bundle patch 里那一行有东西可挂。
 */
export function apply() {}
