# Manifest contract v1

JSON 使用 UTF-8，`schema_version=1`。空值使用 null，不用空字符串假装有证据。S/R/E/CRP 是本项目命名空间，不与 PR20 M 编号混用。

## sources.json

`source_id`, `title`, `author`, `platform`, `canonical_url`, `published_date`（可 null）, `retrieved_date`, `evidence_kind`, `access_status`, `locator`, `observation`, `limitation`, `discovery_route`, `scientific_claim_evidence=false`。

access_status：text_read / text_and_selected_visual / partial_text / metadata_only / blocked。后两种不得支撑已提炼的设计规则。published_date 不明时必须 null，禁止以爬取日期代替发表日期。

## rules.json

`rule_id`, `title`, `action`, `applicable_to`（数组）, `do_not_transfer`, `evidence_level`, `source_ids`（数组）, `source_locator`, `validation`, `status=candidate`。

evidence_level：source_supported / visual_observation / curator_synthesis / project_guardrail / rights_policy / interface_contract。必须有可访问证据；来源数不等于独立证据数。

## reference-evidence.json

`asset_id`, `source_id`, `title`, `source_url`, `download_url`, `local_path`, `storage_policy`, `license`, `license_url`, `rights_evidence`, `attribution`, `modifications`, `third_party_review`, `sha256`, `bytes`, `width`, `height`, `qa_status`, `qa_note`, `inspected_date`, `approved_for_pr20=false`, `canonical_id=null`, `rule_ids`。

- public_mirror：必须给 local_path、SHA256、尺寸、许可、权利依据、署名、变更说明及 agent_visual_inspected。
- link_only：local_path/download_url/sha256/bytes/width/height 均 null；可为 agent_visual_inspected / text_only / uninspected / blocked。观察过不等于允许复制。
- 当前保存格式只支持 PNG；增加 SVG/PDF 等格式需要扩展验证器和风险检查。
- 实际 `assets/` 中所有文件必须被 manifest 精确列出；禁止私有或未标记附件混入。

## handoff/CRP001.json

跨文件引用必须存在；status=proposed，user_selection_required=true，approved_for_pr20=false，canonical_id=null。映射的是 PR20 已存在的 Style Recipe 字段，本模块不执行导入。

## 校验范围

脚本检查 ID、引用、状态、许可字段、路径越界、PNG 字节/尺寸/hash、未登记资产、私密 query 参数、Markdown 相对链接、提案状态。它不能证明网站权利声明真实、社区意见代表性或视觉美感；这些由 evidence 中的记录和后续用户审核承担。
