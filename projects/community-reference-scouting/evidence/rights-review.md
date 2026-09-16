# 逐资产版权核查

核查日期：2026-09-15。这里记录实际条款和本项目的保守处理，不把公开可读等同于开放授权。所有保存资产的原始字节、尺寸和 SHA256 在 [reference evidence](../manifests/reference-evidence.json) 中。

<a id="plos"></a>
## E001–E003：PLOS Fig 4、5、6

- 原文：[Jambor & Bornhäuser 2024](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789)。版权段明确 Creative Commons Attribution，并链接 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。
- 逐一查看 Fig 4/5/6 caption：没有单列第三方署名或许可例外。未把同文其它图的权利自动扩展到它们，也未下载含多个第三方素材说明的 Fig 2。
- 保存：publisher 原始 PNG，未裁剪、重绘、去水印、改色或提取图标。文件名仅为管理重命名。
- 允许本批公开镜像；旁附作者、题名、DOI、图号、许可和未改动说明。图片仍按原始 CC BY 4.0 使用，不随仓库其它文件改变许可。

<a id="esurf"></a>
## E004：Eekhout et al. 2018 Fig 1

- 发现入口 S004 博客 footer 是 CC BY-NC 4.0，因此不从博客镜像图片。
- [出版原文](https://esurf.copernicus.org/articles/6/687/2018/)独立声明本文 CC BY 4.0；核查 Fig 1 caption，无单列第三方除外信息。
- 从原文 Download 链接取得图像；保留完整 PNG、作者、DOI 和图号。原图没有改动。
- 这条路线说明：权利判断绑定具体资产版本与来源，不能从博客的许可猜测出版版本，反之亦然。

## E005–E010：只留链接

- BioRender 的公开教程和免费模板入口不构成已验证的素材库重分发授权。本批仅保存原始页面 URL、定位和观察笔记；没有存入截图或拆取图标。参见 [S010 官方条款](https://help.biorender.com/hc/en-gb/articles/17605463719709-Publication-license-Terms-of-use)和 [S018 外部编辑要求](https://help.biorender.com/hc/en-gb/articles/17605449206045-Publication-license-guidelines-Editing-your-figure-outside-of-BioRender)。
- Simplified Science footer 有附 URL 分享条件，但本批未据此推断开放素材库和派生资产许可，只保留链接。
- Animate Your Science 配图和 Reddit 转贴图未逐资产核实公开重分发权，故只留链接。
- 小红书/知乎未访问成功，不下载、不镜像、不根据缓存伪造图像。

## 截图、图库和生成模型

[SMART 条款](https://smart.servier.com/terms-of-use/)区分可按 CC BY 4.0 使用的医学图片与不在该许可下的网页设计、logo 等内容。本批没有保存其网页截图或图片。未来 screenshot 必须核查画面内所有组成部分，避免个人信息、账号、评论头像和无关品牌元素；不能把裁剪或缩略图当作自动免责。

本批仅公开分发明确可用的参考图，不建立训练集或上传参考图至图像生成服务。将来用于模型输入、微调、重绘或衍生资产库，需重新审查实际用途和所用许可。禁止把 link-only 文件、分享 token、cookie、登录态或原始全文缓存提交 Git。

权利状态不能由校验器自动裁定；校验器只阻止缺证据、状态冲突、未知资产和哈希不一致。
