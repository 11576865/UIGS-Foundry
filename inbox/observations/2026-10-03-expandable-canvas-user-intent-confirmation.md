# 可扩展画布工作区：用户意图确认

- Type: Observation
- Status: Unpromoted
- Date: 2026-10-03 (Asia/Shanghai)
- Family: UIGS.RECIPE.MULTI_INSTANCE_TOOL_WORKSPACE
- Related patterns: UIGS.NAVIGATION.CAPABILITY_CATALOG; UIGS.WORKSPACE.TRANSIENT_COMMITTED_SURFACE_GEOMETRY; UIGS.WORKSPACE.EXPLICIT_TOOL_BINDING

## Provenance and evidence

用户本轮明确表示无限画布正是其此前缺少的组织方式，并将其与在有限空间中叠加 UI 的思路区分。附件 Screenrecorder-2026-10-03-22-56-12-241.mp4（libfile_84ef0b79b2a08191bd86392a877e4dbf，时长约 14.74 秒）在约 3 秒和 11 秒的抽帧中显示预览、字幕导航和正文工具，以及 62% 和 94% 的工作区缩放状态。此次仅做抽帧核对，没有代码检查、完整交互测试或性能验证。

Evidence level: 单一用户偏好陈述 + 局部录屏视觉证据。不能推导所有用户均受益、任意功能适配或无限资源容量。

## Reusable observation

有限屏幕与可扩展工作区可以分离：工具保留空间位置，视口选择当前可见区域。这为不断增长的专业工具提供组织方向。用户先前关于解除空间强塞的需求，在本次具体界面中获得了明确的偏好确认；不是新增一套业务系统的要求。

## Expected effect and proposed validation

预期效果：增加工具不必重新压缩全部现有面板；概览与局部编辑可切换。待验证：新增工具后原布局与对象绑定保持；通过目录或导航召回视口外工具；缩小时点击目标仍可用或进入摘要表示；重新打开工程可恢复布局；手机上画布平移不与面板内容滚动、时间轴操作冲突。

## Limits / known risks

可容纳不等于可发现、可操作或高效。离屏工具迷失、过小点击目标、对象绑定混淆、手势争用和资源增长是待测试风险，不能据本次录屏断言已发生。旧报告允许空间画布但未将其强制设为所有任务的唯一组织方式；本次偏好确认不自动修改 Canonical。

## Dedupe

已检查 Foundry 树中的 registry/inbox 文件名，并读取现有 MULTI_INSTANCE_TOOL_WORKSPACE recipe 与 TOOL_CANVAS.WEB_REFERENCE manifest；复用现有 family，仅补充本轮用户意图与视觉证据，未创建重复 Pattern。

## User clarification — 2026-10-03 23:08 Asia/Shanghai

用户纠正了将无限画布仅理解为工具布局/展示策略的狭窄解读：无限画布是展示空间本身，是可以承载此前讨论的 UI 设计的空间基底。用户同时强调手指手势对缩放、移动、编辑、改变对象和层次、跳转、叠加、淡入淡出的统一操控意图。

Interpretation: 画布可作为可缩放空间界面（Zoomable User Interface, ZUI）的基底；工具、列表、时间轴、预览和组合面板作为其承载的界面对象。后续设计应区分视口导航、对象编辑、层级/组合操作和表现过渡，但保留同一连续空间中的直接操纵体验。屏幕固定入口也可作为空间导航的辅助层，而非要求所有控件随世界坐标缩小。

Evidence boundary: 此段是明确用户意图及设计解释；没有证明所列手势已实现，也不将空间容量等同于业务能力或无限资源。后续验证应覆盖手势目标判定、对象与视口变换隔离、层级操作及返回路径。更新同一 Observation，不创建新 Pattern，不提升 Canonical。
