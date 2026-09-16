#!/usr/bin/env python3
"""Validate a bounded reference package without network access or PR20 writes."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import struct
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE_STATES = {'text_read', 'text_and_selected_visual', 'partial_text', 'metadata_only', 'blocked'}
EVIDENCE_LEVELS = {'source_supported', 'visual_observation', 'curator_synthesis',
                   'project_guardrail', 'rights_policy', 'interface_contract'}
SOURCE_KINDS = {'expert_vendor', 'practitioner', 'community_anecdote', 'expert_tutorial',
                'published_visual_example', 'rights_primary', 'discovery_index',
                'discovery_only', 'publisher_primary', 'repository_contract'}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def load():
    return [read(p) for p in ('manifests/sources.json', 'manifests/rules.json',
                             'manifests/reference-evidence.json', 'handoff/CRP001.json')]


def validate(pack, check_links=True):
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    def local_path(value):
        if not isinstance(value, str) or not value:
            return None
        p = (ROOT / value.split('#', 1)[0]).resolve()
        if not p.is_relative_to(ROOT) or Path(value).is_absolute():
            errors.append('Path escapes project: ' + value)
            return None
        return p

    for doc in pack:
        require(doc.get('schema_version') == 1, 'Unsupported schema version')
    sd, rd, ad, handoff = pack
    sources, rules, assets = sd['sources'], rd['rules'], ad['assets']
    for rows, key, pattern in ((sources, 'source_id', r'S\d{3}'),
                               (rules, 'rule_id', r'R\d{2}'),
                               (assets, 'asset_id', r'E\d{3}')):
        ids = [r.get(key) for r in rows]
        require(len(ids) == len(set(ids)), 'Duplicate ' + key)
        require(all(isinstance(i, str) and re.fullmatch(pattern, i) for i in ids), 'Invalid ' + key)
    sm = {s['source_id']: s for s in sources}
    rm = {r['rule_id']: r for r in rules}
    am = {a['asset_id']: a for a in assets}

    for s in sources:
        sid = s['source_id']
        for key in ('title', 'author', 'platform', 'canonical_url', 'retrieved_date',
                    'locator', 'observation', 'limitation', 'discovery_route'):
            require(bool(s.get(key)), f'{sid}: missing {key}')
        require(s.get('access_status') in SOURCE_STATES, f'{sid}: invalid access state')
        require(s.get('evidence_kind') in SOURCE_KINDS, f'{sid}: invalid evidence kind')
        require(s.get('scientific_claim_evidence') is False, f'{sid}: not biological evidence')
        require(s['canonical_url'].startswith('https://'), f'{sid}: noncanonical URL')

    for r in rules:
        rid = r['rule_id']
        for key in ('title', 'action', 'applicable_to', 'do_not_transfer', 'source_ids',
                    'source_locator', 'validation'):
            require(bool(r.get(key)), f'{rid}: missing {key}')
        require(r.get('status') == 'candidate', f'{rid}: automatic promotion forbidden')
        require(r.get('evidence_level') in EVIDENCE_LEVELS, f'{rid}: invalid evidence level')
        for sid in r['source_ids']:
            require(sid in sm, f'{rid}: missing source {sid}')
            if sid in sm:
                require(sm[sid]['access_status'] not in {'blocked', 'metadata_only'},
                        f'{rid}: inaccessible source cannot substantiate a rule: {sid}')

    mirrored_paths = set()
    for a in assets:
        aid = a['asset_id']
        require(a.get('source_id') in sm, f'{aid}: source missing')
        require(a.get('approved_for_pr20') is False and a.get('canonical_id') is None,
                f'{aid}: PR20 selection is not authorized by this package')
        require(all(r in rm for r in a.get('rule_ids', [])), f'{aid}: unknown rule')
        if a.get('storage_policy') == 'public_mirror':
            require(a.get('license') in {'CC-BY-4.0', 'CC0-1.0'}, f'{aid}: mirror license not allowed')
            for key in ('license_url', 'rights_evidence', 'attribution', 'modifications',
                        'third_party_review', 'sha256', 'qa_note', 'inspected_date'):
                require(bool(a.get(key)), f'{aid}: missing {key}')
            require(a.get('qa_status') == 'agent_visual_inspected', f'{aid}: visual inspection required')
            for key in ('rights_evidence', 'qa_note'):
                p = local_path(a.get(key))
                require(p is not None and p.is_file(), f'{aid}: missing evidence file {key}')
            p = local_path(a.get('local_path'))
            if p is None or not p.is_file():
                errors.append(f'{aid}: missing local asset')
                continue
            mirrored_paths.add(p.relative_to(ROOT).as_posix())
            data = p.read_bytes()
            require(p.suffix == '.png' and data[:8] == b'\x89PNG\r\n\x1a\n', f'{aid}: not a PNG')
            require(len(data) == a.get('bytes'), f'{aid}: byte count mismatch')
            require(hashlib.sha256(data).hexdigest() == a.get('sha256'), f'{aid}: hash mismatch')
            if len(data) >= 24:
                require(struct.unpack('>II', data[16:24]) == (a.get('width'), a.get('height')),
                        f'{aid}: dimension mismatch')
        elif a.get('storage_policy') == 'link_only':
            require(all(a.get(k) is None for k in ('local_path', 'download_url', 'sha256', 'bytes', 'width', 'height')),
                    f'{aid}: link-only asset must not contain local bytes or download pointer')
            require(a.get('qa_status') in {'agent_visual_inspected', 'text_only', 'uninspected', 'blocked'},
                    f'{aid}: invalid link-only QA state')
            if a.get('qa_status') == 'agent_visual_inspected':
                require(bool(a.get('qa_note')) and bool(a.get('inspected_date')), f'{aid}: missing inspection evidence')
        else:
            errors.append(f'{aid}: unknown storage policy')
    actual_assets = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'assets').rglob('*') if p.is_file()}
    require(actual_assets == mirrored_paths, 'Unmanifested or missing assets: ' + str(actual_assets ^ mirrored_paths))

    require(handoff.get('status') == 'proposed', 'Handoff must remain proposed')
    require(handoff.get('target_pr') == 20, 'Unexpected target PR')
    require(handoff.get('user_selection_required') is True, 'User selection must remain required')
    require(handoff.get('approved_for_pr20') is False and handoff.get('canonical_id') is None,
            'Handoff auto-approval forbidden')
    require(bool(re.fullmatch(r'[0-9a-f]{40}', handoff.get('target_snapshot_sha', ''))), 'Missing PR20 snapshot')
    for key, lookup in (('source_ids', sm), ('rule_ids', rm), ('asset_ids', am)):
        require(bool(handoff.get(key)), 'Handoff missing ' + key)
        require(all(i in lookup for i in handoff.get(key, [])), 'Handoff unresolved ' + key)
    for mapped in handoff.get('style_recipe_field_map', {}).values():
        require(all(i in handoff['rule_ids'] for i in mapped), 'Handoff maps undeclared rule')

    forbidden_query_keys = {'xsec_token', 'share_id', 'token', 'access_token', 'api_key', 'cookie',
                            'x-goog-signature', 'x-goog-credential', 'signature'}
    all_text = json.dumps(pack, ensure_ascii=False)
    for url in re.findall(r'https?://[^\s<>"\)]+', all_text):
        keys = {k.lower() for k in parse_qs(urlsplit(url).query)}
        require(not keys.intersection(forbidden_query_keys), 'Sensitive URL query parameter')
    if check_links:
        for md in ROOT.rglob('*.md'):
            body = md.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)', body):
                if target.startswith(('https://', 'http://', '#', 'mailto:')):
                    continue
                target = unquote(target.split('#')[0])
                require((md.parent / target).is_file(), f'{md.name}: missing local link {target}')
    return errors


def self_test(pack):
    """Negative cases test rights/provenance gates, without touching real assets."""
    cases = [
        ('unknown source', lambda p: p[1]['rules'][0]['source_ids'].append('S999')),
        ('blocked source supporting rule', lambda p: p[1]['rules'][0]['source_ids'].append('S014')),
        ('unlicensed mirror', lambda p: p[2]['assets'][0].update(license='not_verified')),
        ('incorrect hash', lambda p: p[2]['assets'][0].update(sha256='0' * 64)),
        ('escaping path', lambda p: p[2]['assets'][0].update(local_path='../outside.png')),
        ('link-only with local path', lambda p: p[2]['assets'][4].update(local_path='assets/public/secret.png')),
        ('automatic PR20 approval', lambda p: p[3].update(approved_for_pr20=True)),
        ('sensitive sharing URL', lambda p: p[0]['sources'][0].update(canonical_url='https://example.org/?xsec_token=TEST')),
    ]
    for name, mutation in cases:
        probe = copy.deepcopy(pack)
        mutation(probe)
        if not validate(probe, check_links=False):
            raise AssertionError('Gate failed to reject: ' + name)
    return len(cases)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        pack = load()
        errors = validate(pack)
        if errors:
            print(json.dumps({'status': 'FAIL', 'errors': errors}, indent=2, ensure_ascii=False))
            return 1
        result = {'status': 'PASS', 'sources': len(pack[0]['sources']), 'rules': len(pack[1]['rules']),
                  'reference_records': len(pack[2]['assets']),
                  'public_assets': sum(a['storage_policy'] == 'public_mirror' for a in pack[2]['assets'])}
        if args.self_test:
            result['negative_cases_rejected'] = self_test(pack)
        print(json.dumps(result, indent=2))
        return 0
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
